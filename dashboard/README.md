# Dashboard

This folder should contain all code, documentation, and resources required for the dashboard.

## Setup

1. CD into this directory using `cd dashboard`.

2. Install the required dependencies using `pip install -r requirements.txt`.

3. Set up the environment variables by creating a `.env` file with the necessary configuration.

4. Run the consumer script using `python pipeline.py`.

## CLI args

- `python -w INFO|WARNING|ERROR|DEBUG`: Set the warning level for the logger.
- `python -d`: Disable logging into the commmand-line (will still log into the file).

### Details

- The consumer subscribes to the 'lmnh' topic and continuously polls for new messages.
- Log messages are logged into the `kiosk_logs.log` file. This file only stores the last 1MB of logs.
- The 'at' field is automatically added to messages if it is missing, using the current timestamp.
- The consumer uses the `validate` function to ensure that each message meets the required schema and value constraints.
- The consumer will continue running indefinitely, polling for new messages until manually stopped.

## Tableau

- The dashboard is built using Tableau and visualises the kiosk data.
- It can be viewed through Tableau Desktop by opening the 'c26-aloysius-lmnh.twbx' file.