from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/create', methods=['POST'])
def create_order():
    data = request.json
    print(f"订单创建，事务 {data['txn_id']}")
    return jsonify({"status": "created"})

@app.route('/cancel', methods=['POST'])
def cancel_order():
    data = request.json
    print(f"订单取消，事务 {data['txn_id']}")
    return jsonify({"status": "cancelled"})

if __name__ == "__main__":
    app.run(port=5001)
