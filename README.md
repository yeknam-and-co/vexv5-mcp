# VEX BRAIN MCP

Control a VEX V5 robot through an AI assistant using **MCP** and **pySerial**.

Code is sent over USB, executed on the Brain, and printed output is returned to the assistant.

## Setup

```bash
python -m pip install fastmcp pyserial
```

1. Upload and run `brain.py` through VEXcode.
2. Connect the Brain over USB and close any serial monitors.
3. Configure your MCP client to launch `robot_server.py` using Python over **stdio**.

Default for Claude Desktop
```json
  "mcpServers": {
    "robot": {
      "command": "/Users/ian/heyzack/venv/bin/python",
      "args": [
        "/Users/ian/heyzack/server.py"
      ]
    }
  },```


The default robot configuration uses an **18:1 motor on port 1**.

## Files

- `brain.py` — receives and executes Python on the robot.
- `serial_bridge.py` — handles USB communication and port detection.
- `robot_server.py` — exposes the `run_python` MCP tool.

## Usage

Ask your assistant to print text, read sensors, or control configured motors.

```python
brain.screen.print("Hello from MCP!")
print("Done")
```

Port detection supports macOS naming patterns and Windows VEX User Port labels.# vexv5-mcp
