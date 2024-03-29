import base64
import streamlit as st
import io
from PIL import Image
import pdf2image
from django.http import JsonResponse
from dotenv import load_dotenv
import google.generativeai as genai
from django.views.decorators.csrf import csrf_exempt

load_dotenv()

genai.configure(api_key="AIzaSyA3nWZeFQCagPfHR86o0f6kZnD6invO0Bc")

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

@csrf_exempt
def MatchingRate(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['resume']
        input_text = """
        1. Develop and implement innovative blockchain solutions using your expertise in blockchain technology and C++ programming
        2. Collaborate with cross-functional teams to design, develop, and deploy decentralized applications (dApps) on the Ethereum platform
        3. Utilize your knowledge of GNU Octave to analyze complex data sets and provide insights for optimizing blockchain protocols
        """

        input_prompt = """
        You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of Full Stack Development and ATS functionality, 
        your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
        the job description. output should come as a one and only percentage.
        """

        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt)

        return JsonResponse({'message': 'File uploaded successfully', 'rate': response})
