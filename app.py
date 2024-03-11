from flask import Flask, request, jsonify
from flask_cors import CORS
import gemini_util as genAi
from PIL import Image

from pymongo import MongoClient
from io import BytesIO
import base64


app = Flask(__name__)
CORS(app)

@app.route("/api/calculate_calorie", methods=['POST'])
def analyze():
    
    try:
        # Retrieve the uploaded image and query from the request
        client = MongoClient('mongodb://localhost:27017/')
        db = client['Calorie']
        collection = db['CalorieAdvisor']
        uploaded_file = request.files['image']
        

        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            uploaded_file = request.files['image']
            image = Image.open(uploaded_file)
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

        # Prompt for processing the image
            prompt = """
            you are an expert in nutritionist where you need to see the food item from the image and calculate
            the total amout of calories , also provide the details of evry food item
            with calories intake is below format
            1. item 1 -- no.of calories
            2. item 2 -- no.of calories
            ---
            ---

            Total calories
        """
        


        if not prompt or not image:
            return jsonify({'error': 'Prompt and image are required.'}), 400

        # Call the function to process the image and generate a response
        response = genAi.get_gemini_pro_vision_response(image,prompt)
        entry = {
            'image' : img_str,
            'response' : response
        }
        collection.insert_one(entry)

    except Exception as e:
        print(e)
        # return jsonify({'error': 'An error occurred.'}), 500

    return ({'response': response})

@app.route("/api/get_chat_history", methods=['GET'])
def get_chat_history():
    # Retrieve chat history from MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['Calorie']
    collection = db['CalorieAdvisor']
    chat_history = list(collection.find({}, {'_id': 0}))
    return jsonify(chat_history)

@app.route("/api/register",methods=['POST'])
def register():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['Calorie']
    collection = db['users']
    data = request.json
    name=data.get('name')
    email=data.get('email')
    phone=data.get('phone')
    password=data.get('password')
    user_data={
        'name':name,
        'email':email,
        'phone':phone,
        'password':password
    }
    try:
        collection.insert_one(user_data)
        return "registered succesfuuly"
    except Exception as e:
        return False    

@app.route("/api/login", methods=['POST'])
def login():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['Calorie']
    collection = db['users']
    data = request.json
    email=data.get('email')
    password=data.get('password')
    user_data={
        'email':email,
        'password':password
    }
    user = collection.find_one({'email': email, 'password': password})
    if user:
        return "login successfull"
    else:
        return "False"    

if __name__ == "__main__":
    app.run(host = '192.168.1.7', port = 5000,debug=True)