import streamlit as st

from ranker import (
    extract_text_from_pdf,
    rank_resume
)

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="AI Resume Screener",
    page_icon="📄",
    layout="wide"
)

# -----------------------------
# HEADER
# -----------------------------
st.title("🤖 AI Resume Screener & Ranker")
st.markdown("### Upload resumes and let AI rank the best candidates instantly")

st.divider()

# -----------------------------
# JOB DESCRIPTION SECTION
# -----------------------------
st.subheader("📌 Job Description")

jd_option = st.selectbox(
    "Choose Job Role",
    ["Custom JD", "Frontend Developer", "Backend Developer"]
)

job_description = ""

if jd_option == "Custom JD":
    job_description = st.text_area("Enter Job Description")

elif jd_option == "Frontend Developer":
    job_description = """
Frontend Developer Role:
- React, JavaScript, HTML, CSS
- REST APIs
- Git & Responsive Design
"""

elif jd_option == "Backend Developer":
    job_description = """
Backend Developer Role:
- Python, Django / Flask
- REST APIs
- SQL / Databases
- Authentication & Security
"""

st.divider()

# -----------------------------
# UPLOAD SECTION
# -----------------------------
st.subheader("📤 Upload Resumes (Max 5)")

uploaded_resumes = st.file_uploader(
    "Upload PDF resumes",
    type=["pdf"],
    accept_multiple_files=True
)

# Limit check
if uploaded_resumes and len(uploaded_resumes) > 5:
    st.error("❌ Maximum 5 resumes allowed")
    st.stop()

st.divider()

# -----------------------------
# PROCESSING
# -----------------------------
if uploaded_resumes and job_description:

    st.info("⏳ AI is analyzing resumes... please wait")

    results = []

    progress_bar = st.progress(0)

    for i, file in enumerate(uploaded_resumes):

        # Extract text
        resume_text = extract_text_from_pdf(file)

        # AI scoring
        score = rank_resume(resume_text, job_description)

        results.append({
            "name": file.name.replace(".pdf", ""),
            "score": score
        })

        # Update progress bar
        progress_bar.progress((i + 1) / len(uploaded_resumes))

    # Sort results
    results = sorted(
        results,
        key=lambda x: x["score"],
        reverse=True
    )

    st.success("✅ Analysis Complete!")

    st.divider()

    # -----------------------------
    # RESULTS DASHBOARD
    # -----------------------------
    st.subheader("🏆 Candidate Ranking")

    cols = st.columns(3)

    for i, r in enumerate(results, start=1):

        card = f"""
        ### {i}. {r['name']}
        **Match Score:** `{r['score']}%`
        """

        if i == 1:
            cols[0].success("🥇 TOP CANDIDATE")
            cols[0].markdown(card)

        elif i == 2:
            cols[1].info("🥈 SECOND BEST")
            cols[1].markdown(card)

        elif i == 3:
            cols[2].warning("🥉 THIRD PLACE")
            cols[2].markdown(card)

        else:
            st.markdown(card)

        st.progress(int(r['score']))

    st.divider()

    # -----------------------------
    # SUMMARY
    # -----------------------------
    st.subheader("📊 Summary")

    best = results[0]

    st.success(
        f"🏆 Best Candidate: {best['name']} with {best['score']}% match"
    )

else:
    st.warning("📌 Please upload resumes and select a job description")