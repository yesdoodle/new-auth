from flask import Flask, send_from_directory, request, jsonify

app = Flask(__name__)

# Dictionary to track how many times each code has been verified
code_verification_count = {}

# Route to reset the verification counter
@app.route('/api/reset-counter', methods=['POST'])
def reset_counter():
    """Reset the verification counter for all codes"""
    global code_verification_count
    code_verification_count = {}
    return jsonify({'success': True, 'message': 'Counter reset successfully'})

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/verify-code', methods=['POST'])
def verify_code():
    """Track how many times a specific code has been verified"""
    data = request.json
    code = data.get('code', '')
    
    # Increment counter for this specific code
    if code in code_verification_count:
        code_verification_count[code] += 1
    else:
        code_verification_count[code] = 1
    
    # Determine if the code is authentic (starts with 08552)
    is_authentic = code.startswith('08552')
    
    # Determine product type based on the last digit
    product_type = None
    if is_authentic and len(code) > 0:
        last_digit = code[-1]
        if last_digit == '1':
            product_type = "1 gram disposable cartridge"
        elif last_digit == '2':
            product_type = "2 gram disposable cartridge"
        elif last_digit == '3':
            product_type = "Concentrate/Dabs"
    
    return jsonify({
        'authentic': is_authentic,
        'count': code_verification_count[code],
        'product_type': product_type
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)