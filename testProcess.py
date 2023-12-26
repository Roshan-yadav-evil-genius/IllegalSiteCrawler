import time
from datetime import datetime, timedelta

# Record the start time
start_time = datetime.now()

while True:
    # Get the current time and format it with AM/PM
    current_time = datetime.now()
    formatted_current_time = current_time.strftime("%I:%M:%S %p")

    # Calculate the current uptime
    uptime = current_time - start_time
    formatted_uptime = str(timedelta(seconds=int(uptime.total_seconds())))

    # Print the current time and uptime
    print(f"Current Time: {formatted_current_time} | Uptime: {formatted_uptime}")

    # Wait for 1 second
    time.sleep(1)
