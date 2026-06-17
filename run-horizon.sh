#!/bin/bash
cd /Users/huanghaoming/Documents/Obsidian优化

echo "🚀 运行 Horizon..."
/Users/huanghaoming/.local/bin/uv run horizon 2>&1 | tee ~/Library/Logs/horizon.log

echo ""
echo "📱 同步到 Obsidian..."
/Users/huanghaoming/Documents/Obsidian优化/sync-to-obsidian.sh
