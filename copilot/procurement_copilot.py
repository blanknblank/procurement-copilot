from ollama import chat

def ask_copilot(question, context):

    prompt = f"""
    You are a procurement analyst.

    Use the analytics information below.

    {context}

    Question:
    {question} 
    """

    response = chat(
        model="llama3.2:3b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]