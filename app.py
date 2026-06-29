import streamlit as st
import os
from pypdf import PdfReader
from dotenv import load_dotenv
from google import genai
from openai import OpenAI

# Load environment variables
load_dotenv()

# Configure LLM clients
gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
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
        "Format the output beautifully using clean markdown headings and bullet points."
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

# --- Streamlit Premium UI Customization ---
st.set_page_config(page_title="Interview Coach Pro", page_icon="🎯", layout="wide")

# Custom Premium CSS Inject
st.markdown("""
    <style>
    /* Main body adjustments */
    .main {
        background-color: #fcfcfd;
    }
    /* Title and Subtitle styling */
    .main-title {
        font-size: 2.8rem;
        font-weight: 800;
        color: #1E293B;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.1rem;
        color: #64748B;
        margin-bottom: 2rem;
    }
    /* Unique feature metric cards */
    .feature-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        border-left: 5px solid #4F46E5;
        margin-bottom: 15px;
    }
    .feature-card h4 {
        margin: 0 0 5px 0;
        color: #1E293B;
    }
    .feature-card p {
        margin: 0;
        color: #64748B;
        font-size: 0.9rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Application Header
st.markdown("<div class='main-title'>🎯 Interview Coach Pro</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Evolving standard AI mock preparation into a context-driven simulation framework.</div>", unsafe_allow_html=True)

# Sidebar Settings Dashboard
st.sidebar.markdown("### ⚙️ Engine Control Room")
st.sidebar.markdown("Switch model endpoints dynamically on the fly.")
llm_model = st.sidebar.selectbox("Active AI Core", ["Gemini", "OpenAI"])

# Visual Feature Highlights in Sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("### 🛠️ Active Subsystems")
st.sidebar.markdown("""
<div class='feature-card'>
    <h4>Resume Parser</h4>
    <p>Using structural PDF stream segmentation</p>
</div>
<div class='feature-card'>
    <h4>Gap Analyzer</h4>
    <p>Cross-examining matrix requirements</p>
</div>
""", unsafe_allow_html=True)

# Main Application Form Columns
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("### 📁 1. Candidate Context")
    st.caption("Upload your latest industry resume profile.")
    uploaded_file = st.file_uploader("", type=["pdf"], key="resume_uploader")
    
with col2:
    st.markdown("### 💼 2. Target Framework")
    st.caption("Paste the core requirements or job script details.")
    job_desc = st.text_area("", height=140, placeholder="Paste job requirements here...", key="jd_input")

st.markdown("---")

# Centering the submission action
left_spacer, center_button, right_spacer = st.columns([2, 1, 2])

with center_button:
    run_analysis = st.button("🚀 Analyze & Generate", type="primary", use_container_width=True)

if run_analysis:
    if uploaded_file and job_desc:
        with st.spinner("Executing structural semantic comparison..."):
            resume_text = extract_text_from_pdf(uploaded_file)
            questions = generate_tailored_questions(llm_model, resume_text, job_desc)
            
            st.toast("Analysis Successful!", icon="✅")
            
            # Display results in a high-contrast container block
            st.markdown("### 📋 Deep-Dive Evaluation Path")
            with st.container(border=True):
                st.markdown(questions)
    else:
        st.error("Execution failed: Please upload a resume PDF and supply a valid job target.")