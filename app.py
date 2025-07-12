# app.py

from flask import Flask, render_template, request

# हमारे बनाए हुए फंक्शन्स को इम्पोर्ट करना
from nlu import get_intent
from modules.movie_module import get_movie_recommendations
from modules.product_module import get_product_recommendations

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_recommendation', methods=['POST'])
def get_recommendation():
    prompt = request.form['prompt']
    
    # 1. यूज़र का इरादा समझो
    intent = get_intent(prompt)
    
    recommendations = []
    
    # 2. इरादे के हिसाब से सही मॉड्यूल को कॉल करो
    if intent == 'recommend_movie':
        recommendations = get_movie_recommendations(prompt)
    elif intent == 'find_product':
        recommendations = get_product_recommendations(prompt)
    else:
        recommendations = ["I'm sorry, I don't understand. Please ask about movies or products."]
        
    # 3. रिजल्ट को वेबपेज पर भेजो
    return render_template('index.html', 
                           prompt=prompt, 
                           intent=intent, 
                           recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)