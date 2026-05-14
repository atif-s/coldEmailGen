import io
import time
import pdfplumber as pp
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from web_scraping import extract_website_data
from dotenv import load_dotenv
import os

load_dotenv("keys.env")
groq_key = os.getenv("GROQ_API_KEY")
_llm_instance = None

def _get_llm():
    global _llm_instance
    if _llm_instance is None:
        _llm_instance = ChatGroq(
            temperature=0,
            groq_api_key=groq_key,
            model_name="openai/gpt-oss-20b",
            max_tokens=3000,
        )
    return _llm_instance



def is_valid_website(text: str) -> bool:
    if not text:
        return False

    cleaned = text.strip().lower()

    if len(cleaned) < 100:
        return False

    job_keywords = [
        "responsibilities",
        "requirements",
        "qualifications",
        "skills",
        "experience",
        'education',
        "job description",
        "description",
        "about the role",
        "submit",
        "what you'll do",
        "what you will do"
    ]

    # Check if at least one strong job keyword exists
    n = 0
    for keywords in job_keywords:
        if keywords in cleaned:
            n+=1
    if(n>=2):
        return True
    return False

def extract_resume_data(source=None) -> str:
    """
    source can be:
    - None (default): reads hardcoded sample file
    - str/Path: reads from file path
    - bytes: reads from uploaded file data
    """
    if source is None:
        return 'Please upload a valid resume.'
    elif isinstance(source, (bytes, bytearray)):
        pdf = pp.open(io.BytesIO(source))
        text = ''
        for page in pdf.pages:
            text += page.extract_text() + '\n'
    elif isinstance(source, str):
        pdf = pp.open(source)
        text = ''
        for page in pdf.pages:
            text += page.extract_text() + '\n'
    else:
        return ''
    return text[:3000] if len(text) > 3000 else text


def is_valid_resume(text: str) -> bool:
    keywords = ["experience", "skills", "education"]
    text_lower = text.lower()
    return all(keyword in text_lower for keyword in keywords)

def generate_email(website_url: str, resume_text: str) -> str:
    prompt = PromptTemplate.from_template("""
    You are given a job posting and a resume.
    Ensure to focus on the text which contains the following:

    - Required skills
    - Preferred skills
    - Required experience
    - Key responsibilities
                                      
    If the website does not explicitly mention any of the above fields, then focus on the job description and try to identify the job title, company name, required skills, experience and responsibilities from there.
    Then internally identify which resume points directly match those.

    Do NOT output this analysis.

    Now write a concise professional email that:
    - Highlights only strong direct matches
    - Uses specific examples
    - Avoids generic statements
    - Sounds confident but not exaggerated

    Rules:
    - 180-220 words
    - Plain text only
    - No markdown
    - No asterisks
    - No preamble or postamble
    - First line should be the following : "Subject : Application for <job title> at <company name>"
    - End with:
    Looking forward to a positive response. Thank you for your time and consideration.

    Divide the output response into small paragraphs each of 70-90 words.
    
    Job Posting:
    {website_data}

    Resume:
    {resume_text}
    """)
    website_text = extract_website_data(website_url)
    if not is_valid_resume(resume_text) and is_valid_website(website_text):
        result = 'Resume is invalid or not uploaded. Please upload a valid resume and try again.'
    
    elif not is_valid_website(website_text) and is_valid_resume(resume_text):
        result = 'Invalid website(Website does not have a job/internship posting). Please try again with a valid job posting URL'
    elif not is_valid_resume(resume_text) and not is_valid_website(website_text):
        result = 'Both resume and website are invalid. Please try again.'
    else:
        response = (prompt | _get_llm()).invoke({
            "website_data": website_text,
            "resume_text": resume_text
        })
        result = response.content
    return result


if __name__ == "__main__":
    import time

    job_posting_url = input("Enter the job posting URL: ")
    start = time.perf_counter()
    resume_text = extract_resume_data("C:/Users/AtifSha/Downloads/sample_resume.pdf")
    website_text = extract_website_data(job_posting_url)
    print()
    print(generate_email(job_posting_url, resume_text))
    end = time.perf_counter()
    print("TIME TAKEN = ", end - start)