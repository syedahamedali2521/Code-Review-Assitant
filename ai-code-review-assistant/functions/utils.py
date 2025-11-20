import streamlit as st
from fpdf import FPDF
import requests
import json
def load_lottie_animation(file_path):
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None


def generate_report(analysis_results, ai_review, language):
    """
    Generate a PDF report from analysis results and AI review.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="AI-Powered Code Review Report", ln=True, align='C')
    pdf.cell(200, 10, txt=f"Language: {language}", ln=True)
    pdf.cell(200, 10, txt="", ln=True)

    pdf.cell(200, 10, txt="Static Analysis Results:", ln=True)
    for key, value in analysis_results.items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)

    pdf.cell(200, 10, txt="", ln=True)
    pdf.cell(200, 10, txt="AI Review:", ln=True)
    pdf.multi_cell(0, 10, txt=ai_review)

    return pdf.output(dest='S').encode('latin-1')

def trigger_confetti():
    """
    Trigger confetti animation using streamlit-confetti or similar.
    Since streamlit-confetti might not be installed, use a placeholder.
    """
    # Placeholder: In a real app, integrate with streamlit-confetti
    st.balloons()  # Streamlit's built-in balloons as placeholder for confetti

def load_lottie_animation(file_path):
    """
    Load Lottie animation from JSON file.
    """
    with open(file_path, 'r') as f:
        return json.load(f)
