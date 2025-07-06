from ipaddress import summarize_address_range

from openai import OpenAI
from py4j.java_gateway import JavaGateway
import os

# create connection to JVM
gateway = JavaGateway()
java_app = gateway.entry_point

# Connect to LM Studio's local server
client = OpenAI(
	base_url="http://192.168.1.245:1234/v1",  # LM Studio's default API server
	api_key="lm-studio"  # Dummy key required
)

# Initialize conversation history
conversation = [
	{"role": "system", "content": "You are a helpful assistant."},
	{"role": "system", "content": "You are a therapist and should assess the hobbies of the user, traits of the user, and impactful experiences"}
]


#end sequence make into method
#ending = [
#	{"role": "system", "content": "make a summary of everything you know of me"}
#	#this is where you can use the py4j to transfer the data
#]

#implement another version of end sequence
def end_sequence():
	summary_payload = [
		{"role": "system","content":"make a summary of everything you know of me"}
	]
	summary_text = summary_payload[0]["content"]

	#asking for phone number and password to login, if it  doesn't exist it will create an account automatically
	phone_number = input("Please enter your phone number:")
	password  = input("Please enter your password: ")

	java_app.importSummary(summary_text,phone_number,password)

	print("Bot:Goodbye!")

	#auto matching
	number = java_app.getTotalNumber()
	lists = " "
	print("Match {number} times: " )
	for i in range(number):
		Matching = [
			{"role": "User","content": "Only gives me the percentage of following two person, do not add any other word and symbols include %, 1," + summary_text + "\n 2," + java_app.getSummary(i)}
		]
		if(int(Matching) >= 50):
			lists += i + "," + java_app.getPhone_Number + "\n"

	if lists == " ":
		print("Sorry, there's no one matching with you\n")
	else:
		print("this is the lists that matching with you\n" + lists)

	return summary_payload




while True:
	user_input = input("You: ")
	if user_input.lower() in ["exit", "quit", "bye", "goodbye", "have a nice day"]:
		end_sequence()
	else:
		conversation.append({"role": "user", "content": user_input})

		# Stream the assistant's response
		print("Bot: ", end="", flush=True)
		stream = client.chat.completions.create(
			model="google/gemma-3-12b",  # e.g., "llama-3.2-1b-instruct"
			messages=conversation,
			temperature=0.1,
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
