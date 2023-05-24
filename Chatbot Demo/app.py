from flask import Flask, render_template, request
import openai

app = Flask(__name__)

# Set up OpenAI API credentials
openai.api_key = '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'

# Define the default route to return the index.html file
@app.route("/")
def index():
    return render_template("index.html")

# Define the /api route to handle POST requests
@app.route("/api", methods=["POST"])
def api():
    # Get the message from the POST request
    message = request.json.get("message")

    # Send the message to OpenAI's API and receive the response
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": message},
        ]
    )

    if completion.choices[0].message.get("role") == "assistant":
        response = completion.choices[0].message["content"]
        return response
    else:
        return "Failed to generate a response."

if __name__ == '__main__':
    app.run()
