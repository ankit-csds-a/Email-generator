import streamlit as st
from groq import Groq
from deep_translator import GoogleTranslator
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# App title and description
st.title("📧 Gen AI - Email Assistant")
st.markdown("Generate professional emails based on your input topic, tone, and language.")

# Initialize Groq client
api_key = "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"  # Replace with your Groq API key
client = Groq(api_key=api_key)

# Mapping UI language names to codes for translation
language_map = {
    "english": "english",
    "hindi": "hindi",
    "spanish": "spanish",
    "french": "french",
    "german": "german",
    "chinese (simplified)": "zh-CN",
    "japanese": "japanese",
    "italian": "italian",
    "portuguese": "portuguese"
}

# Input form
with st.form("email_form"):
    topic = st.text_input("✏️ Enter the topic or content of the email", max_chars=200)
    tone = st.selectbox(
        "🎭 Choose the tone of the email",
        [
            "formal",
            "casual",
            "persuasive",
            "apologetic",
            "friendly",
            "enthusiastic",
            "professional",
            "humorous",
            "sympathetic",
            "rude"
        ]
    )
    language = st.selectbox(
        "🌐 Language of the email",
        [
            "english",
            "hindi",
            "spanish",
            "french",
            "german",
            "chinese (simplified)",
            "japanese",
            "italian",
            "portuguese"
        ]
    )
    word_limit = st.slider("🧮 Desired word limit for email", min_value=50, max_value=300, value=120, step=10)
    recipient_name = st.text_input("👤 Recipient name (e.g., HR Manager) — optional")
    recipient_email = st.text_input("📧 Recipient's email address (for optional sending)")
    sender_name = st.text_input("🧑 Your name — optional")
    sender_email = st.text_input("📤 Your email address (for sending, optional)")
    sender_password = st.text_input("🔒 Your email password or app password (for sending, optional)", type="password")
    keywords_input = st.text_input("🔑 Keywords to emphasize (comma-separated)", "")
    send_email = st.checkbox("📨 Send the generated email to the recipient? (Optional)")
    submit = st.form_submit_button("✉️ Generate Email")

# On form submission
if submit:
    if not topic:
        st.error("Please enter the email topic or content.")
    elif send_email and (not recipient_email or not sender_email or not sender_password):
        st.error("To send email, please fill recipient email, your email, and your email password.")
    else:
        keywords = [kw.strip() for kw in keywords_input.split(",") if kw.strip()]
        keyword_text = ", ".join(keywords) if keywords else "none"

        # Get language code for translation
        source_lang = language_map.get(language.lower(), "english")

        # Translate topic to English if needed
        if source_lang != "english":
            try:
                topic_en = GoogleTranslator(source=source_lang, target="english").translate(topic)
            except Exception as e:
                st.error(f"Translation error: {e}")
                topic_en = topic  # fallback to original
        else:
            topic_en = topic

        # Construct prompt dynamically based on optional names
        greeting_part = f"addressed to {recipient_name}" if recipient_name else ""
        sender_part = f"from {sender_name}" if sender_name else ""

        prompt = (
            f"Write a detailed, {tone} email in {language} "
            f"{greeting_part} {sender_part}. "
            f"The topic is: '{topic_en}'. Include these keywords: {keyword_text}. "
            f"Keep the length around {word_limit} words. "
            f"Use a professional structure: greeting, body, closing. Respond only in {language}. "
        )

        # If sender_name is provided, instruct to replace placeholder, else skip that
        if sender_name:
            prompt += "Ensure [Your Name] is replaced with the actual sender's name."

        # Generate email
        with st.spinner("Generating your email..."):
            stream = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_completion_tokens=1000,
                top_p=1,
                stream=True
            )

            response = ""
            for chunk in stream:
                delta = chunk.choices[0].delta.content or ""
                response += delta
                time.sleep(0.02)

            # Replace placeholder with sender name if provided
            if sender_name:
                full_email = response.replace("[Your Name]", sender_name)
            else:
                full_email = response

            # Background box for output
            background_image_url = "https://i.pinimg.com/236x/f7/ab/d1/f7abd14eece4d7c94bc8cdaa3c47bf4e.jpg"

            styled_html = f"""
            <div style="
                padding: 20px;
                border-radius: 12px;
                border: 1px solid #ccc;
                background-image: url('{background_image_url}');
                background-size: cover;
                background-repeat: no-repeat;
                background-position: center;
                color: black;
                font-size: 16px;
                line-height: 1.6;
                white-space: pre-wrap;
                box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
            ">
                {full_email.strip().replace('\n', '<br>')}
            </div>
            """
            st.markdown("---")
            st.markdown("✅ **Final Email:**", unsafe_allow_html=True)
            st.markdown(styled_html, unsafe_allow_html=True)

            # Send email if opted in
            if send_email:
                try:
                    # Prepare the email
                    msg = MIMEMultipart()
                    msg['From'] = sender_email
                    msg['To'] = recipient_email
                    msg['Subject'] = f"Email from {sender_name if sender_name else sender_email} via Gen AI Assistant"

                    # Use plain text part for sending
                    body = full_email.replace("<br>", "\n")
                    msg.attach(MIMEText(body, 'plain'))

                    # SMTP sending - example uses Gmail
                    smtp_server = 'smtp.gmail.com'
                    smtp_port = 587

                    server = smtplib.SMTP(smtp_server, smtp_port)
                    server.starttls()
                    server.login(sender_email, sender_password)
                    server.send_message(msg)
                    server.quit()

                    st.success(f"📨 Email sent successfully to {recipient_email}!")
                except Exception as e:
                    st.error(f"❌ Failed to send email: {e}")
