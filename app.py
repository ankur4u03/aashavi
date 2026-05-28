from groq import Groq

# API KEY
import os
from groq import Groq

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)
print("🚀 Groq AI Chatbot Started!")
print("Type 'exit' to close.\n")

while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Chatbot Closed.")
        break

    try:

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": user_input
                }
            ],
            temperature=0.7,
            max_tokens=1024
        )

        reply = completion.choices[0].message.content

        print("\nAI:", reply)
        print()

    except Exception as e:
        print("Error:", e)