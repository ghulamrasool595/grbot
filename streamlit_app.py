from flask import Flask, request, jsonify
import google.generativeai as genai  # Install with pip install google-generativeai

app = Flask(__name__)

# Configure Gemini API (replace with your API key)
genai.configure(api_key="YOUR_GEMINI_API_KEY")
model = genai.GenerativeModel('gemini-1.5-flash')  # Supports multilingual, including Sindhi

@app.route('/')
def index():
    return open('index.html').read()

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    # Generate response in Sindhi (Gemini handles language detection)
    response = model.generate_content(f"Respond in Sindhi: {user_message}")
    return jsonify({'response': response.text})

if __name__ == '__main__':
    app.run(debug=True)
