from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/reserve', methods=['POST'])
def reserve_inventory():
    data = request.json
    print(f"库存预留，事务 {data['txn_id']}")
    # 这里可以模拟失败，比如：
    # return jsonify({"error": "库存不足"}), 500
    return jsonify({"status": "reserved"})

@app.route('/release', methods=['POST'])
def release_inventory():
    data = request.json
    print(f"库存释放，事务 {data['txn_id']}")
    return jsonify({"status": "released"})

if __name__ == "__main__":
    app.run(port=5002)
