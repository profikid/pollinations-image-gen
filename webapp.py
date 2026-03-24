#!/usr/bin/env python3
"""Simple web interface for Pollinations Image Gen"""
import os
import sys
sys.path.insert(0, '/app')

from flask import Flask, render_template_string, request, jsonify, send_file
from gen import generate_image
import tempfile
import shutil

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Pollinations Image Generator</title>
    <style>
        body { font-family: sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; background: #1a1a2e; color: #fff; }
        h1 { color: #ff6b00; }
        input[type="text"] { width: 100%; padding: 10px; font-size: 16px; margin: 10px 0; }
        button { padding: 10px 20px; font-size: 16px; background: #ff6b00; color: white; border: none; cursor: pointer; }
        button:hover { background: #e65100; }
        .result { margin-top: 20px; }
        .result img { max-width: 100%; border-radius: 8px; margin-top: 10px; }
        .error { color: #ff6b6b; }
        .loading { color: #ffd93d; }
        .free-badge { background: #4CAF50; padding: 4px 8px; border-radius: 4px; font-size: 12px; }
    </style>
</head>
<body>
    <h1>🎨 Pollinations.ai Generator <span class="free-badge">FREE - No API Key</span></h1>
    <p>Generate images for free using Pollinations.ai</p>
    <form id="genForm">
        <input type="text" id="prompt" name="prompt" placeholder="Enter your prompt..." required>
        <button type="submit">Generate Image</button>
    </form>
    <div id="result" class="result"></div>
    <script>
        document.getElementById("genForm").onsubmit = async (e) => {
            e.preventDefault();
            const prompt = document.getElementById("prompt").value;
            const resultDiv = document.getElementById("result");
            resultDiv.innerHTML = '<p class="loading">Generating image... This may take 10-30 seconds.</p>';
            try {
                const response = await fetch("/generate", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({prompt: prompt})
                });
                const data = await response.json();
                if (data.error) {
                    resultDiv.innerHTML = '<p class="error">Error: ' + data.error + '</p>';
                } else if (data.images && data.images.length > 0) {
                    resultDiv.innerHTML = '<p>Generated image:</p><img src="' + data.images[0] + '" alt="Generated">';
                } else {
                    resultDiv.innerHTML = '<p class="error">No images generated</p>';
                }
            } catch (err) {
                resultDiv.innerHTML = '<p class="error">Error: ' + err.message + '</p>';
            }
        };
    </script>
</body>
</html>
'''

@app.route("/")
def index():
    return HTML_TEMPLATE

@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.get_json()
        prompt = data.get("prompt", "")
        if not prompt:
            return jsonify({"error": "No prompt provided"})
        
        # Generate images
        images = generate_image(prompt=prompt, count=1)
        
        if images:
            # Copy to a temp directory that we can serve from
            temp_dir = tempfile.mkdtemp()
            dest = os.path.join(temp_dir, "generated.jpg")
            shutil.copy(images[0], dest)
            return jsonify({"images": ["/image?path=" + dest], "success": True})
        else:
            return jsonify({"error": "No images generated"})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/image")
def serve_image():
    path = request.args.get("path")
    if path and os.path.exists(path):
        return send_file(path, mimetype="image/jpeg")
    return "Image not found", 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
