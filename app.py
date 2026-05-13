import streamlit as st
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv
import os


# Load API key
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Gemini model
model = genai.GenerativeModel("gemini-2.5-flash")

# Streamlit UI
st.set_page_config(page_title="Renault Content Auditor")

# CSS

st.markdown(
    """
    <style>

    @font-face {
        font-family: 'NouvelR';
        src: url('assets/NouvelR-Regular-AH-a6ef79cbe0c9af2e.woff2') format('woff2');
    }

    /* ===== GLOBAL BACKGROUND ===== */

    .stApp {
        background-color: #000000;
    }

    /* ===== TEXT ===== */

    html, body, p, div, span, label {
        color: white !important;
        font-family: 'NouvelR', sans-serif;
    }

    /* ===== SVG LOGO ===== */

    svg {
        width: 40px !important;
        height: auto !important;
    }

    /* ===== TITLES ===== */

    .main-title {
        font-family: 'NouvelR', sans-serif;
        font-size: 42px;
        font-weight: 700;
        color: white;
        margin-bottom: 5px;
    }

    .subtitle {
        font-family: 'NouvelR', sans-serif;
        font-size: 16px;
        color: #CCCCCC;
        margin-bottom: 30px;
    }

    /* ===== INPUTS ===== */

    textarea, input {
    background-color: #111111 !important;
    color: white !important;
    border: 1px solid #444444 !important;
    border-radius: 10px !important;
}

    /* ===== FILE UPLOADER ===== */

   [data-testid="stFileUploader"] {
    background-color: #111111 !important;
    border: 1px dashed #444444 !important;
    border-radius: 12px !important;
    padding: 15px !important;
}

[data-testid="stFileUploader"] section {
    background-color: #111111 !important;
}

[data-testid="stFileUploader"] div {
    background-color: #111111 !important;
    color: white !important;
}

section[data-testid="stFileUploader"] * {
    color: white !important;
}

    /* ===== BUTTON ===== */

    .stButton > button {
    background-color: #efdf00 !important;
    color: black !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: bold !important;
    padding: 12px 24px !important;
    font-family: 'NouvelR', sans-serif !important;
}

[data-testid="stFileUploader"] button {
    background-color: #efdf00 !important;
    color: black !important;
    border-radius: 10px !important;
    border: none !important;
    font-weight: bold !important;
}
.stButton button {
    background-color: #efdf00 !important;
    color: black !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: bold !important;
    padding: 12px 24px !important;
    font-family: 'NouvelR', sans-serif !important;
}

[data-testid="stFileUploader"] button * {
    color: black !important;
    fill: black !important;
    background: transparent !important;
}

.stButton button:hover {
    background-color: #f7ea4a !important;
    color: black !important;
}

.stButton button * {
    color: black !important;
}

/* ===== HEADER ===== */

header {
    background-color: black !important;
}

/* ===== SIDEBAR ===== */

[data-testid="stSidebar"] {
    background-color: #0a0a0a;
}

    </style>
    """,
    unsafe_allow_html=True
)

#RENAULT SVG LOGO

with open("assets/LogoRenaultWhite.svg", "r", encoding="utf-8") as file:
    svg_logo = file.read()

st.markdown(
    f"""
    <div style="display:flex; align-items:center; gap:20px; margin-bottom:20px;">
        <div style="width:40px; display:flex; align-items:center;">
    {svg_logo}
    </div>
        <div>
            <div class="main-title">Renault AI Content Auditor</div>
            <div class="subtitle">
                AI-powered guideline auditing for importer social media and marketing assets
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.write("Upload a social media creative and paste the copy.")

uploaded_image = st.file_uploader(
    "Upload Image",
    type=["png", "jpg", "jpeg"]
)

copy_text = st.text_area("Paste Copy")


# MAIN PROMPT
PROMPT = """
You are Renault Global Brand Auditor AI.

Your role is to audit Renault social media creatives according to Renault brand guidelines.

Analyze the image and copy carefully.

You must detect violations related to:

TYPOGRAPHY
- Incorrect typography (should be Nouvel'R)
- Wrong capitalization (should not use capital letters at the beggining of the sentence. The copy should all be in lowercase, but car model names 
can be in uppercase)
- Wrong model naming
- Incorrect use of "NEW"

VISUAL BRANDING
- Unauthorized logos
- Multiple logos
- Logo added over image
- Cut logos
- Unauthorized visual elements
- Decorative elements
- Text inside boxes
- Photo montage
- Excessive visual effects
- Wrong Renault color palette
- Low quality images
- Cropped vehicles

COPYWRITING
- Emojis are forbidden
- Wrong capitalization
- Incorrect CTA
- Unauthorized claims
- Wrong tone of voice

CONTENT COMPLIANCE
- Unauthorized local content
- AI generated images
- Out-of-rights images
- Non-compliant crossed posts

SCORING RULES
- Critical issues reduce score heavily
- Medium issues reduce score moderately
- Minor issues reduce score slightly

Return the result STRICTLY using this structure:

GUIDELINE SCORE: X/100

APPROVED:
YES or NO

CRITICAL ISSUES:
- issue

MEDIUM ISSUES:
- issue

MINOR ISSUES:
- issue

POSITIVE POINTS:
- point

RECOMMENDATIONS:
- recommendation

Be strict and professional like Renault Global Marketing Audit Team.
"""

# Analyze button
if uploaded_image and st.button("Analyze Creative"):

    image = Image.open(uploaded_image)

    with st.spinner("Analyzing creative..."):

        response = model.generate_content(
            [
                PROMPT,
                f"Copy:\n{copy_text}",
                image
            ]
        )

    st.subheader("📋 Audit Result")

    st.write(response.text)



