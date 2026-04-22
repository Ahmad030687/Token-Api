from flask import Flask, request, jsonify
import requests
import uuid

app = Flask(__name__)

def get_fb_token(email, password):
    # Unique ID aur User Agent taake FB ko lage ke real phone se login ho raha hai
    device_id = str(uuid.uuid4())
    adb_id = str(uuid.uuid4())
    
    headers = {
        "Authorization": "OAuth 350685531728|62f8ce9f74b12f84c123cc23437a4a32",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 10; Mi 9T Pro Build/QKQ1.190825.002) [FBAN/MessengerLite;FBAV/305.1.0.40.120;FBPN/com.facebook.mlite;FBLC/en_US;FBBV/3051040120;]",
        "Content-Type": "application/x-www-form-urlencoded",
        "X-FB-Connection-Type": "WIFI",
        "X-FB-HTTP-Engine": "Liger"
    }
    
    data = {
        "email": email,
        "password": password,
        "generate_session_cookies": "1",
        "generate_analytics_claim": "1",
        "format": "json",
        "device_id": device_id,
        "adr_id": adb_id,
        "method": "auth.login"
    }

    try:
        # Facebook Business API Login Endpoint
        response = requests.post("https://b-api.facebook.com/method/auth.login", data=data, headers=headers)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

@app.route('/')
def home():
    return jsonify({
        "status": "Online",
        "message": "Welcome to AHMAD RDX Token API",
        "usage": "/token?u=EMAIL&p=PASSWORD"
    })

@app.route('/token', methods=['GET'])
def token_api():
    user = request.args.get('u')
    pw = request.args.get('p')
    
    if not user or not pw:
        return jsonify({"status": "error", "message": "Email and Password are required!"}), 400
    
    result = get_fb_token(user, pw)
    
    # Agar token mil jaye
    if "access_token" in result:
        return jsonify({
            "status": "success",
            "creator": "AHMAD RDX",
            "data": {
                "access_token": result["access_token"],
                "cookies": result.get("session_cookies", [])
            }
        })
    else:
        return jsonify({
            "status": "failed",
            "message": result.get("error_msg", "Unknown error occurred"),
            "full_response": result
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

