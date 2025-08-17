import streamlit as st
from detector.secure_prompt_advanced import run_secure_prompt_filter

# Page settings
st.set_page_config(page_title="Secure AI Prompt Filter", layout="centered")

# Title and instruction
st.title("🔒 Secure AI Prompt Filter")
st.markdown("Enter a prompt below. Sensitive data will be detected and masked.")

# User input
user_prompt = st.text_area("Enter your AI prompt:", height=200)

# Button to trigger masking
if st.button("Detect & Mask"):
    if user_prompt.strip():
        with st.spinner("Analyzing..."):
            result = run_secure_prompt_filter(user_prompt)
        st.success("✅ Secure Prompt Ready!")
        st.text_area("Masked Prompt:", result, height=200)
    else:
        st.warning("⚠️ Please enter a prompt first.")
