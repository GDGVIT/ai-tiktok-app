import google.generativeai as palm
import os

# load dotenv
from dotenv import load_dotenv

load_dotenv()

palm.configure(api_key=os.environ["PALMAPI"])

def generate_text(prompt):
    
    models = [
        m
        for m in palm.list_models()
        if "generateText" in m.supported_generation_methods
    ]
    model = models[0].name
    try:
        # return palm.generate_text(model=model, prompt=prompt).result
        # Return the generated text as a dictionary with output as key
        return {
            "output": palm.generate_text(model=model, prompt=prompt).result,
        }
    except Exception as e:
        print(e)
        return {"error": "Error generating text"}


# print(generate_text("Write a long paragraph voiceover about " + "Cats"))
