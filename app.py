from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/get_customer_priority', methods=['GET'])
def get_customer_priority():
    """
    This endpoint simulates determining a customer's priority level.
    In a real-world scenario, this could involve a database lookup
    or a more complex business logic.

    Query Parameters:
        customer_id (str): The ID of the customer.
    """
    customer_id = request.args.get('customer_id')

    if not customer_id:
        return jsonify({"error": "customer_id parameter is required"}), 400

    # In a real application, you would look up the customer's priority
    # from a database or another service. Here, we'll just use a simple
    # logic for demonstration.
    if customer_id.startswith('VIP'):
        priority = 1
        skill_group = "Premium_Support"
    else:
        priority = 5
        skill_group = "Standard_Support"

    response = {
        "customer_id": customer_id,
        "priority": priority,
        "skill_group": skill_group
    }

    return jsonify(response)

if __name__ == '__main__':
    # Note: In a production environment, you would use a production-ready
    # web server like Gunicorn or uWSGI instead of the built-in Flask server.
    app.run(host='0.0.0.0', port=5000)