#!/bin/bash
# Horizon → Obsidian 同步脚本

SOURCE_DIR="/Users/huanghaoming/Documents/Obsidian优化/data/summaries"
OBSIDIAN_DIR="/Users/huanghaoming/Library/Mobile Documents/com~apple~CloudDocs/Obsidian/Hyman Ai Viki/Hyman Ai Viki/Horizon-Daily"

# 创建目标目录（如果不存在）
mkdir -p "$OBSIDIAN_DIR"

# 复制最新的摘要文件
if [ -d "$SOURCE_DIR" ]; then
    cp -n "$SOURCE_DIR"/*.md "$OBSIDIAN_DIR/" 2>/dev/null
    echo "✅ 已同步 Horizon 日报到 Obsidian"
else
    echo "⚠️ 源目录不存在: $SOURCE_DIR"
fi
