from flask import Flask, request, jsonify
from redis_client import set_idempotency_key, get_value
import uuid

app = Flask(__name__)

# 模拟数据库（内存）
ORDERS = {}
PAYMENTS = {}


@app.route("/create_order", methods=["POST"])
def create_order():
    user_id = request.json["user_id"]
    amount = request.json["amount"]
    order_id = str(uuid.uuid4())

    ORDERS[order_id] = {
        "user_id": user_id,
        "amount": amount,
        "status": "PENDING"
    }

    return jsonify({"order_id": order_id})


@app.route("/initiate_payment", methods=["POST"])
def initiate_payment():
    order_id = request.json["order_id"]
    payment_id = str(uuid.uuid4())
    idempotency_key = f"payment:{payment_id}"

    if not set_idempotency_key(idempotency_key, "initiated"):
        return jsonify({"error": "Duplicate payment"}), 409

    PAYMENTS[payment_id] = {
        "order_id": order_id,
        "status": "PENDING"
    }

    # 假设支付链接为模拟跳转
    return jsonify({
        "payment_id": payment_id,
        "payment_url": f"http://localhost:5000/simulate_gateway_callback/{payment_id}"
    })


@app.route("/webhook/payment_callback", methods=["POST"])
def payment_callback():
    print("Received:", request.json)

    data = request.json
    print("Received webhook:", data)

    payment_id = request.json["payment_id"]
    success = request.json["success"]
    idempotency_key = f"callback:{payment_id}"

    if not set_idempotency_key(idempotency_key, "received"):
        return jsonify({"message": "Duplicate callback"}), 200

    payment = PAYMENTS.get(payment_id)
    if not payment:
        return jsonify({"error": "Invalid payment ID"}), 404

    if success:
        payment["status"] = "PAID"
        order_id = payment["order_id"]
        ORDERS[order_id]["status"] = "PAID"
    else:
        payment["status"] = "FAILED"

    #return jsonify({"message": "Callback processed"})
    return jsonify({"status": "ok", "message": "payment processed"}), 200

@app.route("/orders", methods=["GET"])
def get_orders():
    return jsonify(ORDERS)


if __name__ == "__main__":
    app.run(debug=True)
