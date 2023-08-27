import os
import datetime

# Read and return the longest messages from client files
def find_longest_message():
    longest_message = ""
    longest_client_name = ""
    for file_name in os.listdir("."):
        if file_name.startswith("client_") and file_name.endswith(".txt"):
            with open(file_name, "r") as file:
                lines = file.readlines()

                # Find the longest message
                for line in lines:
                    if len(line) > len(longest_message):
                        longest_message = line
                        longest_client_name = file_name.split("_")[1]
    return longest_message.strip(), longest_client_name.strip()

# Read and return the most active client based on message counts
def find_most_active_client():
    most_active_client = ""
    most_messages_count = 0

    for file_name in os.listdir("."):
        if file_name.startswith("client_") and file_name.endswith(".txt"):
            with open(file_name, "r") as file:
                lines = file.readlines()
                message_count = len(lines)
                client_name = file_name.split("_")[1]

                # Compare the current message_count with most_messages_count
                if message_count > most_messages_count:
                    most_messages_count = message_count
                    most_active_client = client_name

    return most_active_client


# Read and return messages sent within the specified time frame
def read_messages_in_time_frame(start_time, end_time):
    all_messages = []

    for file_name in os.listdir("."):
        if file_name.startswith("client_") and file_name.endswith(".txt"):
            with open(file_name, "r") as file:
                lines = file.readlines()
                for line in lines:
                    timestamp_str = line.split("[")[1].split("]")[0]
                    timestamp = datetime.datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
                    if start_time <= timestamp <= end_time:
                        all_messages.append(line.strip())

    return all_messages
