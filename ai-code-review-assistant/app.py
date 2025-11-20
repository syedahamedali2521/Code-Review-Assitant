import streamlit as st
from streamlit_lottie import st_lottie
import functions.static_analysis as sa
import functions.utils as utils
import json
from dotenv import load_dotenv
load_dotenv()

# Page config
st.set_page_config(page_title="Code Review Assistant", page_icon="🔍", layout="wide")

# ================================
# CUSTOM BLACK + GREEN UI THEME
# ================================
st.markdown("""
<style>

    body {
        background: linear-gradient(135deg, #000000 0%, #003300 100%) !important;
        color: #ccffcc !important;
    }

    .stApp {
        background: linear-gradient(135deg, #000000 0%, #004400 100%) !important;
    }

    .block-container {
        background: transparent !important;
    }

    h1, h2, h3, p, label, .stRadio, .stSelectbox {
        color: #ccffcc !important;
    }

    .card {
        background: rgba(0, 40, 0, 0.25);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        border: 1px solid rgba(0, 255, 0, 0.2);
        backdrop-filter: blur(8px);
    }

    .stTextArea, .stFileUploader {
        background: rgba(0, 30, 0, 0.4) !important;
        border-radius: 10px !important;
        border: 1px solid rgba(0, 255, 0, 0.3) !important;
        color: #ccffcc !important;
    }

    .stButton>button {
        background: linear-gradient(135deg, #004400, #009900) !important;
        color: white !important;
        border-radius: 10px !important;
        border: 1px solid #00ff55 !important;
        box-shadow: 0px 0px 8px #00ff44;
        transition: 0.2s;
        font-weight: 600;
    }

    .stButton>button:hover {
        background: linear-gradient(135deg, #00aa00, #00dd00) !important;
        transform: scale(1.03);
        box-shadow: 0px 0px 16px #00ff44;
    }

    .stTabs [data-baseweb="tab"] {
        color: #ccffcc !important;
        background: rgba(0, 50, 0, 0.3);
        border-radius: 10px 10px 0 0;
    }

    .stTabs [aria-selected="true"] {
        background: rgba(0, 100, 0, 0.4) !important;
        border-bottom: 2px solid #00ff55 !important;
        color: #00ff99 !important;
        font-weight: bold !important;
    }

</style>
""", unsafe_allow_html=True)

# ================================
# Load Lottie Animations
# ================================
animation1 = utils.load_lottie_animation("assets/animation1.json")
animation2 = utils.load_lottie_animation("assets/animation1.json")

# ================================
# TITLE
# ================================
st.title("Code Review Assistant (Static Only)")


st.markdown("Upload or paste your Python or JavaScript code for static analysis!")

# ================================
# INPUT SECTION
# ================================
st.header("📝 Code Input")
input_method = st.radio("Choose input method:", ["Upload File", "Paste Code"])

code = ""
language = st.selectbox("Select Language:", ["Python", "JavaScript"])

if input_method == "Upload File":
    uploaded_file = st.file_uploader("Upload .py or .js file", type=["py", "js"])
    if uploaded_file:
        code = uploaded_file.read().decode("utf-8")
        if uploaded_file.name.endswith('.py'):
            language = "Python"
        elif uploaded_file.name.endswith('.js'):
            language = "JavaScript"
else:
    code = st.text_area("Paste your code here:", height=200)

# ================================
# ANALYSIS BUTTONS
# ================================
if code:
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔍 Analyze Code"):
            with st.spinner("Analyzing..."):
                if language == "Python":
                    results = sa.analyze_python_code(code)
                else:
                    results = sa.analyze_js_code(code)

                st.session_state['analysis'] = results
                st.success("Analysis complete!")

    with col2:
        if st.button("🎉 Check Quality"):
            if 'analysis' in st.session_state:
                score = 0

                if language == "Python":
                    if not st.session_state['analysis'].get('unused_variables'):
                        score += 50
                    if st.session_state['analysis'].get('complexity', 0) < 10:
                        score += 50
                else:
                    issues = st.session_state['analysis'].get('issues', [])
                    score = max(0, 100 - len(issues) * 10)

                if score > 80:
                    utils.trigger_confetti()
                    st.success(f"High quality code! Score: {score}/100")
                else:
                    st.warning(f"Code quality: {score}/100")

    # ================================
    # RESULTS — ONLY STATIC NOW
    # ================================
    if 'analysis' in st.session_state:
        st.header("📊 Static Analysis Results")
        results = st.session_state['analysis']
        if 'error' in results:
            st.error(results['error'])
        else:
            for key, value in results.items():
                st.write(f"**{key.replace('_', ' ').title()}:** {value}")

