import os

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from mcp.server.fastmcp import FastMCP

app = FastAPI()

mcp = FastMCP("hello-world-app")


BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")


@mcp.tool()
def greet_user(name: str) -> dict:
    """
    Greet a user.
    """

    return {
        "content": [
            {
                "type": "text",
                "text": f"Hello {name}"
            }
        ],
        "structuredContent": {
            "message": f"Hello {name}"
        },
        "_meta": {
            "openai/outputTemplate": f"{BASE_URL}/widget/hello"
        }
    }


@app.get("/")
async def root():
    return {"status": "ok"}


@app.get("/widget/hello")
async def hello_widget():
    html = """
    <html>
    <body style="font-family:sans-serif;padding:20px;">
        <h1>Hello Widget</h1>
        <p>This UI comes from your MCP app.</p>
    </body>
    </html>
    """
    return HTMLResponse(html)


app.mount("/mcp", mcp.streamable_http_app())