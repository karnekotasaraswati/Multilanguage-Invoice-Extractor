from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Google Generative AI
genai.configure(api_key=os.getenv("Google_API_KEY"))

# Load Gemini Pro Vision model
model = genai.GenerativeModel("gemini-2.5-flash")

# Function to get response from Gemini
def get_gemini_response(prompt, image, user_input, language):
    # Append language preference
    final_prompt = f"{prompt}\nAnswer in {language}.\nUser Query: {user_input}"
    response = model.generate_content([final_prompt, image])
    return response.text

# Function to set up image input
def input_image_setup(upload_file):
    if upload_file is not None:
        image = Image.open(upload_file)
        return image
    return None

# ------------------- Streamlit App ------------------- #
st.set_page_config(
    page_title="🌍 Multilanguage Invoice Extractor",
    page_icon="🧾",
    layout="wide"
)

# Custom CSS for styling
st.markdown(
    """
    <style>
        .main-title {
            text-align: center;
            font-size: 32px !important;
            font-weight: bold;
            color: #2E86C1;
        }
        .sub-title {
            text-align: center;
            font-size: 18px;
            color: #566573;
            margin-bottom: 20px;
        }
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            text-align: center;
            padding: 10px;
            color: white;
            background-color: #2E86C1;
        }
        .stButton>button {
            background-color: #2E86C1;
            color: white;
            border-radius: 10px;
            font-size: 16px;
            padding: 10px 20px;
        }
        .stButton>button:hover {
            background-color: #1B4F72;
            color: #f0f0f0;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar
st.sidebar.title("⚙️ Settings")
language = st.sidebar.selectbox(
    "🌐 Choose Output Language", 
    ["English", "Hindi", "Spanish", "French", "German", "Chinese"]
)
st.sidebar.markdown("---")
st.sidebar.info("Upload your invoice and ask questions about it!")

# Main Title
st.markdown('<p class="main-title">🌍 Multilanguage Invoice Extractor</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Upload invoices in any language and get AI-powered insights instantly.</p>', unsafe_allow_html=True)

# Layout columns
col1, col2 = st.columns([1,2])

with col1:
    uploaded_file = st.file_uploader("📤 Upload Invoice Image", type=["jpg", "jpeg", "png"])
    image = None
    if uploaded_file is not None:
        image = input_image_setup(uploaded_file)
        st.image(image, caption="📄 Uploaded Invoice", use_column_width=True)

with col2:
    user_input = st.text_area("💬 Ask something about the invoice", placeholder="e.g. What is the total amount?", height=120)

submit = st.button("🚀 Extract Information")

# Default system prompt
input_prompt = """
You are an expert in reading and understanding invoices. 
Analyze the uploaded invoice image and answer user queries.
"""

# If submit button is clicked
if submit:
    if image is not None:
        with st.spinner("🔎 Analyzing the invoice..."):
            response = get_gemini_response(input_prompt, image, user_input, language)
        st.success("✅ Analysis Complete!")
        st.subheader("📌 Extracted Information:")
        st.info(response)
    else:
        st.warning("⚠️ Please upload an invoice image first.")

# Footer
st.markdown('<div class="footer">Made with ❤️ using Streamlit & Gemini AI</div>', unsafe_allow_html=True)
