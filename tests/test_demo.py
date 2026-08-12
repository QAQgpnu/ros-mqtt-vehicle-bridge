import contextlib
import io
import json
import pathlib
import sys
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "demo"))

from terminal_demo import DemoBridge, ROS_COMMAND_TOPIC, ROS_TASK_TOPIC, run_demo


class OfflineDemoTests(unittest.TestCase):
    def test_demo_shows_both_directions(self):
        output = io.StringIO()
        run_demo(emit=lambda line: output.write(line + "\n"))
        rendered = output.getvalue()
        self.assertIn(ROS_TASK_TOPIC, rendered)
        self.assertIn(ROS_COMMAND_TOPIC, rendered)
        self.assertIn("vehicle/task_cmd", rendered)
        self.assertIn("vehicle/mqtt_cmd", rendered)

    def test_malformed_or_non_object_json_is_rejected(self):
        bridge = DemoBridge(lambda _line: None)
        with self.assertRaises(ValueError):
            bridge.ros_to_mqtt("not-json")
        with self.assertRaises(ValueError):
            bridge.mqtt_to_ros(json.dumps(["not", "an", "object"]))

    def test_visual_assets_are_present(self):
        self.assertTrue((ROOT / "docs" / "architecture.svg").is_file())
        self.assertTrue((ROOT / "demo" / "terminal-demo.cast").is_file())


if __name__ == "__main__":
    unittest.main()

