import google.generativeai as genai
import streamlit as st


# Configuring Gemini key
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Initializing the Gemini model
model = genai.GenerativeModel("gemini-2.5-flash")

def gemini_generate(prompt, temp=0.5, max_tokens=8192):
    """Writing a function that takes a prompt and generates a response using google ai"""
    response = model.generate_content(
        prompt, 
        generation_config={
            "temperature": temp,
            "max_output_tokens": max_tokens
        }
    )
    return response.text.strip()

def rewrite_resume(resume_text, jd_text, target_match=0.8):
    """
    Rewrites the resume to match the job description.
    """
    prompt = f"""
Act as an expert Resume Optimization Engine.

Your Task: Rewrite the candidate's resume to target the specific Job Description (JD) below, ensuring an ATS match score of {int(target_match * 100)}%+.

### INPUT DATA:
RESUME:
{resume_text}

JOB DESCRIPTION:
{jd_text}

### STRICT CONSTRAINTS (READ CAREFULLY):
1. **NO CONVERSATIONAL FILLER:** Do not output sentences like "Here is the updated resume" or "I have optimized it." Output **ONLY** the resume content.
2. **ZERO DATA LOSS:** You MUST include ALL sections from the original resume (Contact Info, Education, Experience, Projects, Skills). Do not summarize or truncate older roles. Do not skip any job, project, or education entry. Every single entry in the original must appear in the output.
3. **FORMATTING:** Use valid Markdown.
   - Use `##` for Section Headers (e.g., ## EXPERIENCE).
   - Use `###` for Job Titles/Companies.
   - Use `-` for bullet points.
   - Use `**text**` for bold emphasis on key terms.
4. **KEYWORD OPTIMIZATION:** Swap generic verbs with specific keywords from the JD where truthfully applicable.
5. **LENGTH:** The output MUST be at least as long as the input resume. Do not shorten it. If the original has 5 jobs, the output must have 5 jobs. If it has 3 projects, the output must have 3 projects.
6. **COMPLETENESS CHECK:** Before finishing, count the number of Experience entries, Education entries, and Project entries in the original. Your output MUST have the same count for each.

### OUTPUT FORMAT:
Output the full resume content in Markdown. Do not wrap it in code blocks. Do not add any commentary before or after.
"""

    # Using high token limit to prevent truncation on 2-page resumes
    response = gemini_generate(prompt, temp=0.2, max_tokens=8192)
    
    return response