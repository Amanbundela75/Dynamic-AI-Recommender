from flask import Flask, render_template, request
from main import get_dynamic_recommendation 

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_recommendation', methods=['POST'])
def handle_recommendation():
    user_prompt = request.form['prompt']
    ai_recommendations = get_dynamic_recommendation(user_prompt)
    
    return render_template('index.html', 
                           recommendations=ai_recommendations, 
                           prompt=user_prompt)

if __name__ == '__main__':
    app.run(debug=True)