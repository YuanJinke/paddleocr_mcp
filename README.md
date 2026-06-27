# PaddleOCR MCP Server

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server that provides OCR (Optical Character Recognition) capabilities via [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR). Works with any MCP-compatible AI agent — Claude Code, Cline, Hermes Agent, OpenCode, and more.

## Features

- **Single tool, focused job** — `ocr_image(image_path)` extracts text from images
- **Chinese + English** — mixed-language recognition out of the box
- **100+ languages** — PaddleOCR supports 109 languages
- **Local & offline** — no API keys, no network calls after initial model download
- **Fast** — lightweight PP-OCRv6 models run on CPU

## Quick Start

### Prerequisites

- Python 3.8–3.12
- Node.js 18+ (for MCP client-side tools like Claude Code, but **not** required by this server itself)

### Install

```bash
# Install PaddleOCR and PaddlePaddle
pip install paddlepaddle==3.2.0 paddleocr

# Clone or download this repo
git clone https://github.com/YOUR_USER/paddleocr-mcp.git
cd paddleocr-mcp
```

> **Windows users**: PaddlePaddle 3.3.1 has a known oneDNN bug. Pin to **3.2.0** as shown above.

### Configure in your MCP client

<details>
<summary><b>Claude Code</b></summary>

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
<summary><b>Hermes Agent</b></summary>

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
<summary><b>Cline (VS Code)</b></summary>

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
<summary><b>Generic (other MCP clients)</b></summary>

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

### Usage

Send a prompt like this to your AI agent:

> "ocr_image" on `/path/to/screenshot.png"
> What does this image say?

The agent will call the `ocr_image` tool and return the recognised text.

**Example result:**
```json
{"text": "Hello World\n你好世界", "lines": ["Hello World", "你好世界"]}
```

## Development

### Test locally

```bash
# Start the server (it waits for JSON-RPC on stdin)
python paddleocr_mcp.py

# In another terminal, send a test request
echo '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"ocr_image","arguments":{"image_path":"/path/to/test.png"}},"id":1}' | python paddleocr_mcp.py
```

## Why PaddleOCR?

| Feature | PaddleOCR | Cloud OCR APIs |
|---------|-----------|----------------|
| Cost | Free | Pay per request |
| Privacy | 100% local | Data sent to cloud |
| Latency | ~1-3s | ~0.5-3s + network |
| Internet | Not required | Required |
| Languages | 109 | Varies |

## Known Issues

- **Windows + oneDNN**: PaddlePaddle 3.3.1 has a bug with oneDNN attribute conversion. Pin to 3.2.0 or set `FLAGS_use_onednn=0`.
- **First run**: Model weights (~50 MB) are downloaded automatically on first use. Subsequent runs use cached files.

## License

MIT — do whatever you want with it.
