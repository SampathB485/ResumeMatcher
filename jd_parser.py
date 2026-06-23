import re
from utils.skill_list import TECH_SKILLS, SOFT_SKILLS

def clean_text(text):
    """Basic text cleaning for Job Description"""
    text = re.sub(r'\s+', ' ', text)  # Remove extra spaces/newlines
    text = re.sub(r'[^\w\s.,-]', '', text)  # Remove unwanted special chars
    return text.strip().lower()


def extract_sections(text):
    """Try to split JD into sections based on common headings"""
    sections = {}
    patterns = {
        "responsibilities": r"(responsibilities|what you'll do|your role).*?(?=(requirements|skills|required|$))",
        "requirements": r"(requirements|qualifications|what you'll need).*?(?=(responsibilities|skills|$))",
        "skills": r"(skills|technologies|tools).*?(?=(requirements|responsibilities|$))"
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            sections[key] = match.group().strip()
        else:
            sections[key] = ""
    return sections


def extract_skills(text):
    """Extract skills from JD based on predefined list"""
    text_lower = text.lower()
    found_skills = []

    for skill in TECH_SKILLS + SOFT_SKILLS:
        if skill.lower() in text_lower:
            found_skills.append(skill)

    return list(set(found_skills))  # Remove duplicates


def parse_jd(raw_text):
    """Main function to process JD"""
    cleaned = clean_text(raw_text)
    sections = extract_sections(cleaned)
    skills = extract_skills(cleaned)
    
    return {
        "clean_text": cleaned,
        "sections": sections,
        "skills": skills
    }



