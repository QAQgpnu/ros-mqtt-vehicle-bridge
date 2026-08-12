# Changelog

All notable changes to this project are documented here.

## [Unreleased]

- Add issue templates, pull-request review checklist, and release-note categorization.

## [0.2.0] - 2026-08-12

### Added

- Add a dependency-free offline demo that shows both ROS-to-MQTT and MQTT-to-ROS directions.
- Add a checked-in architecture SVG and asciinema-compatible terminal recording for quick visual verification.
- Reject malformed and non-object JSON in the offline demo before it is shown as a valid message.

### Notes

- The offline demo is a contract walkthrough; native ROS/Paho validation still requires the environment described below.

## [0.1.0] - 2026-08-12

### Added

- Bidirectional ROS 1 `std_msgs/String` and MQTT JSON bridge.
- Configurable broker URI, topics, client ID, QoS, and environment-based credentials.
- Local Mosquitto Compose setup, examples, architecture notes, and offline repository tests.
- MIT license, security policy, contribution guide, and GitHub Actions quality workflow.

### Notes

- Native ROS/Paho compilation still requires an Ubuntu/ROS Noetic environment.
- This release intentionally excludes private message packages, customer endpoints, credentials, and build artifacts.

