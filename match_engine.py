import google.generativeai as genai
import streamlit as st
import numpy as np
from utils.text_utils import clean_text

# Configuring Gemini API key
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Initializing the Gemini model
model = genai.GenerativeModel("gemini-2.5-flash")



def gemini_generate(prompt, temp=0.5):
    """Writing a function that takes a prompt and generates a response using google ai"""
    response = model.generate_content(prompt, generation_config={"temperature": temp})
    return response.text.strip()

#Caching the data to make sure my API calls are low and also so that streamlit keeps my data displayed
@st.cache_data(show_spinner=False)

def get_embedding(text):
    """
    Generate a semantic embedding for the given text using Gemini.
    Embedding will be used to compare the similarity between the JD and the resume.
    """
    text = clean_text(text)
    
    embed_model = genai.embed_content(
        model = "models/gemini-embedding-001", # model to be used for getting the embedding
        content = text,
        task_type = "retrieval_document" # that means we will be using the embedding to compare text
    )

    embedding = np.array(embed_model["embedding"])

    return embedding


def cosine_similarity(vec1, vec2):
    """Calculate cosine similarity between two vectors."""
    
    # Safety check for empty vectors (zeros) to avoid dividing by zero
    if np.all(vec1 == 0) or np.all(vec2 == 0):
        return 0.0
    
    # Cosine Similarity Calculation
    dot_product = np.dot(vec1, vec2)
    norm_resume = np.linalg.norm(vec1)
    norm_jd = np.linalg.norm(vec2)
    
    if norm_resume == 0 or norm_jd == 0:
        return 0.0
        
    similarity = dot_product / (norm_resume * norm_jd)
    
    return similarity

def compute_match_percentage(resume_text, jd_text):
    """Compute similarity score between resume and job description."""
    resume_emb = get_embedding(resume_text)
    jd_emb = get_embedding(jd_text)
    
    similarity = cosine_similarity(resume_emb, jd_emb)
    
    # Convert to percentage
    match_percent = round(similarity * 100, 2)
    
    return match_percent