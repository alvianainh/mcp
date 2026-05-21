import os

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from mcp.server.fastmcp import FastMCP

BASE_URL = os.getenv(
    "BASE_URL",
    "mcp-production-ec83.up.railway.app"
)

mcp = FastMCP("hello-world-app")


@mcp.tool()
def greet_user(name: str) -> str:
    return f"Hello {name}"

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from mcp.server.fastmcp import FastMCP

app = FastAPI()

mcp = FastMCP("hello-world-app")


@mcp.tool()
def greet_user(name: str) -> dict:
    return {
        "content": [
            {
                "type": "text",
                "text": f"Hello {name}"
            }
        ],
        "_meta": {
            "openai/outputTemplate": "https://mcp-production-ec83.up.railway.app/widget/hello"
        }
    }


@app.get("/")
async def root():
    return {"status": "ok"}


@app.get("/widget/hello")
async def hello_widget():
    return HTMLResponse("""
    <html>
      <body style="font-family:sans-serif;padding:20px;">
        <h1>Hello Widget</h1>
        <p>Connected successfully.</p>
      </body>
    </html>
    """)


# MCP endpoint
app.mount("/mcp", mcp.streamable_http_app())
app = FastAPI()


@app.get("/")
async def root():
    return {"status": "ok"}


@app.get("/widget/hello")
async def hello_widget():
    return HTMLResponse(f"""
    <html>
      <body style="font-family:sans-serif;padding:20px;">
        <h1>Hello Widget</h1>
        <p>Connected successfully.</p>
        <p>Base URL: {BASE_URL}</p>
      </body>
    </html>
    """)


# IMPORTANT
app.mount("/", mcp.streamable_http_app())