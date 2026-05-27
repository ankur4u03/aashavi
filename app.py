from google import genai

# API KEY
client = genai.Client(api_key="AIzaSyAxk68b44Dof-PWUjir9Sm3KBp2XE7hBcU")

print("Gemini AI Chatbot Started!")
print("Type 'exit' to close.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Chatbot Closed.")
        break

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_input
        )

        print("\nAI:", response.text)
        print()

    except Exception as e:
        print("Error:", e)