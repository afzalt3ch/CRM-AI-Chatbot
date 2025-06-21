<p align="center">
  <img src="https://raw.githubusercontent.com/afzalt3ch/banner.png/main/Gemini_Generated_Image_hb31fqhb31fqhb31.png" alt="WeeBee Banner" width="100%" />
</p>

# 🤖 CRM AI Chatbot – Intelligent Assistant for Software Institution

A smart chatbot that answers course-related queries, captures user info, and emails it to the admin. Powered by **DistilBERT** for intent detection and **T5** for response generation, this chatbot provides a seamless conversational experience for users visiting your software training institute's website.

---

## 🖼️ Screenshots

### 🎥 Demo (GIF)
![Chatbot Demo](https://github.com/afzalt3ch/CRM-AI-Chatbot/blob/main/screenshots/crm-chatbot.gif)

### 💻 Interface UI
![Interface](https://github.com/afzalt3ch/CRM-AI-Chatbot/blob/main/screenshots/crm-interface.png)

---

## ✨ Features

- 🧠 **DistilBERT-based Intent Detection**
- 🗣️ **T5 Response Generator** for contextual answers
- 🧾 **Entity Extraction**: Detects name, contact info, and course
- 📨 **Admin Notification via Email** when user provides contact
- 🔁 **Session-aware**: Remembers user's name and course preference
- ✅ Pretrained models not included due to size — see below

---

## 🗃️ Intents Handled

The chatbot can identify and handle the following types of queries:

- `admission_process` – How to enroll
- `fees_inquiry` – Course pricing
- `batch_timing` – Schedule & timings
- `course_info` – Overview of a course
- `course_duration` – Duration details
- `learning_mode` – Online/offline/hybrid
- `placement_support` – Placement assistance
- `contact_info` – Collect name and phone/email

---

## 🧠 Models

| Task                  | Model       | Path             |
|-----------------------|-------------|------------------|
| Intent Detection      | DistilBERT  | `./saved_model/` |
| Response Generation   | T5 Small    | `./t5_chatbot/`  |

> **Note:** Models are NOT included in the repo due to size.  
> Train them using the included notebooks below.

---

## 📁 Folder Structure

```
CRM_T5/
├── app.py                  # Flask backend
├── static/css/styles.css   # Chatbot + UI styling
├── templates/index.html    # Main front-end HTML
├── screenshots/            # GIF + UI Screenshot
├── Dataset/
│   ├── Distell_Bert-Dataset.json
│   └── T5_Response_dataset.json
├── Training_models/
│   ├── Distell_bert.ipynb      # Notebook to train intent model
│   └── T5_Responses.ipynb      # Notebook to train T5 response model
├── saved_model/            # Trained DistilBERT (not uploaded)
├── t5_chatbot/             # Trained T5 Model (not uploaded)
└── requirements.txt
```

---

## 📦 Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/afzalt3ch/crm-chatbot.git
cd crm-chatbot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Train the Models (if needed)

Run these notebooks in Colab or Jupyter to generate models:

- `Training_models/Distell_bert.ipynb`
- `Training_models/T5_Responses.ipynb`

Save the outputs in `saved_model/` and `t5_chatbot/` respectively.

### 4. Configure Email

In `app.py`, scroll to the `send_email_to_admin()` function and change these lines:

```python
sender_email = "youremail@gmail.com"
sender_password = "your_app_password"  # Use Gmail App Password
receiver_email = "admin@gmail.com"
```

> 🔒 Never push actual passwords to GitHub. Keep them blank or use environment variables.

---

## 🚀 Run the App

```bash
python app.py
```

Visit `http://localhost:5000` in your browser.

---

## 💡 Example Flow

```plaintext
User: Hi
Bot: Hello! How can I assist you today?

User: My name is Rahul
Bot: Nice to meet you, Rahul! Please provide your contact number.

User: My contact number is 9876543210
Bot: Thanks! Your details have been sent to the admin.
```

---

## 📬 Admin Email Sample

When a user provides name + contact:

```
Subject: New Chatbot User Details

Name: Rahul
Contact: 9876543210
Course Preference: datascience
```

---

## 📜 License

MIT License

---

<p align="center"><strong>Made with ❤️ by Afzal T3ch</strong></p>
