# Architecture

The bridge deliberately treats JSON as the public boundary between ROS and MQTT.

## Data flow

1. A ROS producer publishes a JSON string to `/vehicle/task_cmd_json`.
2. The bridge forwards the unchanged payload to `vehicle/task_cmd` on MQTT.
3. A cloud service or dispatcher publishes JSON to `vehicle/mqtt_cmd`.
4. The bridge forwards the unchanged payload to `/vehicle/mqtt_cmd_json`.

The bridge does not own a business schema. Applications can version and validate their own payloads without coupling the transport package to proprietary ROS messages.

## Why credentials are environment variables

Launch files and YAML files are commonly committed to Git. Reading `MQTT_USERNAME` and `MQTT_PASSWORD` from the process environment prevents the default configuration from encouraging embedded credentials. Production deployments should use a service manager or secret store to inject these variables.

## Custom message adapter

For a custom ROS message such as `TaskCmd`, add a separate adapter node:

```text
TaskCmd -> task_cmd_adapter -> JSON String -> bridge -> MQTT
MQTT -> bridge -> JSON String -> mqtt_cmd_adapter -> InternalCommand
```

This keeps proprietary definitions outside the reusable transport layer.
