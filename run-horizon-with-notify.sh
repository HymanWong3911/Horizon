#!/bin/bash
LOG="/Users/huanghaoming/Library/Logs/horizon.log"
PROJ="/Users/huanghaoming/Documents/Obsidian优化"
GITHUB_TOKEN=$(grep "GITHUB_TOKEN=" "$PROJ/.env" 2>/dev/null | grep -v "^#" | cut -d= -f2 | tr -d '"' | tr -d "'")
TODAY=$(date +%Y-%m-%d)

echo "🚀 [$(date)] Horizon 自动运行开始" >> "$LOG"

cd "$PROJ"

# 运行 Horizon
"$PROJ/.venv/bin/uv" run horizon 2>&1 | tee -a "$LOG"
RESULT=$?

# 同步到 Obsidian
"$PROJ/sync-to-obsidian.sh"

# 发送 macOS 通知
if [ $RESULT -eq 0 ]; then
    osascript -e 'display notification "Horizon 日报已生成！" with title "📰 Horizon 完成"'
else
    osascript -e 'display notification "Horizon 运行出错，请检查日志" with title "⚠️ Horizon 错误"'
fi

echo "✅ [$(date)] Horizon 运行完成" >> "$LOG"

# GitHub Pages 自动发布
if [ -n "$GITHUB_TOKEN" ] && [ -d "$PROJ/docs/_posts" ]; then
    # 克隆 gh-pages 到临时目录
    TEMP_DIR=$(mktemp -d)
    echo "📄 推送日报到 GitHub Pages..."
    GIT_HTTPS_URL="https://${GITHUB_TOKEN}@github.com/Thysrael/Horizon.git"
    if git clone --branch gh-pages --depth 1 "$GIT_HTTPS_URL" "$TEMP_DIR" 2>/dev/null; then
        # 复制最新日报
        cp "$PROJ/data/summaries/horizon-${TODAY}"*-zh.md "$TEMP_DIR/docs/_posts/" 2>/dev/null
        cp "$PROJ/data/summaries/horizon-${TODAY}"*-en.md "$TEMP_DIR/docs/_posts/" 2>/dev/null
        cd "$TEMP_DIR"
        git config user.email "horizon@huanghaoming.com" 2>/dev/null
        git config user.name "Horizon Bot" 2>/dev/null
        git add docs/_posts/
        if ! git diff --cached --quiet; then
            git commit -m "Auto-publish: $TODAY" && git push origin gh-pages && echo "✅ 已推送日报到 GitHub Pages" || echo "⚠️ GitHub Pages 推送失败"
        else
            echo "📄 无新日报需要推送"
        fi
    fi
    rm -rf "$TEMP_DIR"
    cd "$PROJ"
fi
