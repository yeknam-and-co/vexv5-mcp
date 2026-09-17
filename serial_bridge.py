import argparse
import sys
import time

import serial
from serial.tools import list_ports

def find_vex_port():
    ports = [
        p for p in list_ports.comports()
        if p.vid == 0x2888 and p.pid == 0x0501
    ]

    if sys.platform == "darwin":
        matches = [
            p for p in ports
            if p.device.startswith("/dev/cu.")
            and p.device.endswith("103")
        ]
    elif sys.platform == "win32":
        matches = [
            p for p in ports
            if "user" in
            f"{p.description} {p.interface or ''}".lower()
        ]
    else:
        matches = []

    if len(matches) == 1:
        return matches[0].device

    if len(ports) == 1:
        return ports[0].device

def send_to_brain(message, read_timeout=2.0, port=None):
    port = port or find_vex_port()

    with serial.Serial(
        port, 115200, timeout=0.1, write_timeout=2
    ) as connection:
        connection.reset_input_buffer()
        connection.write(f"{message}\n".encode("utf-8"))
        connection.flush()

        lines = []
        deadline = time.monotonic() + read_timeout

        while time.monotonic() < deadline:
            line = connection.readline()
            if line:
                lines.append(
                    line.decode("utf-8", errors="replace").rstrip("\r\n")
                )

        return "\n".join(lines)