from dotenv import load_dotenv
import os
import google.generativeai as genAi 

load_dotenv()

apiKey=os.getenv("GEMINI_API_KEY")

genAi.configure(api_key=apiKey)

def get_gemini_pro_vision_response(input,image):
    model=genAi.GenerativeModel("gemini-pro-vision")
    response=model.generate_content([input,image])
    return response.text

print("Done")