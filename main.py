from openai import OpenAI
from py4j.java_gateway import JavaGateway
import os

# create connection to JVM
gateway = JavaGateway()
Manager = gateway.entry_point.getManager()
Manager.Signup("I hate you", "I hate you", "I hate you")
print("is this running")

# Connect to LM Studio's local server
client = OpenAI(
	base_url="http://192.168.1.13:1234/v1",  # LM Studio's default API server
	api_key="lm-studio"  # Dummy key required
)

# Initialize conversation history
conversation = [
	{"role": "system", "content": "You are a helpful assistant."},
	{"role": "system", "content": "You are a therapist and should assess the hobbies of the user, traits of the user, and impactful experiences"}

]


#end sequence make into method
ending = [
	{"role": "system", "content": "make a summary of everything you know of me"}
	#this is where you can use the py4j to transfer the data
]

while True:
	user_input = input("You: ")
	if user_input.lower() in ["exit", "quit", "bye"]:
		ending#add the method
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
