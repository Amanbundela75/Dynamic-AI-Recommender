from flask import Flask, render_template, request
# हमारे AI लॉजिक वाले फंक्शन को इम्पोर्ट करें
from main import get_dynamic_recommendation 

# Flask ऐप को इनिशियलाइज़ करें
app = Flask(__name__)

@app.route('/')
def home():
    """यह फंक्शन होमपेज दिखाता है।"""
    return render_template('index.html')

@app.route('/get_recommendation', methods=['POST'])
def handle_recommendation():
    """यह फॉर्म सबमिशन को हैंडल करता है और AI से जवाब लाता है।"""
    # यूज़र का प्रॉम्प्ट फॉर्म से निकालें
    user_prompt = request.form['prompt']
    
    # AI फंक्शन को कॉल करके रिकमेंडेशन पाएं
    # यह API कॉल्स करेगा, इसलिए इसमें थोड़ा समय लग सकता है
    ai_response = get_dynamic_recommendation(user_prompt)
    
    # रिजल्ट को वापस HTML पेज पर भेजें
    return render_template('index.html', 
                           recommendation_text=ai_response, 
                           prompt=user_prompt)

if __name__ == '__main__':
    # ऐप को चलाएं
    app.run(debug=True)