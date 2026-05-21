from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from mcp.server.fastmcp import FastMCP

app = FastAPI()

mcp = FastMCP("hello-world-app")


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


# IMPORTANT
mcp_app = mcp.streamable_http_app()

# mount WITHOUT trailing slash problems
app.mount("/mcp-server", mcp_app)