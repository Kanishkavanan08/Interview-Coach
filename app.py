import streamlit as st
import os
from pypdf import PdfReader
from dotenv import load_dotenv
import google.genai as genai
from openai import OpenAI

# Load environment variables
load_dotenv()

# Configure LLM clients
gemini_client= genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_text_from_pdf(pdf_file):
    """Extracts plain text from an uploaded PDF file."""
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def generate_tailored_questions(llm_choice, resume_text, job_description):
    """Generates tailored interview questions based on Resume and JD gaps."""
    system_prompt = (
        "You are an expert technical recruiter. Analyze the candidate's Resume and the target Job Description. "
        "Identify potential gaps, weak points, or standout strengths in the resume relative to the job. "
        "Generate 3 highly tailored, specific interview questions that test these gaps or probe deeper into relevant projects. "
        "Format the output clearly as a list."
    )
    
    user_prompt = f"### JOB DESCRIPTION ###\n{job_description}\n\n### CANDIDATE RESUME ###\n{resume_text}"

    if llm_choice == "Gemini":
         response = gemini_client.models.generate_content(
        model="gemini-1.5-flash",
        contents=user_prompt,
        config={"system_instruction": system_prompt}
    )
         return response.text
        
    elif llm_choice == "OpenAI":
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        return response.choices[0].message.content
    
    return "Selected model configuration missing."

# --- Streamlit UI Setup ---
st.set_page_config(page_title="AI Interview Coach Pro", page_icon="🎯", layout="wide")

st.title("🎯 AI Interview Coach Pro")
st.caption("A multi-LLM powered, resume-tailored interview preparation assistant.")

# Sidebar Settings
st.sidebar.header("Configuration")
llm_model = st.sidebar.selectbox("Choose AI Engine", ["Gemini", "OpenAI"])

# Main Interface Layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Your Background")
    uploaded_file = st.file_uploader("Upload your Resume (PDF format)", type=["pdf"])
    
with col2:
    st.subheader("2. Target Role")
    job_desc = st.text_area("Paste the Target Job Description here", height=150)

if st.button("Generate Tailored Interview Questions", type="primary"):
    if uploaded_file and job_desc:
        with st.spinner("Analyzing resume against job description..."):
            resume_text = extract_text_from_pdf(uploaded_file)
            questions = generate_tailored_questions(llm_model, resume_text, job_desc)
            
            st.success("Analysis Complete!")
            st.markdown("### 📋 Recommended Focus Questions")
            st.write(questions)
    else:
        st.error("Please provide both your resume and the job description to continue.")