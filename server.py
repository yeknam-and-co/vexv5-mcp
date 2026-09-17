from threading import Lock

from fastmcp import FastMCP
from serial_bridge import send_to_brain

mcp = FastMCP("bobot server")
serial_lock = Lock()

RESERVED_LINES = {
    "__BEGIN_CODE__",
    "__END_CODE__",
    "stop",
}


@mcp.tool(
    name="run_python",
    description=(
        "Execute Python code on the connected VEX V5 Brain using "
        "its running command receiver. Existing robot globals, such as "
        "brain and configured motors, are available. "
        "Use print(...) to return values, readings, or confirmation. "
        "brain.screen.print(...) displays text on the robot's screen. "
        "Send complete, correctly indented code blocks. "
        "Code may physically move the robot. "
        "An empty response does not prove execution failed; "
        "do not automatically retry movement commands. "
        "read_timeout controls how long to collect output, "
        "not how long the robot may execute."
    ),
)
def run_python(code: str, read_timeout: float = 2.0) -> str:
    """Execute code and return captured serial output."""
    if not 0 < read_timeout <= 60:
        raise ValueError("read_timeout must be greater than 0 and at most 60.")

    code = code.replace("\r\n", "\n").replace("\r", "\n")

    if not code.strip():
        raise ValueError("Code cannot be empty.")

    if any(line.strip() in RESERVED_LINES for line in code.split("\n")):
        raise ValueError("Code contains a reserved protocol line.")

    message = f"__BEGIN_CODE__\n{code}\n__END_CODE__"

    with serial_lock:
        return send_to_brain(message, read_timeout=read_timeout)


if __name__ == "__main__":
    mcp.run(transport="stdio")