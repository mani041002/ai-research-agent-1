import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

# Load Groq API key
groq_key = os.getenv("GROQ_API_KEY")

# Initialize model
llm = ChatGroq(
    api_key=groq_key,
    model="llama-3.3-70b-versatile",
    temperature=0.3   # more factual, less random
)
import requests
from bs4 import BeautifulSoup



from tavily import TavilyClient
import os

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def scrape_web(topic):
    try:
        response = tavily.search(
            query=topic,
            max_results=5,
            include_answer=True
        )

        results = []

        # ✅ Add main answer (VERY IMPORTANT)
        if response.get("answer"):
            results.append(response["answer"])

        # ✅ Add content + title
        for r in response["results"]:
            text = f"{r.get('title', '')} - {r.get('content', '')}"
            results.append(text)

        return results

    except Exception as e:
        print(e)
        return []

def rag_pipeline(topic):
    try:
        # 1. Get web data
        web_data = scrape_web(topic)

        if not web_data:
            return "No data found from web."

        # 2. Convert to text
        text_data = "\n".join(web_data)

        # 3. Split into chunks
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        docs = splitter.create_documents([text_data])

        # 4. Embeddings
        embeddings = HuggingFaceEmbeddings()

        # 5. Store in FAISS
        db = FAISS.from_documents(docs, embeddings)

        # 6. Retrieve relevant docs
        retriever = db.as_retriever()
        relevant_docs = retriever.invoke(topic)

        context = "\n".join([doc.page_content for doc in relevant_docs])

        # 7. Ask LLM with context
        prompt = f"""
        Answer ONLY using this context:

        {context}

        Question: {topic}
        """

        response = llm.invoke(prompt)

        return response.content

    except Exception as e:
        return f"Error: {str(e)}"

def research(topic):
    return rag_pipeline(topic)