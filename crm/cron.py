import datetime
import os
import requests
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def log_crm_heartbeat():
    """
    Logs a heartbeat message to a file to confirm the CRM application's health.
    This function also queries a GraphQL endpoint to verify its responsiveness.
    """
    log_file_path = "/tmp/crm_heartbeat_log.txt"
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")

    graphql_status = "GraphQL endpoint is NOT responsive."

    # Define the GraphQL query
    query = gql("""
        query {
            hello
        }
    """)

    # Note: Replace this with your actual GraphQL endpoint URL.
    graphql_endpoint_url = "https://google.com" 

    try:
        # Create a GraphQL client to execute the query
        transport = RequestsHTTPTransport(
            url=graphql_endpoint_url,
            verify=True,
            retries=3,
        )
        client = Client(transport=transport, fetch_schema_from_transport=True)

        # Execute the query
        result = client.execute(query)

        # Check the result of the query
        if result.get("hello") == "Hello, world!":
            graphql_status = "GraphQL endpoint is responsive."

    except (requests.exceptions.ConnectionError, Exception) as e:
        graphql_status = f"GraphQL endpoint is NOT responsive. Error: {e}"

    message = f"{timestamp} CRM is alive. Status: {graphql_status}\n"

    try:
        # Open the file in append mode to avoid overwriting existing logs
        with open(log_file_path, 'a') as f:
            f.write(message)
    except IOError as e:
        # Log an error if the file cannot be written
        print(f"Error writing to heartbeat log file: {e}")