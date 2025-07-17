from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/pay', methods=['POST'])
def process_payment():
    data = request.json
    print(f"支付处理中，事务 {data['txn_id']}")
    # 模拟成功：
    return jsonify({"status": "paid"})
    # 模拟失败测试补偿：
    # return jsonify({"error": "支付失败"}), 500

@app.route('/refund', methods=['POST'])
def refund_payment():
    data = request.json
    print(f"退款，事务 {data['txn_id']}")
    return jsonify({"status": "refunded"})

if __name__ == "__main__":
    app.run(port=5003)
