import datetime

def run_post_shutdown_tasks(server):
    # Find the maximum message count among clients
    max_message_count = max(server.message_counts.values(), default=0)

    # Find clients with the maximum message count
    most_active_clients = [addr for addr, count in server.message_counts.items() if count == max_message_count]
  
    if most_active_clients:
        print("Most active client:")
        for addr in most_active_clients:
            most_active_client_name = server.get_client_name(addr)
            print(f"- {most_active_client_name}: Number of messages: {max_message_count}")
    else:
        print("No active clients.")

    # Find and print the longest messages sent by clients.
    server.find_longest_messages()

    # Define a start and end time for the time frame
    start_time = datetime.datetime.strptime("2023-08-24 19:4:00", '%Y-%m-%d %H:%M:%S')
    end_time = datetime.datetime.strptime("2023-08-24 19:5:00", '%Y-%m-%d %H:%M:%S')
    
    # Print messages sent within the specified time frame
    server.print_messages_in_time_frame(start_time, end_time)
   