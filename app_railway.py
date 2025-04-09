from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({
        "status": "ok",
        "message": "Freshly API работает"
    })

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "service": "Freshly API",
        "version": "1.0.0"
    })

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port) 