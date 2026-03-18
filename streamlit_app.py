import streamlit as st
import requests
from bs4 import BeautifulSoup
from langchain_groq import ChatGroq

# Load API key from secrets
groq_key = st.secrets["GROQ_API_KEY"]

llm = ChatGroq(
    api_key=groq_key,
    model="llama-3.3-70b-versatile"
)

def scrape_web(topic):
    url = f"https://html.duckduckgo.com/html/?q={topic}"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    results = []
    for r in soup.select(".result__snippet"):
        results.append(r.get_text())

    return results[:5]

def research(topic):
    web_data = scrape_web(topic)

    if not web_data:
        return "No web data found."

    context = "\n".join(web_data)

    prompt = f"""
    Use this web data to answer:

    {topic}

    Data:
    {context}
    """

    response = llm.invoke(prompt)
    return response.content


# UI
st.title("🤖 AI Research Agent")

topic = st.text_input("Enter topic")

if st.button("Research"):
    if topic:
        with st.spinner("Searching..."):
            result = research(topic)
            st.write(result)
    else:
        st.warning("Enter a topic")