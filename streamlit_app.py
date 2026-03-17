import streamlit as st
import requests

# Page configuration
st.set_page_config(
    page_title="AI Research Agent",
    page_icon="🤖",
    layout="centered"
)

# Title
st.title("🤖 AI Research Agent")
st.markdown("Research any topic using AI")

# Sidebar
st.sidebar.header("About")
st.sidebar.write(
    """
    This AI agent researches any topic using an AI model.

    Built with:
    - FastAPI
    - Streamlit
    - Groq AI
    """
)

st.sidebar.info("Enter a topic and click Research")

# Input section
topic = st.text_input("🔍 Enter a topic to research")

# Button
if st.button("🚀 Research"):

    if topic == "":
        st.warning("Please enter a topic")
    else:

        with st.spinner("Researching... please wait..."):

            try:
                response = requests.get(
                    "https://ai-research-agent-l3.onrender.com/research",
                    params={"topic": topic}
                )


                if response.status_code == 200:
                    data = response.json()

                    st.success("Research Complete")

                    st.subheader("📚 AI Research Result")
                    st.write(data["research"])

                else:
                    st.error("Server returned an error")

            except Exception as e:
                st.error("Backend server not running")