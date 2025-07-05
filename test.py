from pyexpat.errors import messages

from openai import OpenAI
import os
#test version
client = OpenAI(
	api_key="lm-studio",
	base_url="http://10.0.0.62:1234/v1"
)

conversation = [
	{"role": "system", "content": "You are a analyzer of human character based on the dialogue."}
]

while True:
	user_input = input("You: ")
	if user_input.lower() in ["exit", "quit", "bye"]:
		print("Bot: Goodbye!")
		break

	conversation.append({"role": "user", "content": user_input})

	print("Bot: ", end="", flush=True)
	stream = client.chat.completions.create(
		model="google/gemma-3-12b",
		messages = conversation,
		temperature=0.7,
		stream=True
	)

	full_reply = ""
	for chunk in stream:
		if chunk.choices[0].delta.content:
			token = chunk.choices[0].delta.content
			print(token, end="", flush=True)
			full_reply += token

	print()
	conversation.append({"role": "assistant", "content": full_reply})