import requests

def get_routing_info_from_api(customer_id):
    """
    Simulates a CVP Call Studio script making a REST API call to an
    external web service to get call routing information.

    Args:
        customer_id (str): The customer's ID, which would be passed
                           from the UCCE ICM script to CVP.

    Returns:
        dict: A dictionary containing the routing information (priority and
              skill group) returned from the API. Returns None if the
              request fails.
    """
    api_url = "http://localhost:5000/get_customer_priority"
    params = {"customer_id": customer_id}

    print(f"--- Simulating UCCE/CVP ---")
    print(f"Making request to API for customer: {customer_id}")

    try:
        response = requests.get(api_url, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            routing_data = response.json()
            print("API Response Received:")
            print(f"  Priority: {routing_data.get('priority')}")
            print(f"  Skill Group: {routing_data.get('skill_group')}")
            print("--- Simulation End ---\n")
            return routing_data
        else:
            print(f"Error: API returned status code {response.status_code}")
            print(f"Response: {response.text}")
            print("--- Simulation End ---\n")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error: Could not connect to the API.")
        print(f"Details: {e}")
        print("--- Simulation End ---\n")
        return None

if __name__ == "__main__":
    # The Flask application (`app.py`) must be running for this to work.

    # --- Scenario 1: A VIP Customer Calls ---
    # In UCCE, the script would get the customer ID (e.g., from a CRM lookup)
    # and pass it to CVP. CVP calls the API and gets back priority 1.
    vip_customer_id = "VIP86753"
    routing_decision = get_routing_info_from_api(vip_customer_id)
    if routing_decision:
        # The UCCE script would now use these variables to route the call
        # to the high-priority queue.
        print(f"UCCE Action: Routing call for {vip_customer_id} to {routing_decision['skill_group']}.\n\n")


    # --- Scenario 2: A Standard Customer Calls ---
    # UCCE gets a different customer ID and passes it to CVP.
    # CVP calls the API and gets back priority 5.
    standard_customer_id = "CUST1138"
    routing_decision = get_routing_info_from_api(standard_customer_id)
    if routing_decision:
        # The UCCE script routes this call to the standard queue.
        print(f"UCCE Action: Routing call for {standard_customer_id} to {routing_decision['skill_group']}.\n\n")

    # --- Scenario 3: API is down or customer_id is missing ---
    # This demonstrates error handling.
    get_routing_info_from_api(None)