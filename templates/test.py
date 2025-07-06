from openai import OpenAI
import os

# Connect to LM Studio's local server
client = OpenAI(
	base_url="http://localhost:1234/v1",  # LM Studio's default API server
	api_key="lm-studio"  # Dummy key required
)

# Initialize conversation history
conversation = [
	{"role": "system", "content": "You are a dialogue analyzer"}
]
history = ""
while True:
	print(history)
	user_input = input("You: ")
	if user_input.lower() in ["exit", "quit", "bye"]:
		print("Bot: Goodbye! 👋")
		break
	elif user_input.lower() in ["analyze", "summarize"]:
		response = client.chat.completions.create(
			model="google/gemma-3-12b",
			messages=[
				{"role": "system", "content": "You are an analyzer based on dialogues"},
				{"role": "user", "content": "summarize and return only words to summarize user's personality based on the following dialogue text" + history}
			],
			temperature=0,
			stream=False
		)
	else:
		# Stream the assistant's response
		print("Bot: ", end="", flush=True)
		stream = client.chat.completions.create(
			model="google/gemma-3-12b",  # e.g., "llama-3.2-1b-instruct"
			messages=conversation,
			temperature=0,
			stream=True
		)

		full_reply = ""
		for chunk in stream:
			if chunk.choices[0].delta.content:
				token = chunk.choices[0].delta.content
				print(token, end="", flush=True)
				full_reply += token
		print()  # Newline after full response
		conversation.append({"role": "assistant", "content": full_reply})
