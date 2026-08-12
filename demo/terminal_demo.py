#!/usr/bin/env python3
"""Dependency-free, offline walkthrough of the public ROS/MQTT contract."""

from __future__ import annotations

import argparse
import json
import time
from dataclasses import dataclass
from typing import Callable


ROS_TASK_TOPIC = "/vehicle/task_cmd_json"
MQTT_TASK_TOPIC = "vehicle/task_cmd"
MQTT_COMMAND_TOPIC = "vehicle/mqtt_cmd"
ROS_COMMAND_TOPIC = "/vehicle/mqtt_cmd_json"


def parse_object(payload: str) -> dict[str, object]:
    """Parse one public payload and reject malformed/non-object JSON."""

    try:
        value = json.loads(payload)
    except json.JSONDecodeError as error:
        raise ValueError(f"invalid JSON: {error.msg}") from error
    if not isinstance(value, dict):
        raise ValueError("payload must be a JSON object")
    return value


@dataclass
class DemoBridge:
    emit: Callable[[str], None]

    def ros_to_mqtt(self, payload: str) -> None:
        message = parse_object(payload)
        self.emit(f"ROS publish  {ROS_TASK_TOPIC}  {self._compact(message)}")
        self.emit(f"Bridge       -> MQTT {MQTT_TASK_TOPIC}")
        self.emit(f"MQTT broker  received {self._compact(message)}")

    def mqtt_to_ros(self, payload: str) -> None:
        message = parse_object(payload)
        self.emit(f"MQTT publish {MQTT_COMMAND_TOPIC}  {self._compact(message)}")
        self.emit(f"Bridge       -> ROS {ROS_COMMAND_TOPIC}")
        self.emit(f"ROS consumer received {self._compact(message)}")

    @staticmethod
    def _compact(message: dict[str, object]) -> str:
        return json.dumps(message, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def run_demo(delay: float = 0.0, emit: Callable[[str], None] = print) -> None:
    """Run the two-way message walkthrough without ROS, MQTT, Docker, or credentials."""

    emit("ROS-MQTT Vehicle Bridge :: offline contract demo")
    emit("This simulates the public topics; it does not connect to a broker.")
    bridge = DemoBridge(emit)
    bridge.ros_to_mqtt(
        json.dumps(
            {"task_id": "demo-0001", "action": "move", "target": {"x": 1.2, "y": 3.4}},
            ensure_ascii=False,
        )
    )
    if delay:
        time.sleep(delay)
    bridge.mqtt_to_ros(json.dumps({"command": "pause", "reason": "operator_request"}))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--delay", type=float, default=0.0, help="seconds between directions")
    args = parser.parse_args()
    if args.delay < 0:
        parser.error("--delay must be non-negative")
    run_demo(args.delay)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

