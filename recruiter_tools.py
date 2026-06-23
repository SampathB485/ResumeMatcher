import google.generativeai as genai
import streamlit as st
import re
import json

# Configure Gemini API key
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

def gemini_generate(prompt, temp=0.5):
    """Writing a function that takes a prompt and generates a response using google ai"""
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt, generation_config={"temperature": temp})
    return response.text.strip()


def extract_job_info(jd_text):
    """Extract job title, company name, and any stated salary from a job description using Gemini."""

    # Check session state first to avoid repeated API calls
    if "jd_info_extracted" in st.session_state and st.session_state.jd_info_extracted:
        return (
            st.session_state.title,
            st.session_state.company,
            st.session_state.stated_salary
        )

    prompt = f"""
Analyze the following job description and extract these three fields.
If a field is not found, return "Not Found" for that field.

Job Description:
{jd_text}

Return ONLY a valid JSON object with these exact keys, no other text:
{{
    "job_title": "the exact job title",
    "company_name": "the company name",
    "stated_salary": "the salary/compensation if explicitly mentioned, otherwise Not Found"
}}
"""

    try:
        response = gemini_generate(prompt, temp=0.1)
        # Clean up response in case Gemini wraps it in markdown code blocks
        response = response.strip()
        response = re.sub(r'^```json\s*', '', response)
        response = re.sub(r'\s*```$', '', response)

        parsed = json.loads(response)
        title = parsed.get("job_title", "Not Found")
        company = parsed.get("company_name", "Not Found")
        stated_salary = parsed.get("stated_salary", "Not Found")
    except (json.JSONDecodeError, Exception):
        title = "Not Found"
        company = "Not Found"
        stated_salary = "Not Found"

    # Store in session state
    st.session_state.title = title if title != "Not Found" else "[Job Title]"
    st.session_state.company = company if company != "Not Found" else "[Company Name]"
    st.session_state.stated_salary = stated_salary if stated_salary != "Not Found" else ""
    st.session_state.jd_info_extracted = True

    return st.session_state.title, st.session_state.company, st.session_state.stated_salary


def generate_recruiter_message(jd_text, tone="Warm"):
    """Generate a short LinkedIn message to a recruiter."""
    job_title, company_name, _ = extract_job_info(jd_text)
    prompt = f"""
You are an expert career networker who writes messages that get replies.

Write a {tone.lower()} LinkedIn connection message (under 300 characters) to a recruiter regarding the {job_title} role at {company_name}.

Context from Job Description:
{jd_text}

### STRICT RULES FOR "HUMAN" TONE:
1. **NO ROBOTIC OPENERS:** Do NOT use "I hope this finds you well," "I am writing to express interest," or "I was impressed by." Start directly with why the specific team or project looks interesting.
2. **BE SPECIFIC:** Mention ONE specific technology, project, or goal from the JD that excites you. Do not just say "your company values."
3. **USE CONTRACTIONS:** Use "I'm," "I'd," "It's" to sound natural.
4. **LOW-FRICTION CLOSE:** Do not ask for a "30-minute meeting." Ask a simple "Yes/No" question or just ask to connect to follow their updates.

### EXAMPLE OF WHAT I WANT:
"Hi [Name], I saw {company_name} is moving into [Topic]—as a dev who loves [Skill], that caught my eye immediately. I'd love to connect and keep up with the team's work."

Generate the message now.
"""

    response = gemini_generate(prompt)
    return response


def generate_cold_email(jd_text):
    """Generate a cold email to the recruiter or company."""
    job_title, company_name, _ = extract_job_info(jd_text)
    prompt = f"""
You are an expert career coach who writes high-converting, human-sounding emails.

Draft a warm, personal cold email for a candidate applying to:
Role: {job_title}
Company: {company_name}

Using this Job Description as context:
{jd_text}

### Instructions for Tone & Style:
1. **Subject Line:** Make it intriguing but casual (e.g., "Question about the {job_title} role" or "{company_name} + {job_title}"). Avoid stiff phrases like "Application for...".
2. **The Opening:** Do NOT start with "I hope this email finds you well" or "I am writing to apply." Start with a genuine compliment about the company or a specific detail from the job description that excited the candidate.
3. **The Middle:** connect ONE key skill from the JD to the candidate's experience casually. Show, don't just tell.
4. **The Close (Crucial):** Make the call-to-action "low friction." Do not ask for a 30-minute interview. Ask for a quick piece of advice or a simple "yes/no" question to gauge interest.
5. **Human Touch:** Use contractions (e.g., "I'm" instead of "I am"). Sound enthusiastic but not desperate.

Keep it under 150 words. The goal is to start a conversation, not just submit a resume.
"""

    response = gemini_generate(prompt)
    return response


def suggest_contact_titles(jd_text):
    """Suggest typical people to reach out to in the company."""
    job_title, company_name, _ = extract_job_info(jd_text)
    prompt = f"""
Given the job title "{job_title}", in the company {company_name}, list 5 relevant job titles or roles of people
in a company that the candidate should reach out to for the best chance of being hired.
Example format: Recruiter, Hiring Manager, Vice President of Engineering, Team Lead, CTO
"""

    response = gemini_generate(prompt, temp=0.3)

    if response:
        titles_list = [title.strip() for title in response.split(',')]
        return titles_list
    else:
        return []


def estimate_salary(jd_text, location="Canada"):
    """Estimate salary range — uses stated salary from JD if available, otherwise asks Gemini to estimate."""
    job_title, company_name, stated_salary = extract_job_info(jd_text)

    # If the JD already contains salary info, return it directly
    if stated_salary:
        return f"Salary listed in JD: {stated_salary}"

    # Otherwise, estimate using Gemini
    prompt = f"""
You are a salary estimation assistant with deep knowledge of the {location} job market.

Analyze the following inputs:
Role: {job_title}
Company: {company_name}
Location: {location}

Job Description for context:
{jd_text}

### INSTRUCTIONS:
1. If the Role is "[Job Title]" or the Company is "[Company Name]", still try to estimate based on the skills and seniority level described in the Job Description.
2. Look at the required experience, technologies, and responsibilities to infer the seniority level (Junior / Mid / Senior / Lead).
3. Provide a realistic salary range for {location}.

### OUTPUT FORMAT:
"$MINk-$MAXk CAD (Seniority Level). One-line explanation of factors."

Example: "$85k-$110k CAD (Mid-Level). Based on 3-5 years Python/AWS experience at a mid-size fintech."
"""

    response = gemini_generate(prompt, temp=0.4)
    return response