from flask import Flask, jsonify, request
import requests
import uuid

app = Flask(__name__)

orders = []

INVENTORY_URL = "http://localhost:5001/inventory/check"
INVENTORY_TIMEOUT_SECONDS = 2

@app.post("/orders")
def create_order():
    data = request.get_json(silent=True) or {}

    item_id = data.get("item_id")
    quantity = data.get("quantity")

    if not item_id or not isinstance(quantity, int) or quantity <= 0:
        return jsonify({
            "error": "item_id and a positive integer quantity are required"
        }), 400

    try:
        response = requests.get(
            INVENTORY_URL,
            params={
                "item_id": item_id,
                "quantity": quantity
            },
            timeout=INVENTORY_TIMEOUT_SECONDS
        )

        response.raise_for_status()
        inventory_result = response.json()

    except requests.exceptions.Timeout:
        return jsonify({
            "error": "Inventory Service request timed out"
        }), 504

    except requests.exceptions.RequestException:
        return jsonify({
            "error": "Inventory Service unavailable"
        }), 503

    if not inventory_result["available"]:
        return jsonify({
            "error": "Item unavailable",
            "item_id": item_id,
            "requested_quantity": quantity
        }), 409

    order = {
        "order_id": str(uuid.uuid4()),
        "item_id": item_id,
        "quantity": quantity,
        "status": "created"
    }

    orders.append(order)

    print("EVENT: OrderCreated", order)

    return jsonify({
        "message": "Order created",
        "order": order
    }), 201

@app.get("/orders")
def get_orders():
    return jsonify(orders), 200

if __name__ == "__main__":
    app.run(port=5000)
