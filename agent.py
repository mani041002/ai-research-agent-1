import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

# Load Groq API key
groq_key = os.getenv("GROQ_API_KEY")

# Initialize model
llm = ChatGroq(
    api_key=groq_key,
    model="llama-3.3-70b-versatile"

)

def research(topic):
    try:
        prompt = f"Explain in detail about {topic}"

        response = llm.invoke(prompt)

        # Handle response safely
        if hasattr(response, "content"):
            return response.content
        else:
            return str(response)

    except Exception as e:
        return f"Error: {str(e)}"