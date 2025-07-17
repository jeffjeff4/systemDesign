from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/webhook/payment_callback", methods=["POST"])
def webhook():
    data = request.get_json()
    print("收到支付回调:", data)
    return jsonify({"status": "received"}), 200

if __name__ == "__main__":
    app.run(debug=True)
