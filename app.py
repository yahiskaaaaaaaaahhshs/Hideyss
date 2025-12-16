import os
import time
import random
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

PORT = os.environ.get('PORT', 10000)

@app.route('/key=<string:key>/cc=<string:cc_data>', methods=['GET'])
def process_payment(key, cc_data):
    """Process payment via Stripe API"""
    
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
        
        # Real processing delay (7-12 seconds)
        delay = random.randint(7, 12)
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
        
        return jsonify(response)
        
    except ValueError:
        return jsonify({
            "error": "Invalid card data format. Use: CARD|MM|YY|CVC",
            "status": "failed"
        }), 400
    except Exception as e:
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
        "usage": "GET /key=@OnyxEnvBot/cc=CARD|MM|YY|CVC"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=False)
