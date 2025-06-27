# to run this code install any local llm model in you system
import streamlit as st
from langchain_community.llms import Ollama
import base64

# ────────── Page Setup ──────────
st.set_page_config(layout="wide")

# ─────── Logo and Title (Centered, Single Block) ───────
with open("logo.png", "rb") as image_file:
    encoded_logo = base64.b64encode(image_file.read()).decode()

st.markdown(f"""
    <div style="display: flex; justify-content: center; align-items: center; gap: 20px; margin-top: 20px; margin-bottom: 30px;">
        <img src="data:image/png;base64,{encoded_logo}" width="100">
        <h1 style="margin: 0; font-size: 2.5rem;">Gen AI – Email Assistant</h1>
    </div>
""", unsafe_allow_html=True)

# ────────── Styling Padding ──────────
st.markdown("""
    <style>
        .block-container { padding-left: 3rem !important; padding-right: 3rem !important; }
    </style>
""", unsafe_allow_html=True)

# ────────── Sidebar for Navigation ──────────
page = st.sidebar.radio("Navigation", ["Generate Email Reply", "Sample Emails"])

# ────────── Sample Emails View ──────────
if page == "Sample Emails":
    st.subheader("Sample Email Collection")
    try:
        with open("sampleemail.pdf", "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
            pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800px" type="application/pdf"></iframe>'
            st.markdown(pdf_display, unsafe_allow_html=True)
    except FileNotFoundError:
        st.error("'sampleemail.pdf' not found in the current directory.")
    st.stop()

# ────────── Ollama Init ──────────
try:
    llm = Ollama(model="gemma2:2b")
except Exception as e:
    st.error(f"Ollama init failed: {e}")
    st.stop()

# ────────── Layout ──────────
left, right = st.columns(2)

with left:
    st.markdown("### Reply to Email")

    with st.form("email_form"):
        tone = st.selectbox("Select your reply tone", ["positive", "neutral", "negative"])
        word_limit = st.slider("Word limit", 50, 300, 120, step=10)
        keywords_raw = st.text_input("Keywords (comma separated)", placeholder="e.g. meeting, form, update")

        original_email = st.text_area(
            "Paste your email content below:",
            height=250,
            placeholder="Paste any email here to generate a reply..."
        )

        submitted = st.form_submit_button("Generate Reply")

# ────────── Helpers ──────────
def format_keywords(raw: str) -> str:
    return ", ".join([k.strip() for k in raw.split(",") if k.strip()]) or "none"
tone_instruction = {
    "positive": (
        "Respond in a warm, cooperative, and proactive tone. "
        "Start by acknowledging the sender's message with gratitude or positivity. "
        "Express agreement, acceptance, or willingness to help. "
        "Confirm actions clearly and offer assistance if needed. "
        "Be encouraging and solution-oriented — great for scheduling, approvals, confirmations, form submissions, etc. "
        "Example language includes:\n"
        "- 'I’d be happy to assist with this.'\n"
        "- 'Thank you for your message – I’ll take care of it promptly.'\n"
        "- 'This sounds like a great initiative – count me in.'\n"
        "- 'I’ve noted the request and will ensure timely completion.'\n"
        "- 'Sure, I will provide the requested details by [date].'\n"
        "- 'Appreciate your effort on this – happy to collaborate.'\n"
        "- 'Thank you for the update – glad to see the progress.'\n"
        "- 'Happy to confirm my attendance for the meeting.'\n"
        "- 'Yes, I’ll submit the form by the stated deadline.'\n"
        "- 'Glad to support this, please let me know the next steps.'\n"
        "- 'I'll share the required documents by EOD.'\n"
        "- 'Thanks again – let me know if you need anything else.'\n"
        "- 'Thank you for your service — we wish you all the best in your next role.'\n"
        "- 'We appreciate your contribution and will ensure a smooth transition.'\n"
        "- 'I’m grateful for your dedication and wish you continued success.'\n"
        "- 'It has been a pleasure working with you — best wishes for your journey ahead.'\n"
        "- 'Thanks for your outstanding work — we look forward to staying in touch.'\n"
        "- 'Absolutely, I’ll prioritize this and update you shortly.'\n"
        "- 'You’ve made a lasting impact here — we’re proud of your work.'\n"
        "- 'Thanks for the timely update — I’m on it now.'\n"
        "- 'Yes, I’ll coordinate with the team and ensure completion.'\n"
        "- 'Looking forward to working together on this new project.'\n"
        "- 'Great to see this moving forward — I’ll be sure to support wherever needed.'"
    ),

    "neutral": (
        "Respond in a courteous, balanced, and professional tone. "
        "Acknowledge the message without confirming or denying the request. "
        "Best suited for pending decisions, escalations, or information-only replies. "
        "Avoid strong opinions; maintain a measured stance. "
        "Example language includes:\n"
        "- 'Thank you for reaching out — I’ll review this and respond shortly.'\n"
        "- 'I’ve noted your request; it’s currently under discussion.'\n"
        "- 'This has been forwarded to the concerned team for further evaluation.'\n"
        "- 'Let me verify the details and get back to you.'\n"
        "- 'I appreciate the update; I’ll keep this in mind.'\n"
        "- 'Thanks for sharing — awaiting internal feedback.'\n"
        "- 'We’ll get back to you once we have more clarity.'\n"
        "- 'I acknowledge receipt of your message and will respond as needed.'\n"
        "- 'We’re currently assessing feasibility; we’ll share a decision soon.'\n"
        "- 'Please allow us some time to explore this further.'\n"
        "- 'Your message has been logged for review by the appropriate team.'\n"
        "- 'We acknowledge receipt of your resignation letter and will begin processing accordingly.'\n"
        "- 'Your notice period has been taken into account — further steps will follow.'\n"
        "- 'The transition process will be coordinated with your reporting manager.'\n"
        "- 'We'll communicate any additional details once the review is complete.'\n"
        "- 'Further analysis is underway — updates will follow.'\n"
        "- 'This is under consideration; we will notify you once finalized.'\n"
        "- 'Thank you for notifying us — we’ll respond with the next steps.'\n"
        "- 'We understand the request and will revert after alignment with relevant stakeholders.'\n"
        "- 'This input has been noted — we are reviewing it internally.'"
    ),

    "negative": (
        "Respond in a respectful, empathetic, and professionally declining tone. "
        "Begin by acknowledging the sender's effort or intention. "
        "Politely decline the request with a brief explanation. "
        "Maintain respect, offer alternatives if available, and avoid harsh language. "
        "Example language includes:\n"
        "- 'Thank you for your message. Unfortunately, I won’t be able to proceed with this at the moment.'\n"
        "- 'Regrettably, due to existing commitments, I cannot attend the meeting.'\n"
        "- 'I appreciate your proposal, but we are unable to accommodate it at this time.'\n"
        "- 'While your request is valid, we are currently focusing on other priorities.'\n"
        "- 'I must respectfully decline due to internal policy restrictions.'\n"
        "- 'Unfortunately, I won’t be able to assist with this task.'\n"
        "- 'As much as I’d like to help, this request falls outside my responsibilities.'\n"
        "- 'We’ve reviewed the matter, and a different course of action is recommended.'\n"
        "- 'Due to scheduling constraints, I won’t be able to join.'\n"
        "- 'While I understand the need, this cannot be approved under current guidelines.'\n"
        "- 'I appreciate your understanding and hope we can explore alternatives soon.'\n"
        "- 'We regret to accept your resignation at this time, but understand and respect your decision.'\n"
        "- 'Unfortunately, the current timeline doesn’t allow for the requested change.'\n"
        "- 'We’ve explored the request, but it’s not feasible within our current scope.'\n"
        "- 'We’re unable to make exceptions at this stage — thank you for understanding.'\n"
        "- 'Despite your commitment, the current situation doesn’t allow us to proceed as requested.'\n"
        "- 'We won’t be able to proceed further on this initiative under the current circumstances.'"
    )
}

# ────────── RIGHT: Output ──────────
with right:
    if submitted:
        if not original_email.strip():
            st.error("Please paste the email content before generating a reply.")
            st.stop()

        keywords = format_keywords(keywords_raw)

        system_prompt = (
            "You are an expert email copywriter. "
            "Write clear, concise, and polite replies in fluent English."
        )

        prompt = (
            f"{system_prompt}\n\n"
            f"{tone_instruction[tone]}\n"
            f"Reply to the email below using a {tone} tone.\n"
            f"- Keywords to include: {keywords}\n"
            f"- Target length: about {word_limit} words\n"
            "Structure: greeting, response body, closing.\n\n"
            f"--- ORIGINAL EMAIL START ---\n{original_email.strip()}\n--- ORIGINAL EMAIL END ---"
        )

        with st.spinner("Crafting your reply..."):
            try:
                email_body = llm.invoke(prompt).strip()

                if not email_body:
                    st.warning("No content generated. Try adjusting your input.")
                else:
                    st.markdown("**Generated Reply:**")
                    st.markdown(
                        f"""
                        <div style='
                            border: 1px solid #ccc;
                            border-radius: 10px;
                            padding: 15px;
                            background-color: #f9f9f9;
                            white-space: pre-wrap;
                            font-family: "Segoe UI", sans-serif;
                            font-size: 15px;
                            line-height: 1.6;
                            color: #333;
                        '>{email_body}</div>
                        """,
                        unsafe_allow_html=True
                    )
                    st.download_button(" Download Reply", email_body, file_name="reply_email.txt")

            except Exception as e:
                st.error(f"LLM generation error: {e}")
    else:
        st.info("Paste your email on the left and click **Generate Reply**.")
