"""Content analysis using AI."""

import asyncio
import json
import re
from typing import List, Optional
from tenacity import retry, stop_after_attempt, wait_exponential
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, MofNCompleteColumn

from .client import AIClient
from .prompts import CONTENT_ANALYSIS_SYSTEM, CONTENT_ANALYSIS_USER
from .utils import parse_json_response
from ..models import ContentItem

DEFAULT_THROTTLE_SEC = 0.0



# Keywords relevant to 黄浩鸣 - boost score if present in title
_HYMAN_KEYWORDS = {
    # 创始人IP/个人品牌核心词
    "创始人IP": 1.5, "个人品牌": 1.5, "创始人品牌": 1.5, "CEO品牌": 1.5,
    "品牌打造": 1.2, "IP打造": 1.5, "IP孵化": 1.5, "个人IP": 1.5,
    # 娱乐/音乐行业
    "演唱会": 1.5, "音乐节": 1.5, "Livehouse": 1.5, "livehouse": 1.5,
    "音乐现场": 1.5, "艺人": 1.3, "歌手": 1.3, "唱片": 1.3,
    "Billboard": 1.3, "综艺": 1.3, "明星": 1.2, "艺人经纪": 1.5,
    "音乐版权": 1.5, "版权": 1.2,
    # 短视频/内容创作
    "短视频": 1.5, "抖音": 1.3, "小红书": 1.3, "B站": 1.3,
    "直播": 1.3, "带货": 1.2, "达人": 1.3, "KOL": 1.3,
    "内容创作": 1.3, "内容策略": 1.5, "爆款": 1.3,
    # 炬映传媒业务
    "炬映": 2.0, "黄浩鸣": 2.0,
    # 企业服务
    "企业创始人": 1.5, "CEO营销": 1.5, "高管IP": 1.5, "企业家IP": 1.5,
    # 商业/增长
    "融资": 1.2, "增长": 1.2, "变现": 1.3, "商业化": 1.2,
    # 影响力
    "影响力": 1.5, "粉丝": 1.2, "破圈": 1.5, "出圈": 1.5,
}


def _apply_keyword_boost(item: ContentItem) -> None:
    """Apply keyword-based score boost for items relevant to 黄浩鸣."""
    title_lower = item.title.lower()
    max_boost = 0.0
    hit_keywords = []
    
    for keyword, boost in _HYMAN_KEYWORDS.items():
        if keyword.lower() in title_lower:
            if boost > max_boost:
                max_boost = boost
            hit_keywords.append(keyword)
    
    if max_boost > 0 and item.ai_score is not None:
        old_score = item.ai_score
        item.ai_score = min(10.0, item.ai_score * max_boost)
        if item.ai_reason:
            item.ai_reason += f" [关键词命中: {', '.join(hit_keywords)}, x{max_boost:.1f}]"
        if hit_keywords and "炬映" in hit_keywords or "黄浩鸣" in hit_keywords:
            item.ai_score = 10.0  # Absolute priority for own brand


class ContentAnalyzer:
    """Analyzes content items using AI to determine importance."""

    def __init__(self, ai_client: AIClient):
        self.client = ai_client

    @staticmethod
    def _parse_json_response(response: str) -> Optional[dict]:
        """Try multiple strategies to extract a JSON object from an AI response.

        Returns the parsed dict, or None if all strategies fail.
        """
        return parse_json_response(response)

    def _get_throttle_sec(self) -> float:
        """Return the configured inter-item throttle, clamped to zero or above."""
        config = getattr(self.client, "config", None)
        throttle_sec = getattr(config, "throttle_sec", DEFAULT_THROTTLE_SEC)
        return max(throttle_sec, 0.0)

    def _get_concurrency(self) -> int:
        """Return the configured analysis concurrency, clamped to 1 or above."""
        config = getattr(self.client, "config", None)
        concurrency = getattr(config, "analysis_concurrency", 1)
        return max(concurrency, 1)

    async def analyze_batch(self, items: List[ContentItem]) -> List[ContentItem]:
        throttle_sec = self._get_throttle_sec()
        concurrency = self._get_concurrency()
        semaphore = asyncio.Semaphore(concurrency)

        async def _process(item: ContentItem, index: int, progress_task) -> ContentItem:
            async with semaphore:
                try:
                    await self._analyze_item(item)
                    _apply_keyword_boost(item)
                except Exception as e:
                    print(f"Error analyzing item {item.id}: {e}")
                    item.ai_score = 0.0
                    item.ai_reason = "Analysis failed"
                    item.ai_summary = item.title
                if throttle_sec > 0 and index < len(items) - 1:
                    await asyncio.sleep(throttle_sec)
            progress.advance(progress_task)
            return item

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            MofNCompleteColumn(),
            transient=True,
        ) as progress:
            task = progress.add_task("Analyzing", total=len(items))
            coros = [
                _process(item, i, task) for i, item in enumerate(items)
            ]
            analyzed_items = await asyncio.gather(*coros)

        return analyzed_items

    @retry(
        stop=stop_after_attempt(2),
        wait=wait_exponential(min=1, max=5)
    )
    async def _analyze_item(self, item: ContentItem) -> None:
        """Analyze a single content item.

        Args:
            item: Content item to analyze (modified in-place)
        """
        # Prepare content section
        content_section = ""
        if item.content:
            # Split off comments if present
            content_text = item.content
            if "--- Top Comments ---" in content_text:
                main, comments_part = content_text.split("--- Top Comments ---", 1)
                content_section = f"Content: {main.strip()[:800]}"
            else:
                content_section = f"Content: {content_text[:1000]}"

        # Prepare discussion section (comments, engagement)
        discussion_parts = []
        if item.content and "--- Top Comments ---" in item.content:
            comments_part = item.content.split("--- Top Comments ---", 1)[1]
            discussion_parts.append(f"Community Comments:\n{comments_part[:1500]}")

        meta = item.metadata
        engagement_items = []
        if meta.get("score"):
            engagement_items.append(f"score: {meta['score']}")
        if meta.get("descendants"):
            engagement_items.append(f"{meta['descendants']} comments")
        if meta.get("favorite_count"):
            engagement_items.append(f"{meta['favorite_count']} likes")
        if meta.get("retweet_count"):
            engagement_items.append(f"{meta['retweet_count']} retweets")
        if meta.get("reply_count"):
            engagement_items.append(f"{meta['reply_count']} replies")
        if meta.get("views"):
            engagement_items.append(f"{meta['views']} views")
        if meta.get("bookmarks"):
            engagement_items.append(f"{meta['bookmarks']} bookmarks")
        if meta.get("upvote_ratio"):
            engagement_items.append(f"upvote ratio: {meta['upvote_ratio']:.0%}")
        if engagement_items:
            discussion_parts.append(f"Engagement: {', '.join(engagement_items)}")
        if meta.get("discussion_url"):
            discussion_parts.append(f"Discussion: {meta['discussion_url']}")
        if meta.get("community_note"):
            discussion_parts.append(f"Community Note: {meta['community_note']}")

        discussion_section = "\n".join(discussion_parts) if discussion_parts else ""

        # Generate user prompt
        user_prompt = CONTENT_ANALYSIS_USER.format(
            title=item.title,
            source=f"{item.source_type.value}",
            author=item.author or "Unknown",
            url=str(item.url),
            content_section=content_section,
            discussion_section=discussion_section
        )

        # Get AI completion (with 60s timeout - doubao 卡住时不再无界挂死)
        try:
            response = await asyncio.wait_for(
                self.client.complete(
                    system=CONTENT_ANALYSIS_SYSTEM,
                    user=user_prompt,
                ),
                timeout=60.0,
            )
        except (asyncio.TimeoutError, Exception) as exc:
            raise RuntimeError(f"analyze timeout/error: {type(exc).__name__}")

        # Parse JSON response with robust fallback
        result = self._parse_json_response(response)
        if result is None:
            print(f"Warning: could not parse analysis response for {item.id}, using defaults")
            item.ai_score = 0.0
            item.ai_reason = "Analysis response parse failed"
            item.ai_summary = item.title
            item.ai_tags = []
            return

        # Update item with analysis results
        item.ai_score = float(result.get("score", 0))
        item.ai_reason = result.get("reason", "")
        item.ai_summary = result.get("summary", item.title)
        item.ai_tags = result.get("tags", [])
