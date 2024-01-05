import google.generativeai as palm
from dotenv import load_dotenv
import os

load_dotenv()


def configure_palm():
    """
    Configures the PALM API with the provided API key from the environment variables.
    """
    palm.configure(api_key=os.environ["PALMAPI"])


def list_supported_models():
    """
    Lists the models that support the "generateText" generation method.

    Returns:
        list: List of models that support "generateText".
    """
    return [
        model
        for model in palm.list_models()
        if "generateText" in model.supported_generation_methods
    ]


def generate_text(prompt):
    """
    Generates text using the selected model based on the given prompt.

    Args:
        prompt (str): The prompt for text generation.

    Returns:
        dict: A dictionary containing the generated text in the 'output' key if successful.
              If an error occurs, the dictionary contains an 'error' key.
    """
    configure_palm()
    try:
        models = list_supported_models()
        if models:
            selected_model = models[0].name
            generated_text = palm.generate_text(
                model=selected_model, prompt=prompt
            ).result
            return generated_text
        else:
            return {"error": "No supported models found"}
    except EOFError as e:
        print(e)
        return {"error": "Error generating text"}


print(generate_text("Write a long paragraph voiceover about cats"))
