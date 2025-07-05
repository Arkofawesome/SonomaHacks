from openai import OpenAI

client = OpenAI(
	api_key="lm-studio",  # 固定写法
	base_url="http://10.0.0.62:1234/v1"
)

response = client.chat.completions.create(
	model="google/gemma-3-12b",
	messages=[
		{"role": "system", "content": "You are a useful ai"},
		{"role": "user", "content": "To C or not to C that is the question"}
	],
	temperature=0.7,
	stream=False
)

print(response.choices[0].message.content)