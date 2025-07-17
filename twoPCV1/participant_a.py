from flask import Flask, request, jsonify
import redis

app = Flask(__name__)
r = redis.Redis()

SERVICE_NAME = "participant_a"

@app.route('/prepare', methods=['POST'])
def prepare():
    data = request.json
    txn_id = data['txn_id']
    can_commit = data.get('can_commit', True)

    if can_commit:
        r.set(f"{SERVICE_NAME}:{txn_id}:prepared", 1)
        return jsonify({"status": "prepared"})
    else:
        return jsonify({"status": "abort"}), 400

@app.route('/commit', methods=['POST'])
def commit():
    txn_id = request.json['txn_id']
    if r.get(f"{SERVICE_NAME}:{txn_id}:prepared"):
        r.delete(f"{SERVICE_NAME}:{txn_id}:prepared")
        return jsonify({"status": "committed"})
    return jsonify({"status": "not_prepared"}), 400

@app.route('/rollback', methods=['POST'])
def rollback():
    txn_id = request.json['txn_id']
    r.delete(f"{SERVICE_NAME}:{txn_id}:prepared")
    return jsonify({"status": "rolled_back"})

if __name__ == '__main__':
    app.run(port=5001)
