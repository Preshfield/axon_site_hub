from duckduckgo_search import DDGS
import streamlit as st
import os, io, base64
from datetime import datetime, timedelta, timezone
from groq import Groq
from gtts import gTTS
import PyPDF2
from streamlit_mic_recorder import speech_to_text
from streamlit_pdf_viewer import pdf_viewer

# 1. LOAD EXTERNAL CSS
def local_css(file_name):
    if os.path.exists(file_name):
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.set_page_config(page_title="AXON SITE | Command Hub", layout="wide", page_icon="🏗️")
local_css("css/style.css")
import streamlit as st
import openai
# ... your other imports ...

# --- STEP 1: INITIALIZE MEMORY (PUT IT HERE) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- STEP 2: YOUR FUNCTIONS ---
def digest_manual():
    # ... code for PDF processing ...
    pass

@st.cache_data(ttl=3600)
def falcon_query(user_prompt, mode):
    # ... the Mistral/DeepSeek logic ...
    pass

# --- STEP 3: THE UI / SIDEBAR ---
# --- STEP 3: THE UI / SIDEBAR ---
st.set_page_config(page_title="AXON SITE | Command Hub", page_icon="🏗️")
st.title("🏗️ AXON SITE INTELLIGENCE")
# ... your sidebar and chat input code goes here ...

# ... rest of your layout ...


# ====================== AXON INTELLIGENCE ENGINES ======================
def digest_site_specs():
    # Looks for site_specs.pdf, falls back to gate_manual.pdf if not found
    target_file = "site_specs.pdf" if os.path.exists("site_specs.pdf") else "gate_manual.pdf"
    if os.path.exists(target_file):
        try:
            with open(target_file, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                return "".join([page.extract_text() for page in reader.pages])
        except: return ""
    return ""

import openai 

@st.cache_data(ttl=3600)
def axon_query(user_prompt: str, mode: str):
    # 1. Setup Context (Same as before)
    site_context = digest_site_specs()
    
    # 2. Build the System Instruction
    sys_rules = f"You are AXON SITE Intelligence. Use these specs: {site_context}. Be conversational but professional."
    
    # 3. Create the Conversation Packet (The Memory)
    # We start with the system rules, then add all previous messages
    conversation = [{"role": "system", "content": sys_rules}]
    for msg in st.session_state.messages:
        conversation.append({"role": msg["role"], "content": msg["content"]})
    
    # Add the current prompt
    conversation.append({"role": "user", "content": user_prompt})

    # 4. Call DeepSeek
    client = openai.OpenAI(api_key=st.secrets["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")
    
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=conversation
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"MEMORY ERROR: {str(e)}"

def save_site_log(report_text):
    with open("site_daily_reports.txt", "a", encoding="utf-8") as f:
        f.write(f"{report_text}\n{'='*50}\n")

# ====================== ACCESS CONTROL ======================
STAFF_DB = {"Eng_Pappi": "Master", "PM_Bambi": "Nancy", "Foreman_Ali": "Build01"}

if "auth" not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    st.markdown("<h1 style='text-align:center; color:#fbbf24; font-family:Orbitron;'>🏗️ AXON SITE | LOGIN</h1>", unsafe_allow_html=True)
    user_id = st.selectbox("OPERATOR ID:", list(STAFF_DB.keys()))
    user_pw = st.text_input("ACCESS CODE:", type="password")
    if st.button("INITIALIZE SYSTEM"):
        if user_pw == STAFF_DB[user_id]:
            st.session_state.auth = True
            st.session_state.current_worker = user_id
            st.rerun()
    st.stop()

# ====================== COMMAND UI ======================
if st.button("🔒 DEACTIVATE", type="secondary"):
    st.session_state.auth = False
    st.rerun()

dubai_time = datetime.now(timezone(timedelta(hours=4))).strftime("%H:%M")
st.markdown(f'<div class="custom-header"><b>Axon Active:</b> {st.session_state.current_worker} | {dubai_time}</div>', unsafe_allow_html=True)

st.markdown("""
    <div style='text-align: left; padding: 40px 0 20px 0;'>
        <h1 class='axon-title'>AXON SITE</h1>
        <h2 class='axon-sub'>ENGINEERING HUB <span style='font-size:20px; color:#fbbf24; vertical-align:middle;'>● ONLINE</span></h2>
        <p style='color: #94a3b8; font-size: 14px; letter-spacing: 5px; font-weight: bold; text-transform: uppercase;'>
            Project Analysis & Compliance Management
        </p>
    </div>
""", unsafe_allow_html=True)

t1, t2, t3 = st.tabs(["🏗️ SITE INTEL", "📘 BLUEPRINTS", "📑 DAILY REPORTS"])

with t1:
    st.subheader("🔍 Technical Scan")
    k_mode = st.radio("Focus:", ["Engineering Specs", "Live Safety Feed"], horizontal=True)
    k_query = st.text_input("Query project data...", key="k_scan")
    if k_query: st.warning(axon_query(k_query, k_mode))

    st.divider()

    st.markdown('<div class="axon-box">', unsafe_allow_html=True)
    st.subheader("📻 Subcontractor Radio")
    langs = {"Hindi": "hi", "Urdu": "ur", "Arabic": "ar", "Bengali": "bn", "Tagalog": "tl"}
    d_lang = st.selectbox("Labor Language:", list(langs.keys()))
    
    c1, c2 = st.columns([3, 1])
    with c1: st.write("🎤 **Incoming Comm (Worker)**")
    with c2: worker_audio = speech_to_text(language=langs[d_lang], start_prompt="👂 LISTEN", key='d_mic')

    if worker_audio:
        trans_resp = axon_query(f"Worker said: {worker_audio}", "Site Radio")
        st.markdown(f'<div class="driver-msg"><b>Worker:</b> {worker_audio}<br><b>Axon:</b> {trans_resp}</div>', unsafe_allow_html=True)

    d_reply = st.chat_input("Dispatch site order...")
    if d_reply:
        trans_reply = axon_query(f"Translate to {d_lang}: {d_reply}", "Site Radio")
        st.success(f"**Dispatched:** {trans_reply}")
        tts = gTTS(text=trans_reply, lang=langs[d_lang])
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        st.audio(fp.getvalue(), format="audio/mpeg", autoplay=True)
    st.markdown('</div>', unsafe_allow_html=True)

with t2:
    st.subheader("Project Documentation")
    current_pdf = "site_specs.pdf" if os.path.exists("site_specs.pdf") else "gate_manual.pdf"
    if os.path.exists(current_pdf):
        pdf_viewer(current_pdf, height=700)

with t3:
    st.subheader("📋 Daily Compliance Logs")
    notes = st.text_area("Field Observations:", key="logs", placeholder="Work completed, incidents, material delays...")
    
    if st.button("🚀 SUBMIT SITE REPORT"):
        if notes:
            with st.spinner("Analyzing Compliance..."):
                report = axon_query(f"Format as Official Daily Site Report: {notes} | Signed: {st.session_state.current_worker}", "Engineering Specs")
                st.code(report)
                save_site_log(report)
                st.success("✅ Log Synchronized with Project Database.")
        else:
            st.warning("Input required for report generation.")

    st.divider()
    if os.path.exists("site_daily_reports.txt"):
        with open("site_daily_reports.txt", "r", encoding="utf-8") as f:
            log_data = f.read()
        st.text_area("History Archive:", log_data, height=300, disabled=True)
        st.download_button("📥 Download Full Site Archive", log_data, file_name="axon_site_history.txt")
