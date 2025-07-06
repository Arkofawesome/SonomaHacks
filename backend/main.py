from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from openai import OpenAI
from py4j.java_gateway import JavaGateway, GatewayParameters

# Setup Flask
app = Flask(__name__)
CORS(app)

# Connect to Gemini (LM Studio)
client = OpenAI(
    base_url="http://10.0.0.62:1234/v1",  # LM Studio local endpoint
    api_key="lm-studio"
)

# Connect to Java
gateway = JavaGateway(gateway_parameters=GatewayParameters(address="10.0.0.62", port=25333))
java_app = gateway.entry_point

# Persistent chat history (can be scoped per session later)
conversation = [
    {"role": "system", "content": "You are a friendly AI trying to understand the user's interests."},
    {"role": "system", "content": "You are a therapist and should assess the user's hobbies, traits, and impactful experiences."}
]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")
    history = data.get("history", [])
    phone = data.get("phone", "unknown")
    password = data.get("password", "pass123")

    print(f"📥 Received phone: {phone}, password: {password}")
    
    # Append user message
    conversation.append({"role": "user", "content": user_input})

    # Handle ending sequence
    if user_input.lower() in ["exit", "quit", "bye", "goodbye", "have a nice day"]:
        summary_payload = [{"role": "system", "content": "make a summary of everything you know of me"}]
        conversation.extend(summary_payload)

        try:
            stream = client.chat.completions.create(
                model="google/gemma-7b-it",  # adjust if using a different model
                messages=conversation,
                temperature=0.2,
                stream=True
            )
            summary_text = ""
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    summary_text += chunk.choices[0].delta.content

            # Store in Java
            phone = data.get("phone", "unknown")
            password = data.get("password", "pass123")
            java_app.importSummary(summary_text, phone, password)

            # Match logic
            number = java_app.getTotalNumber()
            matches = []
            for i in range(number):
                other_summary = java_app.getSummary(i)
                match_prompt = [
                    {"role": "user", "content": f"Compare the following two people and give a compatibility score out of 100 with no explanation:\n1. {summary_text}\n2. {other_summary}"}
                ]
                score_response = client.chat.completions.create(
                    model="google/gemma-7b-it",
                    messages=match_prompt,
                    temperature=0.1
                )
                score = score_response.choices[0].message.content.strip()
                try:
                    if int(score) >= 50:
                        matches.append(f"{java_app.getPhone_Number(i)} ({score}%)")
                except:
                    continue

            reply = "Thanks for chatting! Here's who you matched with:\n" + ("\n".join(matches) if matches else "No good matches found.")
            return jsonify({"response": reply})

        except Exception as e:
            return jsonify({"response": f"An error occurred during summary or matching: {e}"})

    # Normal conversation
    try:
        stream = client.chat.completions.create(
            model="google/gemma-7b-it",
            messages=conversation,
            temperature=0.7,
            stream=True
        )
        full_reply = ""
        for chunk in stream:
            if chunk.choices[0].delta.content:
                full_reply += chunk.choices[0].delta.content

        conversation.append({"role": "assistant", "content": full_reply})
        return jsonify({"response": full_reply.strip()})
    except Exception as e:
        return jsonify({"response": f"An error occurred: {e}"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
