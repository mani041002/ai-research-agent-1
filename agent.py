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

    for g in soup.select(".tF2Cxc"):
        title = g.select_one("h3")
        snippet = g.select_one(".VwiC3b")

        if title and snippet:
            results.append({
                "title": title.text,
                "snippet": snippet.text
            })

    return results[:5]

def research(topic):
    try:
        web_data = scrape_web(topic)

        formatted_data = "\n".join(
            [f"{item['title']}: {item['snippet']}" for item in web_data]
        )

        prompt = f"""
        Use ONLY the below web search results to answer.

        {formatted_data}

        Question: {topic}

        Give a factual and up-to-date answer.
        """

        response = llm.invoke(prompt)

        return response.content

    except Exception as e:
        return f"Error: {str(e)}"