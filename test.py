from openai import OpenAI

//
client = OpenAI(
	api_key="lm-studio",  # 固定写法
	base_url="http://10.0.0.62:1234/v1"
)

response = client.chat.completions.create(
	model="google/gemma-3-12b",
	messages=[
		{"role": "system", "content": "You are a useful ai"},
		{"role": "user", "content": "Why linus does not use C++ in linux but use rust"}
	],
	temperature=0.7,
	stream=True
)

for chunk in response:
	if chunk.choices[0].delta.content:
		print(chunk.choices[0].delta.content, end="", flush=True)