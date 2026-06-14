from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from test import extract_resume_data, generate_email
from starlette.concurrency import run_in_threadpool
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/generate-email")
async def generate_email_endpoint(job_url: str = Form(...), resume: UploadFile = File(...)):

    raw_bytes = await resume.read()
    resume_text = extract_resume_data(source=raw_bytes)
    email = await run_in_threadpool(generate_email,job_url,resume_text)
    return {'email' : email}
