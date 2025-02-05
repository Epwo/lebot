from mistralai import Mistral

api_key = "SvjHMorIrdHZgiQmjLLJEYNN1iuj3VN9"
model = "mistral-small-latest"

client = Mistral(api_key=api_key)

chat_response = client.chat.complete(
    model=model,
    messages=[
        {
            "role": "user",
            "content": "Quelle est la couleur du cheval blanc de henri IV?",
        }
    ],
)

print(chat_response.choices[0].message.content)
