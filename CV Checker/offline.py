import streamlit as st
import PyPDF2
import io
import spacy
import re
import pandas as pd

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

# Predefined list of skills (you can expand)
SKILLS = [
    "Python", "Java", "C++", "SQL", "Machine Learning",
    "Deep Learning", "Data Analysis", "Excel", "PowerPoint",
    "Communication", "Teamwork", "Leadership", "Project Management"
]

# Page Config
st.set_page_config(page_title="Offline CV Checker", page_icon="📄", layout="centered")
st.title("Offline CV Checker")
st.markdown("Upload your CV (PDF or TXT) to get a summary and skill extraction.")

# File Upload
uploaded_file = st.file_uploader("Upload your CV (PDF or TXT)", type=["pdf", "txt"])
job_role = st.text_input("Enter the job role you are applying for")
analyze = st.button("Analyze CV")

# Extract text from PDF
def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        if page.extract_text():
            text += page.extract_text() + "\n"
    return text

# Extract text from uploaded file
def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(io.BytesIO(uploaded_file.read()))
    else:
        return uploaded_file.read().decode("utf-8")

# Extract skills from text
def extract_skills(text):
    skills_found = []
    for skill in SKILLS:
        if re.search(r'\b' + re.escape(skill) + r'\b', text, re.I):
            skills_found.append(skill)
    return skills_found

# Extract experiences using simple rules
def extract_experience(text):
    experience = []
    lines = text.split("\n")
    for line in lines:
        if any(word in line.lower() for word in ["experience", "worked", "intern", "project"]):
            experience.append(line.strip())
    return experience

# Analyze CV
if analyze and uploaded_file:
    try:
        file_content = extract_text_from_file(uploaded_file)

        if not file_content.strip():
            st.error("The uploaded file is empty or could not be read.")
            st.stop()

        # Extract skills & experience
        skills_found = extract_skills(file_content)
        experience_found = extract_experience(file_content)

        # Display results
        st.markdown("### ✅ CV Summary & Feedback:")
        st.markdown(f"**Total Skills Found:** {len(skills_found)}")
        st.write(skills_found if skills_found else "No skills found from the predefined list.")

        st.markdown(f"**Experience / Projects Found:**")
        st.write(experience_found if experience_found else "No experience lines found.")

        # Basic suggestions
        st.markdown("### 💡 Suggestions:")
        if job_role:
            st.write(f"- Make sure your CV highlights skills relevant to {job_role}.")
        if len(skills_found) < 3:
            st.write("- Add more relevant skills to strengthen your CV.")
        if len(experience_found) < 2:
            st.write("- Include more projects or work experience.")

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
