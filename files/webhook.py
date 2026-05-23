from flask import Flask, request

app = Flask(__name__)

VERIFY_TOKEN = "mybotsecret2026"   # ← Change this

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if mode == "subscribe" and token == VERIFY_TOKEN:
            print("✅ Webhook verified successfully!")
            return challenge, 200
        else:
            return "Forbidden", 403

    elif request.method == 'POST':
        data = request.get_json()
        print("📩 Received message:", data)
        
        # Simple echo (for testing)
        try:
            sender_id = data['entry'][0]['messaging'][0]['sender']['id']
            message_text = data['entry'][0]['messaging'][0]['message']['text']
            print(f"User said: {message_text}")
        except:
            pass

        return "EVENT_RECEIVED", 200


@app.route('/')
def home():
    return "Bot is running locally!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)