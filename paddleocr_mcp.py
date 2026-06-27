#!/usr/bin/env python3
"""
PaddleOCR MCP Server — 本地 OCR 识别服务

A Model Context Protocol (MCP) server that provides OCR capabilities
via PaddleOCR. Designed for use with MCP-compatible AI agents
(Claude Code, Cline, Hermes Agent, etc.).

Provides one tool:
  - ocr_image(image_path) → recognizes text from image files

Installation:
  pip install paddlepaddle==3.2.0 paddleocr

Usage (in MCP config):
  {
    "mcpServers": {
      "paddleocr": {
        "type": "stdio",
        "command": "python",
        "args": ["path/to/paddleocr_mcp.py"]
      }
    }
  }
"""

from __future__ import annotations

import json
import logging
import os
import sys
from typing import Any

# ── Silence Paddle's noisy C++ logs ──────────────────────────────────
os.environ.setdefault("GLOG_minloglevel", "3")
os.environ.setdefault("FLAGS_use_onednn", "1")
os.environ.setdefault("PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK", "True")
os.environ.setdefault("PADDLE_DISABLE_INIT_LOG", "1")

logging.basicConfig(level=logging.CRITICAL)
for name in ("paddle", "paddlex", "paddleocr", "ppocr"):
    logging.getLogger(name).setLevel(logging.CRITICAL)

# Paddle's C/C++ backend writes GBK (Windows) / non-UTF-8 bytes to
# stderr during model init, which corrupts the MCP stdio transport.
# Redirect stderr to null until model is loaded.
_stderr_devnull = open(os.devnull, "w")
_stderr_saved = sys.stderr
sys.stderr = _stderr_devnull

# ── Lazy-loaded OCR engine ───────────────────────────────────────────
_OCR: Any = None


def get_ocr() -> Any:
    global _OCR
    if _OCR is None:
        from paddleocr import PaddleOCR

        _OCR = PaddleOCR(lang="ch")

        # Restore stderr after model loading
        sys.stderr.flush()
        sys.stderr = _stderr_saved
        _stderr_devnull.close()
    return _OCR


# ── Tool implementation ──────────────────────────────────────────────

def ocr_image(image_path: str) -> dict[str, Any]:
    """Recognise text from an image file.

    Args:
        image_path: Absolute or relative path to the image file.

    Returns:
        dict with keys:
          - "text":    All recognised text joined by newlines.
          - "lines":   List of individual recognised text lines.
          - "error":   Present only on failure.
    """
    if not os.path.isfile(image_path):
        return {"error": f"File not found: {image_path}"}
    try:
        ocr = get_ocr()
        results = list(ocr.predict(image_path))
        texts: list[str] = []
        for res in results:
            for t in res.get("rec_texts", []):
                texts.append(t)
        if not texts:
            return {"text": "", "message": "No text detected"}
        return {"text": "\n".join(texts), "lines": texts}
    except Exception as e:
        return {"error": f"OCR failed: {e}"}


# ── MCP JSON-RPC message dispatcher ──────────────────────────────────

def handle_message(msg: dict[str, Any]) -> dict[str, Any] | None:
    method = msg.get("method", "")
    msg_id = msg.get("id")

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "paddleocr-mcp", "version": "1.0.0"},
            },
        }

    if method == "notifications/initialized":
        return None  # no response expected

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "tools": [
                    {
                        "name": "ocr_image",
                        "description": (
                            "Use PaddleOCR to perform optical character recognition (OCR) "
                            "on an image and return all detected text. Supports mixed "
                            "Chinese and English recognition."
                        ),
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "image_path": {
                                    "type": "string",
                                    "description": "Absolute local path to the image file",
                                }
                            },
                            "required": ["image_path"],
                        },
                    }
                ]
            },
        }

    if method == "tools/call":
        params = msg.get("params", {})
        tool_name = params.get("name", "")
        args = params.get("arguments", {})

        if tool_name == "ocr_image":
            result = ocr_image(args.get("image_path", ""))
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "content": [
                        {"type": "text", "text": json.dumps(result, ensure_ascii=False)}
                    ]
                },
            }

        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "error": {"code": -32601, "message": f"Unknown tool: {tool_name}"},
        }

    if method == "ping":
        return {"jsonrpc": "2.0", "id": msg_id, "result": {}}

    return {
        "jsonrpc": "2.0",
        "id": msg_id,
        "error": {"code": -32601, "message": f"Unknown method: {method}"},
    }


# ── Entry point ──────────────────────────────────────────────────────

def main() -> None:
    # Warm up model (first load downloads weights)
    get_ocr()

    for raw in sys.stdin:
        line = raw.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
            resp = handle_message(msg)
            if resp is not None:
                sys.stdout.write(json.dumps(resp, ensure_ascii=False) + "\n")
                sys.stdout.flush()
        except json.JSONDecodeError:
            continue
        except Exception as exc:
            # Can't write to stderr (it's null after model load on Windows),
            # silently skip.
            pass


if __name__ == "__main__":
    main()
