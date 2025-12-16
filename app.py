import os
import time
import random
import json
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

PORT = os.environ.get('PORT', 10000)

@app.route('/key=<string:key>/cc=<string:cc_data>', methods=['GET'])
def process_payment(key, cc_data):
    """Process payment via Stripe API"""
    
    # Log the request
    print(f"🔒 Received payment request for key: {key}")
    
    # Validate API key
    if key != "@OnyxEnvBot":
        return jsonify({
            "error": "Invalid API key",
            "status": "failed"
        }), 403
    
    # Validate CC format
    if '|' not in cc_data:
        return jsonify({
            "error": "Invalid card format. Use: CARD|MM|YY|CVC",
            "status": "failed"
        }), 400
    
    try:
        card_number, exp_month, exp_year, cvc = cc_data.split('|')
        
        # Validate card number length
        if len(card_number) < 13 or len(card_number) > 19:
            return jsonify({
                "error": "Invalid card number length",
                "status": "failed"
            }), 400
        
        # Log processing (mask card number for security)
        masked_card = f"{card_number[:6]}******{card_number[-4:]}"
        print(f"💳 Processing: {masked_card}")
        
        # Real processing delay (7-12 seconds)
        delay = random.randint(7, 12)
        print(f"⏱️ Processing time: {delay} seconds")
        time.sleep(delay)
        
        # Create response
        response = {
            "cc": cc_data,
            "Gateway": "Stripe $98.7",
            "Bot": "@OnyxEnvBot",
            "Api": "@Toenv", 
            "Dev": "@Lost_yashika",
            "response": "Your card was declined",
            "status": "declined",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "processing_time": f"{delay} seconds"
        }
        
        print(f"✅ Request completed for: {masked_card}")
        return jsonify(response)
        
    except ValueError:
        return jsonify({
            "error": "Invalid card data format. Use: CARD|MM|YY|CVC",
            "status": "failed"
        }), 400
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({
            "error": "Internal server error",
            "status": "failed"
        }), 500

@app.route('/')
def home():
    return jsonify({
        "service": "Payment Processing API",
        "version": "1.0.0",
        "author": "@Lost_yashika",
        "usage": "GET /key=@OnyxEnvBot/cc=CARD|MM|YY|CVC",
        "example": "https://YOUR-SERVICE.onrender.com/key=@OnyxEnvBot/cc=4111111111111111|12|25|123",
        "response_format": {
            "cc": "CARD|MM|YY|CVC",
            "Gateway": "Stripe $98.7",
            "Bot": "@OnyxEnvBot",
            "Api": "@Toenv",
            "Dev": "@Lost_yashika",
            "response": "Your card was declined",
            "status": "declined"
        },
        "note": "All requests return 'Your card was declined' with 7-12 second delay"
    })

@app.route('/health')
def health():
    return jsonify({
        "status": "active",
        "service": "payment_processor",
        "uptime": "running",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    })

@app.route('/status')
def status():
    return jsonify({
        "service": "Payment API",
        "status": "operational",
        "endpoint": "/key=<api_key>/cc=<card_data>",
        "processing_time": "7-12 seconds",
        "default_response": "Your card was declined"
    })

@app.route('/test')
def test():
    """Quick test endpoint (no delay)"""
    return jsonify({
        "message": "API is working!",
        "test_endpoint": "/key=@OnyxEnvBot/cc=4111111111111111|12|25|123",
        "status": "ready"
    })

@app.errorhandler(404)
def not_found(e):
    return jsonify({
        "error": "Endpoint not found",
        "available_endpoints": {
            "home": "/",
            "process_payment": "/key=@OnyxEnvBot/cc=CARD|MM|YY|CVC",
            "health": "/health",
            "status": "/status",
            "test": "/test"
        }
    }), 404

if __name__ == '__main__':
    print("="*70)
    print("🚀 PAYMENT PROCESSING API - READY FOR DEPLOYMENT")
    print("="*70)
    print(f"📡 Running on port: {PORT}")
    print("🔐 API Key: @OnyxEnvBot")
    print("💳 Endpoint: /key=@OnyxEnvBot/cc=CARD|MM|YY|CVC")
    print("\n📌 Example:")
    print("  /key=@OnyxEnvBot/cc=4111111111111111|12|25|123")
    print("\n✅ Response:")
    print('''  {
    "cc": "4111111111111111|12|25|123",
    "Gateway": "Stripe $98.7",
    "Bot": "@OnyxEnvBot",
    "Api": "@Toenv",
    "Dev": "@Lost_yashika",
    "response": "Your card was declined",
    "status": "declined"
  }''')
    print(f"\n⏱️  Processing time: 7-12 seconds")
    print("="*70)
    
    app.run(host='0.0.0.0', port=PORT, debug=False)
