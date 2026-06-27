<div align="center">

# PaddleOCR MCP Server

📖 [**中文**](#中文) &nbsp;|&nbsp; 🌐 [**English**](#english)

[![Python](https://img.shields.io/badge/python-3.8%2B-blue?logo=python)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![PaddleOCR](https://img.shields.io/badge/PaddleOCR-3.7%2B-orange)](https://github.com/PaddlePaddle/PaddleOCR)
[![MCP](https://img.shields.io/badge/MCP-Compatible-purple)](https://modelcontextprotocol.io)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen)](https://github.com/YuanJinke/paddleocr_mcp/pulls)
[![GitHub Stars](https://img.shields.io/github/stars/YuanJinke/paddleocr_mcp?style=flat&logo=github)](https://github.com/YuanJinke/paddleocr_mcp)

</div>

---

<a id="中文"></a>

<div align="center">

# 🏮 中文

</div>

# PaddleOCR MCP Server

基于 [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) 的 [模型上下文协议 (MCP)](https://modelcontextprotocol.io/) 服务器，为 AI Agent 提供本地图片文字识别能力。

## 🚀 核心优势

| 特性 | PaddleOCR MCP | 云端 OCR API |
|------|--------------|-------------|
| **费用** | 💰 **免费**，零成本 | 按次收费 |
| **隐私** | 🔒 **100% 本地**，数据不出设备 | 数据上传云端 |
| **网络** | 📡 **离线可用**，无需联网 | 依赖网络 |
| **延迟** | ⚡ ~1-3 秒 | ~0.5-3 秒 + 网络耗时 |
| **语言** | 🌍 支持 109 种语言 | 视服务商而定 |
| **模型** | 🤖 支持 **DeepSeek-v4** 等任意大模型搭配 | 厂商锁定 |
| **开源** | 📂 **完全开源**，可自由修改 | 闭源黑盒 |
| **部署** | 🖥️ 低成本 CPU 即可运行 | 需高成本服务器 |

> 💡 **搭配 DeepSeek-v4 的低成本方案**：PaddleOCR 负责提取图片文字，DeepSeek-v4 等大模型负责理解分析——本地运行，无需 GPU，开发成本趋近于零。

## 🤖 自动识别机制

> **即使你的模型不支持看图（纯文本模型），AI Agent 也能自动调用 `ocr_image` MCP 工具识别图片文字后返回结果。**

举个例子：
1. 用户发送一张截图
2. AI Agent 发现该模型不支持直接看图
3. 自动调用 `ocr_image` 工具提取图片中的文字
4. 基于提取的文字内容进行分析和回答

这意味着：
- ✅ **无需切换模型** — 纯文本模型也能"看懂"图片
- ✅ **零额外配置** — MCP 挂载后自动生效
- ✅ **透明使用** — 用户只需发图，Agent 自动处理

## ✨ 功能特性

- **纯文字识别** — `ocr_image(image_path)` 一键提取图片中全部文字
- **中英混合** — 原生支持中文 + 英文混合识别
- **109 种语言** — 覆盖全球主要语言
- **本地离线** — 无需 API Key，首次下载模型后完全离线
- **轻量快速** — PP-OCRv6 模型仅 34.5M 参数，CPU 流畅运行
- **MCP 标准** — 兼容所有 MCP 客户端

## 🎯 适用场景

- 🤖 搭配 **DeepSeek-v4、GLM、Qwen** 等大模型做图片内容理解
- 📄 文档扫描件、截图文字提取
- 🏭 工业场景：车牌、标签、单据识别
- 🌐 多语言文档处理

## 📦 快速开始

### 环境要求

- Python 3.8~3.12
- Node.js 18+（仅 Claude Code 等客户端需要，服务端本身不需要）

### 安装

```bash
# 安装 PaddleOCR 和 PaddlePaddle
pip install paddlepaddle==3.2.0 paddleocr

# 克隆本仓库
git clone https://github.com/YuanJinke/paddleocr_mcp.git
cd paddleocr_mcp
```

> ⚠️ **Windows 用户注意**：PaddlePaddle 3.3.1 有 oneDNN 兼容性问题，请务必安装 **3.2.0** 版本。

### 配置到你的 MCP 客户端

<details>
<summary><b>Claude Code</b> 👈 点击展开</summary>

```bash
claude mcp add -s user paddleocr -- python /路径/paddleocr_mcp.py
```

或添加到 `~/.claude.json`：
```json
{
  "mcpServers": {
    "paddleocr": {
      "type": "stdio",
      "command": "python",
      "args": ["/路径/paddleocr_mcp.py"]
    }
  }
}
```
</details>

<details>
<summary><b>Hermes Agent</b> 👈 点击展开</summary>

添加到 `~/.hermes/config.yaml`：
```yaml
mcp_servers:
  paddleocr:
    command: python
    args: ["/路径/paddleocr_mcp.py"]
    timeout: 120
    connect_timeout: 120
```

然后重启 Hermes。
</details>

<details>
<summary><b>Cline / Cursor / 其他 MCP 客户端</b> 👈 点击展开</summary>

```json
{
  "mcpServers": {
    "paddleocr": {
      "type": "stdio",
      "command": "python",
      "args": ["/路径/paddleocr_mcp.py"]
    }
  }
}
```
</details>

### 使用示例

向你的 AI Agent 发送：

> 调用 `ocr_image` 识别 `/图片路径/screenshot.png`，然后告诉我图片里写了什么。

**返回结果示例：**
```json
{"text": "Hello World\n你好世界", "lines": ["Hello World", "你好世界"]}
```

## 🔧 本地测试

```bash
# 启动服务
python paddleocr_mcp.py

# 另开终端发送测试请求
echo '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"ocr_image","arguments":{"image_path":"/路径/test.png"}},"id":1}' | python paddleocr_mcp.py
```

## ⚠️ 已知问题

- **Windows + oneDNN**：PaddlePaddle 3.3.1 有 oneDNN 属性转换 bug。使用 3.2.0 或设置 `FLAGS_use_onednn=0`
- **首次运行**：自动下载模型权重（约 50 MB），后续使用缓存

## 📄 许可证

MIT — 随意使用，随意修改。

---

<a id="english"></a>

<div align="center">

# 🌐 English

</div>

# PaddleOCR MCP Server

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server providing local OCR capabilities via [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR). Works with any MCP-compatible AI agent.

## 🚀 Key Advantages

| Feature | PaddleOCR MCP | Cloud OCR APIs |
|---------|---------------|----------------|
| **Cost** | 💰 **Free** | Pay per request |
| **Privacy** | 🔒 **100% local**, data never leaves | Data sent to cloud |
| **Network** | 📡 **Offline**, no internet needed | Internet required |
| **Latency** | ⚡ ~1-3s | ~0.5-3s + network |
| **Languages** | 🌍 109 languages supported | Varies |
| **Model** | 🤖 Works with **DeepSeek-v4**, any LLM | Vendor locked |
| **Open Source** | 📂 **Fully open source** | Closed source |
| **Deployment** | 🖥️ Runs on CPU, low cost | Requires servers |

> 💡 **Low-cost solution with DeepSeek-v4**: PaddleOCR extracts text from images, then pairs with any LLM (DeepSeek-v4, GPT, Claude, GLM, etc.) for understanding — all running locally, zero GPU required, near-zero development cost.

## 🤖 Auto-OCR Mechanism

> **Even if your model doesn't support images (text-only model), the AI Agent will automatically call the `ocr_image` MCP tool to read the image and return the text content.**

How it works:
1. User sends a screenshot
2. AI Agent detects the model can't process images natively
3. Auto-calls `ocr_image` to extract text from the image
4. Analyzes and responds based on the extracted text

This means:
- ✅ **No model switching required** — text-only models can "see" images
- ✅ **Zero extra config** — works automatically once MCP is mounted
- ✅ **Transparent usage** — just send the image, the agent handles the rest

## ✨ Features

- **Pure OCR** — `ocr_image(image_path)` extracts all text from images
- **Chinese + English** — mixed-language recognition out of the box
- **109 languages** — global language coverage
- **Local & offline** — no API keys, no network calls after initial model download
- **Lightweight** — PP-OCRv6 (34.5M params) runs on CPU
- **MCP standard** — compatible with all MCP clients

## 🎯 Use Cases

- 🤖 **DeepSeek-v4, GLM, Qwen** image understanding pipeline
- 📄 Document scanning & screenshot OCR
- 🏭 Industrial: license plates, labels, receipts
- 🌐 Multilingual document processing

## 📦 Quick Start

### Prerequisites

- Python 3.8–3.12
- Node.js 18+ (for client-side tools only, not needed by the server itself)

### Install

```bash
# Install PaddleOCR and PaddlePaddle
pip install paddlepaddle==3.2.0 paddleocr

# Clone this repo
git clone https://github.com/YuanJinke/paddleocr_mcp.git
cd paddleocr_mcp
```

> ⚠️ **Windows users**: PaddlePaddle 3.3.1 has a known oneDNN bug. Pin to **3.2.0** as shown above.

### Configure in your MCP client

<details>
<summary><b>Claude Code</b> 👈 click to expand</summary>

```bash
claude mcp add -s user paddleocr -- python /path/to/paddleocr_mcp.py
```

Or add to `~/.claude.json`:
```json
{
  "mcpServers": {
    "paddleocr": {
      "type": "stdio",
      "command": "python",
      "args": ["/path/to/paddleocr_mcp.py"]
    }
  }
}
```
</details>

<details>
<summary><b>Hermes Agent</b> 👈 click to expand</summary>

Add to `~/.hermes/config.yaml`:
```yaml
mcp_servers:
  paddleocr:
    command: python
    args: ["/path/to/paddleocr_mcp.py"]
    timeout: 120
    connect_timeout: 120
```

Then restart Hermes.
</details>

<details>
<summary><b>Cline / Cursor / Other MCP clients</b> 👈 click to expand</summary>

```json
{
  "mcpServers": {
    "paddleocr": {
      "type": "stdio",
      "command": "python",
      "args": ["/path/to/paddleocr_mcp.py"]
    }
  }
}
```
</details>

### Usage Example

Send to your AI agent:

> Call `ocr_image` on `/path/to/screenshot.png" and tell me what it says.

**Example result:**
```json
{"text": "Hello World\n你好世界", "lines": ["Hello World", "你好世界"]}
```

## 🔧 Local Test

```bash
# Start server
python paddleocr_mcp.py

# Send test request
echo '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"ocr_image","arguments":{"image_path":"/path/to/test.png"}},"id":1}' | python paddleocr_mcp.py
```

## ⚠️ Known Issues

- **Windows + oneDNN**: PaddlePaddle 3.3.1 has a oneDNN attribute conversion bug. Use 3.2.0 or set `FLAGS_use_onednn=0`.
- **First run**: Model weights (~50 MB) auto-downloaded on first use. Subsequent runs use cache.

## 📄 License

MIT — free to use, modify, and distribute.
