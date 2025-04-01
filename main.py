from flask import Flask, render_template, send_from_directory, request, jsonify

app = Flask(__name__)

# Counter to track verifications
verification_counter = {
    "total": 0,
    "authentic": 0,
    "fake": 0
}

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/verify', methods=['POST'])
def verify():
    """API endpoint to track product verifications"""
    data = request.json
    code = data.get('code', '')
    
    # Update counters
    verification_counter["total"] += 1
    
    if code.startswith('08552'):
        verification_counter["authentic"] += 1
        result = True
    else:
        verification_counter["fake"] += 1
        result = False
    
    # Return the verification result and updated counter
    return jsonify({
        "result": result,
        "counters": verification_counter
    })

@app.route('/api/counter', methods=['GET'])
def get_counter():
    """API endpoint to get the current verification statistics"""
    return jsonify(verification_counter)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)