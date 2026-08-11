# Contributing

Thank you for helping improve the bridge.

1. Open an issue describing the use case or bug.
2. Keep transport logic independent from proprietary ROS message packages.
3. Never commit broker credentials, customer endpoints, vehicle identifiers, or production payloads.
4. Run `python -m unittest discover -s tests -v` before opening a pull request.
5. Keep each pull request focused and document how the change was tested.
