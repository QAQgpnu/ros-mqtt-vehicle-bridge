# Offline visual demo

This demo makes the public message contract visible without requiring ROS, an MQTT broker, Docker, or credentials.

```bash
python demo/terminal_demo.py --delay 0.2
```

It walks through both directions:

```text
ROS /vehicle/task_cmd_json -> bridge -> MQTT vehicle/task_cmd
MQTT vehicle/mqtt_cmd     -> bridge -> ROS /vehicle/mqtt_cmd_json
```

The simulator validates that each example is a JSON object. It is intentionally not a replacement for the native ROS/Paho build; use the [quick start](../README.md#快速开始) for that path.

The checked-in [`terminal-demo.cast`](terminal-demo.cast) is an asciinema-compatible recording of the same deterministic flow.

