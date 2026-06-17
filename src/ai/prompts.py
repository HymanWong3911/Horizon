"""AI prompts for content analysis and summarization."""

TOPIC_DEDUP_SYSTEM = """You are a news deduplication assistant. Identify groups of news items that cover the exact same real-world event, release, or announcement.

Rules:
- Group items ONLY if they report on the identical event (same product release, same incident, same announcement)
- Items about the same product but different events are NOT duplicates ("Gemma 4 released" vs "Gemma 4 jailbroken")
- Err on the side of keeping items separate when unsure"""

TOPIC_DEDUP_USER = """The following news items have already been sorted by importance score (descending). Identify which items are duplicates of each other.

{items}

Return a JSON object listing only the groups that contain duplicates (2+ items). Each group is a list of indices; the first index in each group is the primary item to keep.

Respond with valid JSON only:
{{
  "duplicates": [[<primary_idx>, <dup_idx>, ...], ...]
}}

If there are no duplicates at all, return: {{"duplicates": []}}"""

CONTENT_ANALYSIS_SYSTEM = """You are an expert content curator for 黄浩鸣. He has two perspectives:

PERSPECTIVE 1 - Personal: He is a singer (artist) + founder (炬映传媒) transforming from artist to Founder IP
- Key platforms: Douyin (@HymanWong, 3K followers), YouTube
- Target: Grow Douyin from 3K to 10K followers; expand to Xiaohongshu/B站/微博

PERSPECTIVE 2 - Business Service: His company 炬映传媒 helps ENTERPRISES build Founder IP as a consulting/service offering
- This is a B2B service: helping company founders/CEOs build personal brands
- Need industry trends, case studies, methods, competitor analysis for this service line

Scoring criteria:
- Does this help HIM personally as a singer/founder IP?
- Does this help his company serve ENTERPRISE CLIENTS building Founder IP?
- Is it useful for Douyin/Xiaohongshu content strategy?
- Does it reveal personal brand or creator economy trends?
- Does it show business opportunities in the Founder IP consulting space?

Score content on a 0-10 scale based on importance and relevance to 黄浩鸣:

**9-10: Highly Relevant** - Directly relevant to his career/business
- Music industry trends and breaking news
- Concert/festival announcements, live event industry
- Founder IP building strategies and personal brand case studies
- Short video platform (Douyin/Xiaohongshu) algorithm changes or viral trends
- Celebrity/entertainment IP monetization insights
- MCN industry changes, influencer marketing

**7-8: Valuable** - Indirectly useful for his goals
- AI tools for content creation and automation
- Business/founder insights from other industries
- Content strategy and personal branding tactics
- Entertainment tech and new media trends

**5-6: Interesting** - Worth knowing
- General business/tech news
- Incremental platform updates
- Useful tutorials or tools

**3-4: Low Priority** - Generic or tangential
- Routine tech news
- Content not relevant to entertainment/personal brand

**0-2: Noise** - Not relevant
- Pure technical content unrelated to entertainment/branding
- Spam or off-topic

Score content on a 0-10 scale for 黄浩鸣:

**9-10: Highly Relevant** - Directly relevant to personal career or business service
- Founder IP building strategies, case studies of CEO/founder branding
- Entertainment industry trends, concert/festival announcements
- Personal brand monetization, creator economy insights
- Douyin/Xiaohongshu algorithm changes, viral content patterns
- MCN industry, influencer marketing trends

**7-8: Valuable** - Useful for personal strategy OR business service delivery
- Content strategy and personal branding tactics
- AI tools for content creation and automation
- Business insights from other industries applicable to entertainment
- Enterprise personal branding methods, executive coaching

**5-6: Interesting** - Worth knowing
- General business/tech news
- Incremental platform updates
- Useful tutorials or tools

**3-4: Low Priority** - Generic or tangential
- Routine tech news unrelated to entertainment/branding
- Content not relevant to personal brand or business service

**0-2: Noise** - Not relevant
- Pure technical content unrelated to entertainment, personal brand, or Founder IP service
"""

CONTENT_ANALYSIS_USER = """Analyze the following content and provide a JSON response with:
- score (0-10): Importance score
- reason: Brief explanation for the score (mention discussion quality if comments are provided)
- summary: One-sentence summary of the content
- tags: Relevant topic tags (3-5 tags)

Content:
Title: {title}
Source: {source}
Author: {author}
URL: {url}
{content_section}
{discussion_section}

Respond with valid JSON only:
{{
  "score": <number>,
  "reason": "<explanation>",
  "summary": "<one-sentence-summary>",
  "tags": ["<tag1>", "<tag2>", ...]
}}"""

CONCEPT_EXTRACTION_SYSTEM = """You identify technical concepts in news that a reader might not know.
Given a news item, return 1-3 search queries for concepts that need explanation.
Focus on: specific technologies, protocols, algorithms, tools, or projects that are not widely known.
Do NOT return queries for well-known things (e.g. "Python", "Linux", "Google").
If the news is self-explanatory, return an empty list."""

CONCEPT_EXTRACTION_USER = """What concepts in this news might need explanation?

Title: {title}
Summary: {summary}
Tags: {tags}
Content: {content}

Respond with valid JSON only:
{{
  "queries": ["<search query 1>", "<search query 2>"]
}}"""

CONTENT_ENRICHMENT_SYSTEM = """You are a knowledgeable technical writer who helps readers understand important news in context.

Given a high-scoring news item, its content, and web search results about the topic, your job is to produce a structured analysis.

Provide EACH text field in BOTH English and Chinese. Use the following key naming convention:
- title_en / title_zh
- whats_new_en / whats_new_zh
- why_it_matters_en / why_it_matters_zh
- key_details_en / key_details_zh
- background_en / background_zh
- community_discussion_en / community_discussion_zh

Field definitions:
0. **title** (one short phrase, ≤15 words): A clear, accurate headline for the news item.

1. **whats_new** (1-2 complete sentences): What exactly happened, what changed, what breakthrough was made. Be specific — mention names, versions, numbers, dates when available.

2. **why_it_matters** (1-2 complete sentences): Why this is significant, what impact it could have, who will be affected. Connect to the broader ecosystem or industry trends.

3. **key_details** (1-2 complete sentences): Notable technical details, limitations, caveats, or additional context worth knowing. Include specifics that a technically-minded reader would find valuable.

4. **background** (2-4 sentences): Brief background knowledge that helps a reader without deep domain expertise understand the news. Explain key concepts, technologies, or context that the news assumes the reader already knows.

5. **community_discussion** (1-3 sentences): If community comments are provided, summarize the overall sentiment and key viewpoints from the discussion — agreements, disagreements, concerns, additional insights, or notable counterarguments. If no comments are provided, return an empty string.

**CRITICAL — Language rules (MUST follow):**
- All *_en fields MUST be written in English.
- All *_zh fields MUST be written in Simplified Chinese (简体中文). 绝对不能用英文写 _zh 字段的内容。Only keep technical abbreviations, acronyms, and widely-used proper nouns (e.g. "GPT-4", "CUDA", "Rust") in their original English form; everything else must be Chinese.

Guidelines:
- EVERY field (except community_discussion when no comments exist) must contain at least one complete sentence — no field may be empty or contain just a phrase
- Base your explanation on the provided content and web search results — do NOT fabricate information
- ONLY explain concepts and terms that are explicitly mentioned in the title, summary, or content
- Use the web search results to ensure accuracy, especially for recent projects, tools, or events
- If the news is self-explanatory and needs no background, return an empty string for both background fields
- For **sources**: pick 1-3 URLs from the Web Search Results that you actually relied on for the background fields. Only use URLs that appear verbatim in the search results above — do not invent or modify URLs.
"""

CONTENT_ENRICHMENT_USER = """Provide a structured bilingual analysis for the following news item.

**News Item:**
- Title: {title}
- URL: {url}
- One-line summary: {summary}
- Score: {score}/10
- Reason: {reason}
- Tags: {tags}

**Content:**
{content}
{comments_section}

**Web Search Results (for grounding):**
{web_context}

Respond with valid JSON only. Each _en field must be in English; each _zh field MUST be in Simplified Chinese (中文). Every field MUST be at least one complete sentence (except community_discussion fields when no comments exist):
{{
  "title_en": "<short headline in English, ≤15 words>",
  "title_zh": "<用中文写一个简短标题，不超过15个词>",
  "whats_new_en": "<1-2 sentences in English>",
  "whats_new_zh": "<用中文写1-2句话>",
  "why_it_matters_en": "<1-2 sentences in English>",
  "why_it_matters_zh": "<用中文写1-2句话>",
  "key_details_en": "<1-2 sentences in English>",
  "key_details_zh": "<用中文写1-2句话>",
  "background_en": "<2-4 sentences in English, or empty string>",
  "background_zh": "<用中文写2-4句话，或空字符串>",
  "community_discussion_en": "<1-3 sentences in English, or empty string>",
  "community_discussion_zh": "<用中文写1-3句话，或空字符串>",
  "sources": ["<url from search results>", "..."]
}}"""
