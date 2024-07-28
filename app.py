from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
from PIL import Image
import pdf2image
import google.generativeai as genai
import base64
import io

genai.configure(api_key=os.getenv("GOOGLE_API_KEY")) # GET ENVIRONMENT VARAIABLE ALONG WITH GOOGLE API KEY
 
def get_gemini_response(input,pdf_content,prompt): # 1. what is the input 2. create pdf to image 3. prompt like how this specific google gemini pro needs to behave like
    # model = genai.GenerativeModel('gemini-pro-vision')
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([input,pdf_content[0],prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    ## convert the pdf to image
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        
        first_page = images[0]
        
        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue() # take all the images convert into bytes and then save this inthe form of image and then turn this pdf part and finally returned all the pdf parts 

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
# streamlit app

st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")

input_text = st.text_area("Job Description: ",key="input")
uploaded_file = st.file_uploader("Upload Your Resume (PDF)...",type=['pdf'])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button('Tell Me About the Resume')

submit2 = st.button("How Can I Improvise My Skills") 

# submit3 = st.button("What are the Keywords That Are Missing")

submit4 = st.button("Percentage Match") 


input_prompt1 = """
 You are an experienced HR with Tech Experience in the field of any one job role from Data Science or Full Stack Web Development or Big Data Engineering or DEVOPS or Data Analyst ,your task is to review the provided resume against the job description for these profiles. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

# input_prompt2 = """
# You are an Technical Human Resource Manager with expertise in Data Science,Full Stack Web Development,Big Data Engineering,DEVOPS,Data Analyst, your role is to scrutinize the resume in light of the job description provided.
# Share your insights on the candidate's suitability for the role from an HR perspective.
# Additionally, offer advice on enhancing the candidate's skills and identify areas
# """

input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of any one job role Data Science,Full Stack Web Development,Big Data Engineering,DEVOPS,Data Analyst and deep ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("The Response is: ")
        st.write(response)
    else:
        st.write("Please Upload the Resume")
        
elif submit4:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3,pdf_content,input_text)
        st.subheader("The Response is: ")
        st.write(response)
    else:
        st.write("Please Upload the Resume")
