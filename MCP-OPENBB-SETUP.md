# Horizon 高级功能配置

## MCP 服务（AI 工具调用）

### 启动 MCP 服务器

```bash
cd /Users/huanghaoming/Documents/Obsidian优化
/Users/huanghaoming/.local/bin/uv run horizon-mcp
```

### 可用工具
- `hz_validate_config` - 验证配置
- `hz_fetch_items` - 获取内容
- `hz_score_items` - AI 评分
- `hz_filter_items` - 筛选内容
- `hz_enrich_items` - 补充背景知识
- `hz_generate_summary` - 生成摘要
- `hz_run_pipeline` - 运行完整流程

### 注意事项
- Codex CLI 目前不支持添加自定义 MCP 服务器
- 可以手动启动 MCP 服务后，通过其他支持 MCP 的客户端使用

---

## OpenBB 财经

### 配置状态
已在 `data/config.json` 中添加配置：
- AI 相关股票：NVDA, MSFT, GOOGL, META, AMD, INTC
- 加密货币：BTC, ETH

### 安装依赖
由于网络问题，需要手动安装：

```bash
cd /Users/huanghaoming/Documents/Obsidian优化

# 方法1: 使用 uv（推荐）
/Users/huanghaoming/.local/bin/uv pip install --only-binary=:all: openbb openbb-benzinga

# 方法2: 使用 pip
pip install openbb openbb-benzinga

# 方法3: 如果上述都失败，从源码安装
pip install --no-build-isolation openbb
```

### 验证安装
```bash
/Users/huanghaoming/.local/bin/uv run python -c "from openbb import TerminalInterface; print('✅ OpenBB 安装成功')"
```

### 启用后功能
- 获取 AI/科技股最新新闻
- 加密货币行情和新闻
- 财报发布提醒
- 机构评级变化
