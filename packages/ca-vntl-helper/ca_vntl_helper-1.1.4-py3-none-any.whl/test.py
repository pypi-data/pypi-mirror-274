from ca_vntl_helper import ErrorTrackerWithCallBacks
from datetime import datetime, timedelta
import requests

def notify_to_slack(message, slack_token=None):
    url = f"https://hooks.slack.com/services/{slack_token}"
    data = {
        "text": message
    }
    response = requests.post(url, json=data)
    assert response.status_code == 200
    return response.status_code

def send_message_to_slack(message):
    # Your code here
    webhook_token = "T05BWS1D421/B073MC4RPCM/GGdZnWbwBH1FgUBQjOjBhxAg"
    notify_to_slack(message, slack_token=webhook_token)

def save_message_to_logfile_on_s3(message):
    print("Message saved to logfile on S3:")
    print(message)

error_tracker = ErrorTrackerWithCallBacks(callback_functions=[send_message_to_slack, save_message_to_logfile_on_s3])

error_tracking_decorator_with_callbacks = error_tracker.error_tracking_decorator

def divide(a, b):
    current_time = datetime.now() - timedelta(10)
    try:
        c = a / b
    except Exception as e:
        raise Exception(f"Error when dividing {a} by {b}")
    return None



def second_inner_function(second_inner_a, second_inner_b):
    return divide(second_inner_a, second_inner_b)


def first_inner_function(first_inner_a, first_inner_b):
    return second_inner_function(first_inner_a, first_inner_b)


@error_tracking_decorator_with_callbacks  # Just place the decorator here
def outer_function(outer_a, outer_b):
    return first_inner_function(outer_a, outer_b)


if __name__ == "__main__":
    # The process will get an error when dividing by 0
    try:
        outer_function(1, 0)
        print("Process completed successfully")
    except Exception as e:
        print("Process failed")
        print(e)