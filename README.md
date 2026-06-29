# 🎯 Interview Coach

An advanced AI-powered mock interview simulator built to bridge the gap between candidates and their target roles. This platform evolves standard AI prompting into a context-aware simulation environment.

## 🚀 Features
* **Context-Aware Analysis:** Dynamically parses complex PDF resumes and matches them against target Job Descriptions.
* **Gap-Analysis Logic:** Automatically detects missing skill matches or weak spots to curate specialized evaluation tracks.
* **Multi-LLM Integration:** Built on a flexible architecture allowing users to alternate between **Google Gemini (using the updated `google-genai` SDK)** and **OpenAI GPT** models.
* **Interactive UI:** A clean, responsive dashboard designed entirely using Streamlit.

## 🛠️ Tech Stack
* **Frontend/Framework:** Streamlit
* **AI Orchestration:** Google GenAI SDK (`gemini-1.5-flash`), OpenAI API (`gpt-4o-mini`)
* **File Processing:** PyPDF
* **Environment Management:** Python-dotenv

## ⚙️ Local Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Kanishkavanan08/Interview-Coach.git](https://github.com/Kanishkavanan08/Interview-Coach.git)
   cd Interview-Coach