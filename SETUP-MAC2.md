# Horizon 在另一台 Mac 上的设置指南

## 1. 克隆你的定制版本
```bash
git clone https://github.com/HymanWong3911/Horizon.git ~/Horizon-Hyman
cd ~/Horizon-Hyman
git checkout hyman-custom
```

## 2. 安装依赖
```bash
cd ~/Horizon-Hyman
curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync
```

## 3. 配置环境变量（复制 .env）
把本 Mac 的 /Users/huanghaoming/Documents/Obsidian优化/.env 内容复制过去，或者手动创建：
```bash
cp .env.example .env
# 然后编辑 .env，填入：
# DOUBAO_API_KEY=<YOUR_DOUBAO_API_KEY>
# MINIMAX_API_KEY=<YOUR_MINIMAX_API_KEY>
# FEISHU_WEBHOOK_URL=https://open.feishu.cn/open-apis/bot/v2/hook/<YOUR_FEISHU_WEBHOOK_ID>
# GITHUB_TOKEN=<YOUR_GITHUB_TOKEN>
```

## 4. 复制配置文件
```bash
cp data/config.json.example data/config.json
# 编辑 data/config.json（可以从本 Mac 的 config.json 复制）
```

## 5. 设置定时任务（可选，另一台 Mac 也要自动运行）
```bash
# 编辑 com.horizon.daily.plist 中的 StartCalendarInterval
```

## 6. 运行测试
```bash
uv run horizon --hours 6
```

## 同步代码更新
```bash
cd ~/Horizon-Hyman
git pull hyman hyman-custom
```
