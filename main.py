from flask import Flask, send_from_directory, request, jsonify

app = Flask(__name__)

# Dictionary to track how many times each code has been verified
code_verification_count = {}

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
    
    return jsonify({
        'authentic': is_authentic,
        'count': code_verification_count[code]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)