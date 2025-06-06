📧 Gen AI - Email Assistant
This Streamlit-based web app allows users to generate professional, custom-tailored emails using a Generative AI model (LLaMA3 via Groq API). The app supports multiple tones and languages, and optionally lets users send the generated email directly through SMTP.

🚀 Features
✅ Generate emails in multiple tones: formal, casual, persuasive, apologetic, friendly, professional, rude, and more.

🌐 Supports multiple languages: English, Hindi, Spanish, French, German, Chinese (Simplified), Japanese, Italian, Portuguese.

✏️ Customize:

Topic/content

Word limit

Optional sender and recipient names

Keywords to emphasize

📤 Optional email sending functionality via SMTP (Gmail supported).

🎨 Stylish HTML rendering of generated emails.

🔐 Secure password input field for email sending.

🧩 Requirements
Python Packages
Install dependencies with:

bash
Copy
Edit
pip install streamlit groq deep-translator
Additional built-in libraries used:

smtplib, email.mime (standard for email sending)

time

🛠 Setup & Usage
1. 🔑 Set Up Groq API Key
You need a Groq API key to access LLaMA3 models.
In the code, replace the placeholder:

python
Copy
Edit
api_key = "your_groq_api_key"
⚠️ Never share or hardcode secrets in production. Use environment variables instead.

2. ▶️ Run the App
In your terminal:

bash
Copy
Edit
streamlit run your_script.py
3. ✉️ Email Sending (Optional)
To enable email sending:

Check the box "Send the generated email to the recipient?"

Provide:

Recipient email

Your email (sender)

Your email password or app password

Gmail users: Enable App Passwords and use that instead of your actual password.

📸 App Preview


🧠 Prompt Structure (under the hood)
Prompts are dynamically constructed like:

css
Copy
Edit
Write a detailed, [tone] email in [language] addressed to [recipient_name] from [sender_name]. 
The topic is: '[translated_topic]'. Include these keywords: [keywords].
Keep the length around [word_limit] words. 
Use a professional structure: greeting, body, closing.
🔒 Security Note
This app requests user email credentials only for SMTP. Passwords are not stored.

📌 Future Improvements
OAuth-based secure email sending (Gmail API / Outlook API)

Add attachments

Save generated emails to PDF

Add more tones and industry-specific templates

👨‍💻 Author
Developed by Ankit Yadav

ML Developer | Streamlit + LLM Enthusiast
