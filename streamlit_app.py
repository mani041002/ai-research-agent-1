import streamlit as st
import requests

# Page config
st.set_page_config(
    page_title="AI Research Agent",
    page_icon="🤖",
    layout="centered"
)

# Title
st.title("🤖 AI Research Agent")
st.markdown("Research any topic using AI + RAG")

# Sidebar
st.sidebar.header("About")
st.sidebar.write("""
This AI agent researches any topic using:
- FastAPI backend
- RAG (FAISS + embeddings)
- Tavily web search
- Groq LLM
""")

st.sidebar.info("Enter a topic and click Research")

# Input
topic = st.text_input("🔍 Enter a topic to research")

# Button
if st.button("🚀 Research"):

    if topic.strip() == "":
        st.warning("Please enter a topic")

    else:
        with st.spinner("Researching... please wait..."):

            try:
                # 🔥 LOCAL BACKEND URL
                url = "http://127.0.0.1:8000/research"

                response = requests.get(
                    url,
                    params={"topic": topic},
                    timeout=60
                )

                # 🔍 DEBUG INFO

                st.write("Raw Response:", response.text)

                if response.status_code == 200:
                    data = response.json()

                    st.success("Research Complete")

                    st.subheader("📚 AI Research Result")
                    st.write(data.get("research", "No data found"))

                else:
                    st.error("❌ Server returned an error")

            except requests.exceptions.ConnectionError:
                st.error("❌ Backend server not running. Start FastAPI first.")

            except requests.exceptions.Timeout:
                st.error("⏳ Request timed out. Try again.")

            except Exception as e:
                st.error(f"⚠️ Error: {str(e)}")