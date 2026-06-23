import streamlit as st
import google.generativeai as genai

genai.configure(api_key = st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")

def gemini_generate(prompt, temp = 0.5):
    """Writing a function that takes a prompt and generates a response using google ai"""
    response = model.generate_content(prompt, generation_config={"temperature": temp})
    return response.text.strip()

def interview_questions(resume_text, jd_text):
    """
    Generates interview questions based on the jd and experience of the user.
    """

    prompt = f"""
You are an expert Hiring Manager and Technical Interviewer. 

Review the Candidate's Resume and the Job Description (JD) below.
Your goal is to generate 10 high-impact interview questions that ruthlessly test the candidate's fit for this specific role.

Resume:
{resume_text}

Job Description:
{jd_text}

### Instructions for Question Generation:
1. **Avoid Generics:** Do not ask generic questions like "What is your greatest weakness?".
2. **Be Specific:** Reference specific projects or tools from the Resume and ask how they apply to the problems listed in the JD.
3. **Structure the Output:** Group the questions into these three categories:
    * **3 Technical Deep-Dives:** Test the specific hard skills required in the JD (e.g., Python, AWS, SQL) based on the candidate's claimed expertise.
    * **4 Behavioral/Experience:** Ask about specific challenges they faced in their previous roles (look at their bullet points) and how those prepare them for the responsibilities in this JD.
    * **3 Situational/Strategic:** "Suppose you are hired and face [Specific Challenge from JD]. How would you approach it?"

### Output Format:
For each question, provide:
* **The Question:** (Crisp, direct, and challenging)
* **The Intent:** (One sentence explaining *why* this question matters for this specific JD)
"""
    
    response = gemini_generate(prompt)

    return response