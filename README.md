# Python Integration for Cisco UCCE Scripts

This project demonstrates a common pattern for integrating external logic, written in Python, with a Cisco UCCE (Unified Contact Center Enterprise) call flow.

## The Problem

Cisco UCCE scripting is primarily done in a graphical tool called ICM Script Editor. While powerful for call routing, it is not designed for complex business logic, database interactions, or integrations with other enterprise systems. The user wanted to know how to "automate UCCE scripts with Python."

Directly generating or manipulating UCCE's proprietary script files (`.icm`) with Python is not a supported or practical approach. The standard industry practice is to have the UCCE script call an external web service (a REST API) to perform these complex tasks.

## The Solution

This project provides a complete, runnable simulation of this client-server pattern. It consists of two main components:

1.  **`app.py` (The REST API Server):** A simple Flask web application that acts as the external service. It exposes an API endpoint that takes a `customer_id` and returns a JSON object with a calculated `priority` and a recommended `skill_group`. In a real-world scenario, this service would contain your complex business logic.

2.  **`ucce_caller_simulation.py` (The UCCE/CVP Client):** A Python script that simulates the role of a UCCE/CVP script. It calls the Flask API to fetch the routing information and then prints the "decision" it would make based on the response. This demonstrates the client side of the interaction.

### How it Works

1.  The `app.py` server is running.
2.  The `ucce_caller_simulation.py` script is executed.
3.  The simulation script makes an HTTP `GET` request to the server, passing a `customer_id`.
4.  The server processes the request, applies its logic, and returns a JSON response.
5.  The simulation script receives the response and prints the routing action that a real UCCE script would take.

## How to Run the Demonstration

### Step 1: Install Dependencies

First, install the necessary Python libraries from the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### Step 2: Start the API Server

In your first terminal window, start the Flask web server.

```bash
python app.py
```

You should see output indicating that the server is running on `http://127.0.0.1:5000`. Leave this terminal open.

### Step 3: Run the UCCE Client Simulation

In a second terminal window, run the client simulation script. This script will make calls to the server you started in the previous step.

```bash
python ucce_caller_simulation.py
```

### Expected Output

When you run the client simulation, you will see the following output, demonstrating the full, end-to-end interaction for different scenarios:

```
--- Simulating UCCE/CVP ---
Making request to API for customer: VIP86753
API Response Received:
  Priority: 1
  Skill Group: Premium_Support
--- Simulation End ---

UCCE Action: Routing call for VIP86753 to Premium_Support.


--- Simulating UCCE/CVP ---
Making request to API for customer: CUST1138
API Response Received:
  Priority: 5
  Skill Group: Standard_Support
--- Simulation End ---

UCCE Action: Routing call for CUST1138 to Standard_Support.


--- Simulating UCCE/CVP ---
Making request to API for customer: None
Error: API returned status code 400
Response: {"error":"customer_id parameter is required"}
--- Simulation End ---
```