from flask import Flask, jsonify, request

app = Flask(__name__)

inventory = {
    "laptop": 5,
    "phone": 10,
    "headphones": 0
}

@app.get("/inventory/check")
def check_inventory():
    item_id = request.args.get("item_id")
    quantity = request.args.get("quantity", type=int)

    if not item_id or quantity is None or quantity <= 0:
        return jsonify({
            "error": "item_id and a positive quantity are required"
        }), 400

    available_quantity = inventory.get(item_id, 0)

    return jsonify({
        "item_id": item_id,
        "requested_quantity": quantity,
        "available_quantity": available_quantity,
        "available": available_quantity >= quantity
    }), 200

if __name__ == "__main__":
    app.run(port=5001)