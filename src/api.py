from mistralai import Mistral


class LeBot:
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = Mistral(api_key=self.api_key)

    def chat_with_lebot(self, question, context="", req_resp=""):
        model = "mistral-large-latest"
        # add if there is a req_resp to add the result of the req to the context
        chat_response = self.client.chat.complete(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": f"""Tu est un agent de conversation dénommé LeBot,
                    Tu communique avec l'utilisateur, en question réponse. Tu est la partie conversationelle Voici l'historique de vos messages : {context}
                    N'hésite pas à aérer et diversifier tes messages, et mettre des émojis pour que l'utilisateur se sente à l'aise.
                    tu va aider les utilisateur à choisir un film et a lancer un téléchargement. Tu peux si tu le juge nécessaire répondre a l'aide de tes connaissances
                    ou bien lister tout les films déja téléchargés. Voici ce que l'utilisateur a dit: {question}.
                    {f"Pour t'aider a répondre a la question de l'utilisateur j'ai deja effectué une requete qui deverait correspondre à la question de l'utilisateur : {req_resp}" if req_resp else ""}
                    """,
                }
            ],
        )

        return chat_response.choices[0].message.content

    def is_humanity_Question(self, user_prompt, tools):
        model = "mistral-small-latest"
        chat_response = self.client.chat.complete(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": f"""Given the user prompt :{user_prompt}
                    You will tell me if this is a question that can be answered using one of the following tools : {tools}.
                    If the question can be answered by one of the tools, you will answer with "tool", otherwise you will answer with "human".
                    answer taking all the comments and functions of the tools into account.
                    YOU WILL ONLY ANSWER FOLLOWING this json format:
                    """
                    """
                    {
                        "answer": <tool/human>
                        # if tool, you will also provide the tool name, and the function
                        "tool_name": <tool_name>
                        "function": <function_name>
                        # provide the arguments, make them empty if there are none
                        "args": {
                            <arg1>: <value1>,
                            <arg2>: <value2>,
                            ...
                        }
                    }
                    """,
                }
            ],
        )
        print(
            "Mistral has choose the tool to use",
            chat_response.choices[0].message.content,
        )
        return chat_response.choices[0].message.content

    def choose_req(self, user_prompt, tools):
        model = "mistral-small-latest"
        chat_response = self.client.chat.complete(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": f"""
                    Please select the tool that you think is most appropriate to answer the user prompt.
                    YOU WILL ONLY SELECT ONE TOOL, YOU WILL NOT ANSWER THE USER PROMPT.
                    Given the yaml of available tools : "{tools}" as well as the user prompt : "{user_prompt}"
                    You will only answer as a json file with the tool you think is most appropriate and the corresponding args, following the format below:
                    """
                    """
                    {
                        "tool": <tool_name>
                        "args": {
                            <arg1>: <value1>,
                            <arg2>: <value2>,
                            ...
                        }
                    }
                    """,
                }
            ],
        )

        return chat_response.choices[0].message.content

    # Example usage:
    # response = chat_with_lebot("Montre moi la liste des films")
    # print(response)
