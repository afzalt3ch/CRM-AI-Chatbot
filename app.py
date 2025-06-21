from flask import Flask, request, jsonify, session, render_template
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# ====== Load DistilBERT for Intent Detection ======
intent_tokenizer = DistilBertTokenizer.from_pretrained("./saved_model")
intent_model = DistilBertForSequenceClassification.from_pretrained("./saved_model")
intent_labels = [
    "admission_process",
    "batch_timing",
    "contact_info",
    "course_duration",
    "course_info",
    "fees_inquiry",
    "learning_mode",
    "placement_support"
]

# ====== Load T5 for Response Generation ======
t5_tokenizer = T5Tokenizer.from_pretrained("./t5_chatbot")
t5_model = T5ForConditionalGeneration.from_pretrained("./t5_chatbot")

# ====== Predefined Courses ======
valid_courses = ["robotics", "testing", "datascience", "django", "java", "mean", "flutter", "aspnet", "list"]

# ====== Utility: Predict Intent ======
def predict_intent(text):
    inputs = intent_tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    outputs = intent_model(**inputs)
    probs = torch.nn.functional.softmax(outputs.logits, dim=1)
    predicted_class = torch.argmax(probs, dim=1).item()

    # Debug output
    print("Predicted Intent ID:", predicted_class)
    print("Predicted Intent Label:", intent_labels[predicted_class])

    return intent_labels[predicted_class]


# ====== Utility: Extract Course Entity ======
def extract_entity(text):
    for course in valid_courses:
        if course.lower() in text.lower():
            return course
    return None

def extract_name(text):
    match = re.search(r"\b(my name is|i am)\s+([A-Za-z]+)", text, re.IGNORECASE)
    if match:
        return match.group(2)
    return None

# ====== Utility: Extract Contact (Phone or Email) ======
def extract_contact(text):
    phone = re.search(r"\b\d{10}\b", text)
    email = re.search(r"\b[\w\.-]+@[\w\.-]+\.\w+\b", text)
    return phone.group(0) if phone else email.group(0) if email else None

def generate_response(user_input):
    input_text = f"generate response: {user_input}"
    input_ids = t5_tokenizer.encode(input_text, return_tensors="pt", truncation=True, max_length=128)

    output_ids = t5_model.generate(
        input_ids,
        max_length=35,
        min_length=20,
        num_beams=4,
        early_stopping=False,
        repetition_penalty=1.6,
        do_sample=True,
        temperature=0.8,
        no_repeat_ngram_size=1
    )

    response = t5_tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return response


def send_email_to_admin(name, contact, course=None):
    sender_email = "yourgmail@gmail.com"       # Replace with your email
    sender_password = "*** **** **** ****"       # Use App Password if using Gmail
    receiver_email = "yourgmail@gmail.com"  # Replace with admin's email

    subject = "New Chatbot User Details"
    body = f"Name: {name}\nContact: {contact}\nCourse Preference: {course if course else 'Not provided'}"

    # Create the email message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)
            print("[✅ EMAIL SENT]")
    except Exception as e:
        print(f"[❌ EMAIL ERROR]: {e}")


# ====== Home Route (Loads Your HTML) ======
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get-response", methods=["POST"])
def get_response():
    user_input = request.json.get("message", "")
    user_input_lower = user_input.lower()

    # ====== Greeting Detection ======
    greetings = ["hi", "hello", "hey", "good morning", "good evening", "good afternoon"]
    if any(greet in user_input_lower for greet in greetings):
        name = session.get("name", "User")
        return jsonify({"response": f"Hello {name}! How can I assist you today?"})

    # ====== Thank You Detection ======
    if any(phrase in user_input_lower for phrase in ["thank you", "thanks", "thankyou"]):
        return jsonify({"response": "You're welcome! Let me know if you need anything else 😊"})

    # ====== Goodbye Detection ======
    if any(phrase in user_input_lower for phrase in ["bye", "goodbye", "see you", "talk to you later"]):
        name = session.get("name", "User")
        return jsonify({"response": f"Goodbye {name}! Have a great day ahead 👋"})

    # ====== Name Detection ======
    name = extract_name(user_input)
    if name:
        session["name"] = name
        return jsonify({"response": f"Nice to meet you, {name}! Please provide your contact number (e.g., My contact number is 9876543210)."})

    # ====== Intent & Entity Detection ======
    intent = predict_intent(user_input)
    entity = extract_entity(user_input)
    if entity:
        session["course"] = entity
    else:
        entity = session.get("course")

    if (intent == "learning_mode" or intent == "course_info") and entity == "list":
        course_list = [course.title() for course in valid_courses if course != "list"]
        response = "We offer the following courses:<br>" + "<br>".join(f"- {course}" for course in course_list)
        return jsonify({"response": response})

    else:
        # ====== Contact Info Flow ======
        if intent == "contact_info":
            if not session.get("name"):
                return jsonify({"response": "Please tell me your name (e.g., My name is John or I am John)."})
            elif not session.get("contact"):
                contact = extract_contact(user_input)
                if contact:
                    session["contact"] = contact
                    send_email_to_admin(session["name"], session["contact"], session.get("course"))
                    return jsonify({"response": "Thanks! Your details have been sent to the admin. You can contact us using our email: luminar123@gmail.com."})
                else:
                    return jsonify({"response": "Please tell me your contact number (e.g., My contact number is 9876543210)."})
            else:
                # If both already exist, send the email again (optional, depending on your use case)
                send_email_to_admin(session["name"], session["contact"], session.get("course"))
                return jsonify({"response": "Your details have been sent to the admin. You can contact us using our email: luminar123@gmail.com."})

        # ====== General Response Generation ======
        response = generate_response(f"intent: {intent} | entity: {entity}")
        return jsonify({"response": response})



# ====== Run the App ======
if __name__ == "__main__":
    app.run(debug=True)
