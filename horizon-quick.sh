#!/bin/bash
case "$1" in
    "run")
        cd /Users/huanghaoming/Documents/Obsidian优化
        /Users/huanghaoming/.local/bin/uv run horizon
        ;;
    "read"|"news")
        FILE=$(ls -t /Users/huanghaoming/Documents/Obsidian优化/data/summaries/horizon-*-zh.md 2>/dev/null | head -1)
        if [ -f "$FILE" ]; then
            head -80 "$FILE"
        else
            echo "没有找到日报文件"
        fi
        ;;
    "status"|"check")
        echo "📁 最新文件："
        ls -lt /Users/huanghaoming/Documents/Obsidian优化/data/summaries/*.md 2>/dev/null | head -3
        echo ""
        echo "📱 Obsidian 同步："
        ls -lt "/Users/huanghaoming/Library/Mobile Documents/com~apple~CloudDocs/Obsidian/Hyman Ai Viki/Hyman Ai Viki/Horizon-Daily/" 2>/dev/null | head -3
        echo ""
        echo "📋 运行日志（最后10行）："
        tail -10 ~/Library/Logs/horizon.log 2>/dev/null
        ;;
    "sync")
        /Users/huanghaoming/Documents/Obsidian优化/sync-to-obsidian.sh
        ;;
    *)
        echo "Horizon 快捷命令"
        echo "用法: horizon-quick.sh [run|read|status|sync]"
        echo ""
        echo "  run    - 运行 Horizon"
        echo "  read   - 查看最新日报"
        echo "  status - 检查状态"
        echo "  sync   - 同步到 Obsidian"
        ;;
esac
