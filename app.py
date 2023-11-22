from flask import Flask, request, jsonify, render_template
import requests
import pymongo
import datetime
import urllib.parse
application = Flask(__name__)
azure_api_url = ""
azure_api_key = "" 


# MongoDB configuration
username = "Promptbuilder"
password = "Promptbuilder@1234"
database_name = "Promptbuilder" 

# Escape the username and password
escaped_username = urllib.parse.quote_plus(username)
escaped_password = urllib.parse.quote_plus(password)

# Build the MongoDB URI
mongo_uri = f"mongodb+srv://{escaped_username}:{escaped_password}@cluster0.ul7b8vv.mongodb.net/{database_name}?retryWrites=true&w=majority"

# Connect to MongoDB
mongo_client = pymongo.MongoClient(mongo_uri)
db = mongo_client[database_name]
collection = db["Prompt_data"]
@application.route("/")
def login():
    return render_template("login.html")

@application.route("/main")
def main_ui():
    return render_template("index.html")

@application.route("/generate_prompt", methods=["POST"])
def generate_prompt():
    data = request.get_json()
    role = data["role"]
    goal = data["goal"]
    model = data["model"]
    adjective = data["adjective"]
    platform = data["platform"]
    area = data["area"]
    prompts = data["prompts"]
    issue = data["issue"]
    Tokens = int(data["Tokens"])
    temperature = float(data["temperature"])
    language = data["language"]
    # like = data["userInput1"]
    # dislike = data["userInput2"]


    message = f"""Assume you are a {role}
    working on {area} and your objective is {adjective} and the issue that the user facing is {issue} on {platform} , you need to provide step-by-step instructions to resolve the issue. 
    If the user is still not able to resolve the issue, ask them to send a mail to ITSupport@wipro.com, provide the 5 instructions in {language} language.
    """

    first_prompt = f"""
                    How can i troubleshoot the issue - {issue} on the {platform} as an {role} to {adjective}?
                
"""
    
    # print(like)
    # print(dislike)
    

    


    #message_prom = f"""Generate 12 prompts that can be fed to large language models to get precise response for the {issue} on {platform} in {language} in more technical and low level context """
    # Process the prompt with the Azure GPT model to get the final response
    message_prom = f"""I want you to become my Prompt Creator. Your goal is to help me craft the {prompts} best possible prompt for your needs. The prompt will be used to fed into ChatGPT. Follow the following process to 
            generate a precise technical prompt for the issue: '{issue}' on the platform: '{platform}'. 
            Make sure it is more technical prompt rather than simple.it should be in '{language}' language"""
    response = process_with_azure(message, "bd38ee31e244408cacab3e1dd4c32221", Tokens, temperature)
    print("Generated Response:", response)

    response_suggestions = process_with_azure(message_prom, "bd38ee31e244408cacab3e1dd4c32221",  Tokens, temperature)
    print("prompt_generated:", response_suggestions)


    print(first_prompt)
    
  

    print("message", message)
    print("Issue: ", issue)
    print("prompts: ", prompts)
    print("tokens: ", Tokens)
    print("temperature: ", temperature)
    print("Language: ", language)


    user_input ={
        "role":role,
        "goal":goal,
        "model":model,
        "adjective": adjective,
        "platform": platform,
        "area": area,
        "Prompts": prompts,
        "response":response,
        "Time":datetime.datetime.now()
    }
    collection.insert_one(user_input)
    # print(response)
    response_data = {
        "first_prompt": first_prompt,
        "response": response,
        "response_suggestions": response_suggestions
    }
    return jsonify(response_data)


def process_with_azure(prompt, azure_api_key, max_token, temperature):
    url = "https://dwspoc.openai.azure.com/openai/deployments/GPTDavinci/completions?api-version=2022-12-01"

    # Set the headers with the API key and content type
    headers = {"Content-Type": "application/json", "api-key": azure_api_key}
    print(max_token)
    print(type(max_token))
    print(temperature)
    # Set the parameters for the GPT-3 completion
    data = {
        "prompt": prompt,
        "max_tokens": max_token,
        "temperature": temperature,
        "top_p": 1,
        "stop": None,
    }

    # Make the API call to GPT-3
    response = requests.post(url, headers=headers, json=data)
    response_data = response.json()
    #print(response_data,'/n')

    # Extract and return the response text
    return response_data["choices"][0]["text"].strip()


if __name__ == "__main__":
    application.run(host="0.0.0.0", port=5000)
