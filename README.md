# 📧 Cold E-Mail Generator

An AI-powered tool that generates personalized cold emails for job and internship applications. Just paste a job posting URL and upload your resume — the website does the rest. 
Try it out : [text](https://cold-email-gen.netlify.app/)
---

## How It Works

1. **Enter the job/internship posting URL** — the app scrapes the page to extract relevant details about the role and company
2. **Upload your resume** (PDF format) — your skills and experience are extracted automatically
3. **Click Generate** — a tailored cold email is crafted based on your resume and the job posting
OpenAI's 20b parameter model has been used for email generation.
---

## Tech Stack

**Backend**
- [FastAPI](https://fastapi.tiangolo.com/)
- [LangChain](https://www.langchain.com/) + [Groq](https://groq.com/) — LLM-powered email generation. Groq is used for quick LLM inference
- [pdfplumber](https://github.com/jsvine/pdfplumber) — Resume PDF parsing
- [Apify](https://apify.com/) — Web scraping for job postings. Standard Python libraries do not dynamically scrape website data.
- [Render](https://render.com/) — Backend hosting

**Frontend**
- HTML, CSS, JavaScript
- [Netlify](https://netlify.com/) — Frontend hosting

---

## Getting Started

### Prerequisites
- Python 3.11+
- API keys for Groq and Apify

### Installation

```bash
git clone https://github.com/atif-s/cold-email-generator.git
cd cold-email-generator
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the root directory:

```
GROQ_API_KEY=your_groq_api_key
APIFY_API_TOKEN=your_apify_token
```

### Run Locally

```bash
uvicorn backendig:app --reload
```

Then open `index.html` in your browser or serve it with:

```bash
python -m http.server 8080
```

---

## 📁 Project Structure

```
├── backendig.py               # FastAPI app and routes
├── test.py               # Resume extraction and email generation logic
├── web_scraping.py       # Job posting scraper
├── requirements.txt      # Python dependencies
├── runtime.txt           # Python version for Render
├── index.html            # Frontend UI
├── style.css             # Frontend design
├── logic.js              # Frontend logic
└── .env                  # API keys (not committed onto the repo)
```

---

## 🔒 Notes/Disclaimer

- The backend is hosted on Render (free tier may sleep after inactivity) which may lead to the website taking about a minute to give the output.
