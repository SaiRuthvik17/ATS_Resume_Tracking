from dotenv import load_dotenv

load_dotenv()

import streamlit as st
st.set_page_config(page_title="Resume Expert")


import os
from PIL import Image
import io
import pdf2image
import base64
import fitz
import PyPDF2
import sys
import os
import re

sys.stderr = open(os.devnull, "w")

import openai  
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to generate response using OpenAI
def get_openai_response(input, pdf_content, prompt):
    messages = [
        {"role": "system", "content": "You are a helpful and experienced ATS (Applicant Tracking System) expert."},
        {"role": "user", "content": input},
        {"role": "user", "content": f"Resume Content: {pdf_content}"},
        {"role": "user", "content": prompt}
    ]

    # Call OpenAI ChatCompletion
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7,
        max_tokens=2000
    )

    return response['choices'][0]['message']['content']

# Function to process uploaded PDF
def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text_parts = [page.extract_text() for page in pdf_reader.pages if page.extract_text()]
        raw_text = " ".join(text_parts)  # Combine text from all pages

        #Regex cleaning for Better Readability
        clean_text = re.sub(r'\s+', ' ', raw_text)  # Remove extra spaces/newlines
        clean_text = re.sub(r'([a-z])-\s([a-z])', r'\1\2', clean_text, flags=re.I)  # Fix broken words
        clean_text = re.sub(r'[^a-zA-Z0-9@,.:\-\s]', '', clean_text)  # Remove unwanted symbols
        clean_text = clean_text.strip()  # Remove leading/trailing spaces

        return clean_text
    else:
        raise FileNotFoundError("No file uploaded")

## Streamlit App
st.header("ATS Resume Tracking")
st.subheader('This application helps you review your resume based on the job description')
input_text = st.text_input("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your Resume(PDF)...", type=["pdf"])
pdf_content = ""

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell Me About the Resume")
submit2 = st.button("How Can I Improvise my Skills")
submit3 = st.button("What are the Keywords That are Missing")
submit4 = st.button("Percentage match")
input_promp = st.text_input("Queries: Feel Free to Ask here")
submit5 = st.button("Answer My Query")

# Prompts
input_prompt1 = """
You are an experienced Technical Human Resource Manager. Your task is to review the provided resume against the job description. 
Please share your professional evaluation on whether the candidate's profile aligns with the role. 
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt2 = """
You are a Technical Human Resource Manager with expertise in data science, front end developer, full stack developer, java developer, QA automation. business analyst, data analyst, data engineer, and all other technological fields.
Your role is to scrutinize the resume in light of the job description provided. 
Share your insights on the candidate's suitability for the role from an HR perspective. 
Additionally, offer advice on enhancing the candidate's skills and identify areas where improvement is needed.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science, , front end developer, full stack developer, java developer, QA automation. business analyst, data analyst, data engineer, all other technological fields, and ATS functionality. 
Your task is to evaluate the resume against the provided job description. Assess the compatibility of the resume with the role. 
List the keywords that are missing and provide recommendations for enhancing the candidate's skills.
"""

input_prompt4 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science, , front end developer, full stack developer, java developer, QA automation. business analyst, data analyst, data engineer, all other technological fields, and ATS functionality. 
Your task is to evaluate the resume against the provided job description. Calculate the percentage match between the resume and the job description. 
First, provide the match percentage, then list missing keywords, and finally share your overall thoughts.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_openai_response(input_text, pdf_content, input_prompt1)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload a PDF file to proceed.")

elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_openai_response(input_text, pdf_content, input_prompt2)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload a PDF file to proceed.")

elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_openai_response(input_text, pdf_content, input_prompt3)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload a PDF file to proceed.")

elif submit4:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_openai_response(input_text, pdf_content, input_prompt4)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload a PDF file to proceed.")

elif submit5:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_openai_response(input_text, pdf_content, input_promp)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload a PDF file to proceed.")
