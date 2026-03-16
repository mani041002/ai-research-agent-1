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
import requests
from bs4 import BeautifulSoup

def scrape_web(topic):
    url = f"https://www.google.com/search?q={topic}"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    results = []
    for g in soup.select("h3"):
        results.append(g.text)

    return results[:5]

def research(topic):
    try:
        # Get web data
        scraped_data = scrape_web(topic)

        # Convert list to text
        context = " ".join(scraped_data)

        # Prompt with web context
        prompt = f"""
        Research the topic: {topic}

        Here are some web search results:
        {context}

        Based on these, write a clear research explanation.
        """

        response = llm.invoke(prompt)

        if hasattr(response, "content"):
            return response.content
        else:
            return str(response)

    except Exception as e:
        return f"Error: {str(e)}"