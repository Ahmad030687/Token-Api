from flask import Flask, request, jsonify
import requests
import uuid

app = Flask(__name__)

def get_fb_token(email, password):
    # Unique IDs generate karna taake FB ko har baar naya device lage
    device_id = str(uuid.uuid4())
    adb_id = str(uuid.uuid4())
    
    # LATEST HEADERS TO BYPASS 5711 ERROR
    headers = {
        "Authorization": "OAuth 350685531728|62f8ce9f74b12f84c123cc23437a4a32",
        "User-Agent": "Mozilla/5.0 (Linux; Android 12; Pixel 6 Build/SD1A.210817.036; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/121.0.6167.178 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/445.0.0.34.118;]",
        "Content-Type": "application/x-www-form-urlencoded",
        "X-FB-Connection-Type": "WIFI",
        "X-FB-HTTP-Engine": "Liger",
        "X-FB-Client-IP": "True",
        "X-FB-Server-Cluster": "True",
        "X-FB-Friendly-Name": "authenticate"
    }
    
    data = {
        "email": email,
        "password": password,
        "generate_session_cookies": "1",
        "generate_analytics_claim": "1",
        "format": "json",
        "device_id": device_id,
        "adr_id": adb_id,
        "method": "auth.login",
        "error_detail_type": "button_with_disabled",
        "fb_api_req_friendly_name": "authenticate",
        "fb_api_caller_class": "com.facebook.account.login.protocol.Fb4aAuthHandler"
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
        "creator": "AHMAD RDX",
        "message": "RDX Token API is Live",
        "usage": "/token?u=EMAIL&p=PASSWORD"
    })

@app.route('/token', methods=['GET'])
def token_api():
    user = request.args.get('u')
    pw = request.args.get('p')
    
    if not user or not pw:
        return jsonify({
            "status": "error", 
            "message": "Email aur Password dono dena lazmi hain ustad!"
        }), 400
    
    result = get_fb_token(user, pw)
    
    # Success check
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
        # Error response formatting
        error_msg = result.get("error_msg", "Unknown error")
        return jsonify({
            "status": "failed",
            "message": error_msg,
            "full_response": result
        })

if __name__ == '__main__':
    # Koyeb ya Render ke liye port 8000 behtar hai
    app.run(host='0.0.0.0', port=8000)
    
