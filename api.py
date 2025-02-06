from mistralai import Mistral


def chat_with_lebot(question, context=""):
    api_key = "SvjHMorIrdHZgiQmjLLJEYNN1iuj3VN9"
    model = "mistral-large-latest"

    client = Mistral(api_key=api_key)

    chat_response = client.chat.complete(
        model=model,
        messages=[
            {
                "role": "user",
                "content": f"""Tu est un agent de conversation dénommé LeBot,
                Tu communique avec l'utilisateur, en question réponse. Tu est la partie bot Voici l'historique de vos messages : {context}
                N'hésite pas à aérer et diversifier tes messages, et mettre des émojis pour que l'utilisateur se sente à l'aise.
                tu va aider les utilisateur à choisir un film et a lancer un téléchargement. Tu peux si tu le juge nécessaire répondre a l'aide de tes connaissances
                ou bien lister tout les films déja téléchargés. Voici ce que l'utilisateur a dit: {question}.""",
            }
        ],
    )

    return chat_response.choices[0].message.content


# Example usage:
# response = chat_with_lebot("Montre moi la liste des films")
# print(response)
