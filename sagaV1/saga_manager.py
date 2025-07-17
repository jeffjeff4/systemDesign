from flask import Flask, request, jsonify
import requests
import threading

app = Flask(__name__)

# 事务状态存储（内存）
saga_states = {}

# 事务步骤定义（顺序执行）
SAGA_STEPS = [
    {
        "name": "create_order",
        "action_url": "http://localhost:5001/create",
        "compensate_url": "http://localhost:5001/cancel"
    },
    {
        "name": "reserve_inventory",
        "action_url": "http://localhost:5002/reserve",
        "compensate_url": "http://localhost:5002/release"
    },
    {
        "name": "process_payment",
        "action_url": "http://localhost:5003/pay",
        "compensate_url": "http://localhost:5003/refund"
    }
]

def call_service(url, txn_id):
    try:
        resp = requests.post(url, json={"txn_id": txn_id}, timeout=5)
        resp.raise_for_status()
        return True
    except Exception as e:
        print(f"调用服务失败 {url}，错误: {e}")
        return False

def execute_saga(txn_id):
    saga_states[txn_id] = {"status": "in_progress", "step": 0}

    for i, step in enumerate(SAGA_STEPS):
        print(f"执行步骤 {step['name']}，事务 {txn_id}")
        success = call_service(step['action_url'], txn_id)
        if not success:
            print(f"步骤失败，开始补偿，事务 {txn_id}")
            # 失败，补偿已执行的步骤
            for j in range(i-1, -1, -1):
                comp_step = SAGA_STEPS[j]
                print(f"补偿步骤 {comp_step['name']}，事务 {txn_id}")
                call_service(comp_step['compensate_url'], txn_id)
            saga_states[txn_id]['status'] = 'failed'
            return
        saga_states[txn_id]['step'] = i + 1

    saga_states[txn_id]['status'] = 'success'

@app.route('/start_saga', methods=['POST'])
def start_saga():
    import uuid
    txn_id = str(uuid.uuid4())
    threading.Thread(target=execute_saga, args=(txn_id,), daemon=True).start()
    return jsonify({"txn_id": txn_id, "message": "Saga started"})

@app.route('/status/<txn_id>', methods=['GET'])
def status(txn_id):
    state = saga_states.get(txn_id, None)
    if not state:
        return jsonify({"error": "unknown txn_id"}), 404
    return jsonify(state)

if __name__ == "__main__":
    app.run(port=5000)
