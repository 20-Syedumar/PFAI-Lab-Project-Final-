import streamlit as st
import PyPDF2
import io
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page Config
st.set_page_config(page_title="CV Checker", page_icon="📃", layout="centered")

# App Title
st.title("CV Checker")
st.markdown("Upload a PDF or TXT file to get a CV summary using OpenAI.")

# Load API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# File Upload
uploaded_file = st.file_uploader("Upload your CV (PDF or TXT)", type=["pdf", "txt"])
job_role = st.text_input("Enter the job role you are applying for")
analyze = st.button("Analyze CV")

# PDF Text Extraction
def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        if page.extract_text():
            text += page.extract_text() + "\n"
    return text

# File Text Extraction
def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(io.BytesIO(uploaded_file.read()))
    else:
        return uploaded_file.read().decode("utf-8")

# Main Logic
if analyze and uploaded_file:
    try:
        file_content = extract_text_from_file(uploaded_file)

        if not file_content.strip():
            st.error("The uploaded file is empty or could not be read.")
            st.stop()

        prompt = f"""
Please analyze the following CV and provide a summary.

Focus on the following aspects:
1. Content clarity and impact
2. Skills presentation
3. Experience descriptions
4. Specific improvements for {job_role if job_role else "general job applications"}

CV Content:
{file_content}
"""

        # Create OpenAI Client
        client = OpenAI(api_key=OPENAI_API_KEY)

        # NEW API RESPONSE FORMAT ✅
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt,
            max_output_tokens=800,
        )

        # Display Output
        st.markdown("### ✅ CV Summary & Feedback:")
        st.markdown(response.output_text)

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
