import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from PIL import Image
import base64

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, image, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, image, prompt])
    return response.text

def input_image_setup(uploaded_file, max_width=600, max_height=400):
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        width, height = image.size

        if width > height:
            new_width = max_width
            new_height = int((max_width / width) * height)
        else:
            new_height = max_height
            new_width = int((max_height / height) * width)

        image = image.resize((new_width, new_height), Image.LANCZOS)
        return image
    else:
        raise FileNotFoundError("No File Uploaded")

def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

background_image_base64 = get_base64_image("AI_chemist_background.jpg")

input_prompt = """
You are an expert pharmaceutical chemist. Examine the image of the tablets and provide details in the following format:

1. Identify the tablets in the image.
2. Describe the uses and functionalities of each tablet.
3. Provide information on intended purposes, features, and typical applications.
4. Include any notable specifications or distinguishing characteristics.
"""

st.set_page_config(page_title="AI Chemist App", page_icon="💊", layout="wide")

st.markdown(
    f"""
    <style>
        /* Background Image Styling */
        .stApp {{
            background: url('data:image/jpeg;base64,{background_image_base64}') no-repeat center center fixed;
            background-size: cover;
            font-family: 'Arial', sans-serif;
        }}

        /* Header Styling */
        .header {{
            text-align: center;
            font-size: 3rem;
            font-weight: bold;
            margin-top: 20px;
            color: #ffffff;
            text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.5);
        }}

        /* Description Styling */
        .description {{
            text-align: center;
            font-size: 1.2rem;
            margin-bottom: 30px;
            color: #000000;
        }}

        /* Button Styling */
        .stButton > button:first-child {{
            background-color: #6c5ce7;
            color: white;
            border-radius: 8px;
            font-size: 1.1rem;
            padding: 0.5em 1.5em;
            margin-top: 20px;
            transition: all 0.3s ease;
        }}

        .stButton > button:first-child:hover {{
            background-color: #4834d4;
        }}

        /* Image Styling */
        .stImage > img {{
            border-radius: 12px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            margin-top: 20px;
            margin-bottom: 20px;
        }}

        /* Card Styling */
        .card {{
            background-color: rgba(255, 255, 255, 0.15);
            border-radius: 12px;
            padding: 20px;
            margin-top: 20px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        }}

        .card h4 {{
            color: #ffdd57;
            font-size: 1.5rem;
        }}

        /* General Spacing Fix */
        .block-container {{
            padding: 2rem 2rem;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 class='header'>🧪 AI Chemist App 💊</h1>", unsafe_allow_html=True)
st.markdown("<p class='description'>Upload an image of tablets, and let AI analyze it for you!</p>", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    input_text = st.text_area("Enter a description or query (optional):", height=100)

with col2:
    uploaded_file = st.file_uploader("Upload an image of tablets (JPG, JPEG, PNG):", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = input_image_setup(uploaded_file) p
    st.image(image, caption="Uploaded Image", use_container_width=False)

submit = st.button("🔍 Analyze Image")

if submit:
    if uploaded_file:
        with st.spinner("Analyzing the image... 🧪"):
            response = get_gemini_response(input_prompt, image, input_text)
            st.success("✅ Analysis Complete!")
            st.markdown(
                f"""
                <div class="card">
                    <h4>📝 AI Analysis Result:</h4>
                    <p>{response}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.error("❌ Please upload an image before clicking 'Analyze Image'.")
        
