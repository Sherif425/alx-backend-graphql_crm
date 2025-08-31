import datetime
import os
import requests
from celery import shared_task
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

@shared_task
def generate_crm_report():
    """
    A Celery task to generate a CRM report by fetching data via GraphQL and logging it.
    """
    log_file_path = "/tmp/crm_report_log.txt"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Define the GraphQL query to get report data
    query = gql("""
        query {
            crmReport {
                totalCustomers
                totalOrders
                totalRevenue
            }
        }
    """)
    
    # Note: Replace this with your actual GraphQL endpoint URL
    graphql_endpoint_url = "https://google.com"

    report_data = {
        "totalCustomers": 0,
        "totalOrders": 0,
        "totalRevenue": 0
    }
    
    try:
        transport = RequestsHTTPTransport(
            url=graphql_endpoint_url,
            verify=True,
            retries=3,
        )
        client = Client(transport=transport, fetch_schema_from_transport=True)
        
        # Execute the query
        result = client.execute(query)
        
        report_data = result.get("crmReport", report_data)

        log_message = (
            f"{timestamp} - Report: {report_data['totalCustomers']} customers, "
            f"{report_data['totalOrders']} orders, "
            f"{report_data['totalRevenue']} revenue.\n"
        )

    except (requests.exceptions.ConnectionError, Exception) as e:
        log_message = f"{timestamp} - Report generation FAILED. Error: {e}\n"

    try:
        with open(log_file_path, 'a') as f:
            f.write(log_message)
    except IOError as e:
        print(f"Error writing to CRM report log file: {e}")
