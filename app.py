from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("hello-world-app")

app = FastAPI()


@mcp.tool()
def greet_user(name: str) -> str:
    return f"Hello {name}"


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


# IMPORTANT:
# mount MCP app DIRECTLY
mcp_http_app = mcp.streamable_http_app()

app.mount("/mcp", mcp_http_app)