import streamlit as st
import requests
import json

API_BASE_URL = "http://localhost:8000"

st.set_page_config(page_title="Non Profit Agent", page_icon="🤖")

st.markdown("""
<style>
    /* Global Font Upgrade */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Title Gradient */
    h1 {
        background: -webkit-linear-gradient(45deg, #4F46E5, #9333EA);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
    }

    /* Premium Glassmorphic Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        color: white !important;
        border-radius: 25px;
        border: none;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease !important;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 10px 20px rgba(100, 100, 255, 0.3) !important;
        color: white !important;
        border: none;
    }
    
    /* Styled Chat Bubbles */
    [data-testid="stChatMessage"] {
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 15px;
        border: 1px solid rgba(150, 150, 150, 0.1);
    }
    
    /* Expanders */
    [data-testid="stExpander"] {
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        border: 1px solid rgba(150, 150, 150, 0.2);
    }
</style>
""", unsafe_allow_html=True)

st.title("🤖 Non Profit Agent")
st.markdown("Welcome! I am here to help you learn how to handle donor emails and scenarios.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
if "active_quiz" not in st.session_state:
    st.session_state.active_quiz = None
if "triage_result" not in st.session_state:
    st.session_state.triage_result = None
if "triaged_email" not in st.session_state:
    st.session_state.triaged_email = ""

def handle_evaluation(user_text):
    st.chat_message("user").markdown(user_text)
    st.session_state.messages.append({"role": "user", "content": user_text})

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        with st.spinner("Thinking..."):
            try:
                # Prepare payload for API
                payload = {
                    "user_input": user_text,
                    "chat_history": st.session_state.messages
                }
                response = requests.post(f"{API_BASE_URL}/evaluate_answer", json=payload)
                response.raise_for_status()
                
                evaluation = response.json().get("content", "Error evaluating response.")
                response_placeholder.markdown(evaluation)
                st.session_state.messages.append({"role": "assistant", "content": evaluation})
                
            except requests.exceptions.RequestException as e:
                err_msg = f"API Error: Make sure FastAPI backend is running! ({str(e)})"
                response_placeholder.error(err_msg)
                st.session_state.messages.append({"role": "assistant", "content": err_msg})

# Main UI - Donor Email Input (Removed Sidebar to make it cleaner!)
if not st.session_state.active_quiz:
    with st.expander("📨 Triage Email & Generate Training Quiz", expanded=len(st.session_state.messages) == 0):
        donor_email = st.text_area("Paste a raw donor email here to analyze:", height=150, value=st.session_state.triaged_email)
        
        if st.session_state.triage_result is None:
            if st.button("Analyze Email (Triage)", use_container_width=True):
                if donor_email.strip():
                    with st.spinner("Analyzing urgency via Triage Agent..."):
                        try:
                            response = requests.post(f"{API_BASE_URL}/triage_email", json={"email_text": donor_email})
                            response.raise_for_status()
                            triage_data = json.loads(response.json().get("content", "{}"))
                            st.session_state.triage_result = triage_data
                            st.session_state.triaged_email = donor_email
                            st.rerun()
                        except Exception as e:
                            st.error(f"Triage Error: {e}")
                else:
                    st.warning("Please paste an email first.")
        else:
            # Display Triage Result
            urgency = st.session_state.triage_result.get("urgency", "Low")
            sla = st.session_state.triage_result.get("sla_days", 5)
            reason = st.session_state.triage_result.get("reason", "")
            
            if urgency == "High":
                st.error(f"🔴 **High Urgency** - SLA: {sla} Day(s)\n\n*Reason: {reason}*")
            elif urgency == "Medium":
                st.warning(f"🟡 **Medium Urgency** - SLA: {sla} Day(s)\n\n*Reason: {reason}*")
            else:
                st.info(f"🟢 **Low Urgency** - SLA: {sla} Day(s)\n\n*Reason: {reason}*")
                
            if st.button("Generate Training Quiz", use_container_width=True):
                with st.spinner("Generating Quiz via Backend API..."):
                    try:
                        response = requests.post(f"{API_BASE_URL}/generate_quiz", json={"email_text": st.session_state.triaged_email})
                        response.raise_for_status()
                        quiz_content_str = response.json().get("content", "[]")
                        try:
                            st.session_state.active_quiz = json.loads(quiz_content_str)
                            st.session_state.triage_result = None # Reset for next time
                            st.session_state.triaged_email = ""
                            st.session_state.messages.append({"role": "assistant", "content": "**I generated a quiz! Please answer the questions below.**"})
                        except Exception:
                            st.error("Failed to parse quiz from backend.")
                        st.rerun()
                    except requests.exceptions.RequestException as e:
                        st.error(f"Make sure backend is running: {e}")

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Interactive Quiz Form
if st.session_state.active_quiz:
    st.markdown("### 📝 Active Training Quiz")
    with st.form("quiz_form"):
        user_answers = {}
        for idx, q_data in enumerate(st.session_state.active_quiz):
            question_text = q_data.get("question", f"Question {idx+1}")
            options = q_data.get("options", ["A", "B", "C", "D"])
            # Set index=None so no option is pre-selected!
            user_answers[str(idx+1)] = st.radio(f"**{idx+1}. {question_text}**", options, key=f"q_{idx}", index=None)
            st.markdown("---")
            
        submitted = st.form_submit_button("Submit Answers", use_container_width=True)
        if submitted:
            # Check if any questions were left blank
            if any(ans is None for ans in user_answers.values()):
                st.error("Please select an answer for every question before submitting!")
            else:
                answer_lines = []
                for idx, q_data in enumerate(st.session_state.active_quiz):
                    q_text = q_data.get("question", f"Question {idx+1}")
                    selected_ans = user_answers[str(idx+1)]
                    answer_lines.append(f"**{idx+1}. {q_text}**\n*My Answer:* {selected_ans}\n")
                
                answer_str = "\n".join(answer_lines)
                st.session_state.active_quiz = None # Clear form
                handle_evaluation(f"Here is my completed quiz:\n\n{answer_str}")
                st.rerun()

# React to user input
prompt = st.chat_input("Enter your response to the scenario or ask a question...")
if prompt:
    handle_evaluation(prompt)
