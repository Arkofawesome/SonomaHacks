from openai import OpenAI
import os

# Connect to LM Studio's local server
client = OpenAI(
	base_url="http://localhost:1234/v1",  # LM Studio's default API server
	api_key="lm-studio"  # Dummy key required
)

# Initialize conversation history
conversation = [
	{"role": "system", "content": "You are a helpful assistant."}
]

while True:
	user_input = input("You: ")
	if user_input.lower() in ["exit", "quit", "bye"]:
		print("Bot: Goodbye! 👋")
		break

	conversation.append({"role": "user", "content": user_input})

	# Stream the assistant's response
	print("Bot: ", end="", flush=True)
	stream = client.chat.completions.create(
		model="google/gemma-3-12b",  # e.g., "llama-3.2-1b-instruct"
		messages=conversation,
		temperature=0.7,
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
