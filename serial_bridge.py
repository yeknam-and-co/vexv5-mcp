import sys
import time

import serial
from serial.tools import list_ports


def find_vex_port():
    ports = [
        p for p in list_ports.comports()
        if p.vid == 0x2888 and p.pid == 0x0501
    ]

    if not ports:
        return None

    if sys.platform == "win32":
        user_matches = []

        for p in ports:
            text = (
                f"{p.description or ''} "
                f"{p.interface or ''} "
                f"{p.hwid or ''}"
            ).lower()

            if "user" in text:
                user_matches.append(p)

        if len(user_matches) == 1:
            return user_matches[0].device

        detailed_matches = []

        for p in ports:
            location = (p.location or "").lower()
            hwid = (p.hwid or "").lower()

            if ":x." in location or ":x." in hwid:
                detailed_matches.append(p)

        if len(detailed_matches) == 1:
            return detailed_matches[0].device

        devices = {
            p.device.upper(): p
            for p in ports
        }

        if "COM3" in devices:
            return "COM3"

        if len(ports) == 1:
            return ports[0].device

        return None

    elif sys.platform == "darwin":
        matches = [
            p for p in ports
            if p.device.startswith("/dev/cu.")
            and p.device.endswith("103")
        ]

        if len(matches) == 1:
            return matches[0].device

        if len(ports) == 1:
            return ports[0].device

        return None

    else:
        if len(ports) == 1:
            return ports[0].device

        return None


def send_to_brain(message, read_timeout=2.0, port=None):
    port = port or find_vex_port()

    if not port:
        raise RuntimeError(
            "Could not find a VEX V5 Brain serial port."
        )

    with serial.Serial(
        port=port,
        baudrate=115200,
        timeout=0.1,
        write_timeout=2
    ) as connection:
        connection.reset_input_buffer()
        connection.reset_output_buffer()

        payload = f"{message}\n".encode("utf-8")

        connection.write(payload)
        connection.flush()

        lines = []
        deadline = time.monotonic() + read_timeout

        while time.monotonic() < deadline:
            line = connection.readline()

            if line:
                lines.append(
                    line.decode(
                        "utf-8",
                        errors="replace"
                    ).rstrip("\r\n")
                )

        return "\n".join(lines)