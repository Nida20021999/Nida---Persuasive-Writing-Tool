import streamlit as st
import json
import os
from datetime import datetime
import re

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Persuasive Writing Studio", layout="wide")

DATA_FILE = "drafts.json"

# Persuasive elements categories
PERSUASIVE_ELEMENTS = {
    "Claim & Argument": "Is your main argument clear, debatable, and concise?",
    "Evidence & Examples": "Did you support your argument with logical facts, examples, or data?",
    "Reasoning & Flow": "Is your reasoning logical, and do ideas flow coherently across sentences and paragraphs?",
    "Sentence Structure": "Are your sentences varied in length and complexity to maintain reader engagement?",
    "Word Choice & Tone": "Did you use precise, academic, and persuasive vocabulary appropriate for your audience?",
    "Rhetorical Techniques": "Did you use techniques like repetition, modal verbs, counter-arguments, and emphatic statements?",
    "Counter-arguments & Rebuttal": "Did you anticipate opposing views and respond convincingly?",
    "Conclusion Effectiveness": "Does your conclusion summarize the argument and reinforce your stance?"
}

# ---------------- FUNCTIONS ----------------
def load_drafts():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_draft(title, text, feedback):
    drafts = load_drafts()
    drafts[title] = {
        "text": text,
        "feedback": feedback,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    with open(DATA_FILE, "w") as f:
        json.dump(drafts, f, indent=4)

def analyze_essay(text, level):
    feedback = {}

    # Claim & Argument
    if len(text.split()) < 120:
        feedback["Claim & Argument"] = "Your argument is underdeveloped. Expand your main claim with examples and specify why it matters."
    else:
        feedback["Claim & Argument"] = "Your claim is clear and arguable."

    # Evidence & Examples
    if not re.search(r"\b(for example|such as|evidence|statistics|data)\b", text.lower()):
        feedback["Evidence & Examples"] = "Add concrete evidence and examples to strengthen your points."
    else:
        feedback["Evidence & Examples"] = "Good use of supporting evidence."

    # Reasoning & Flow
    connectors = ["because", "therefore", "however", "thus", "moreover", "for instance"]
    if not any(c in text.lower() for c in connectors):
        feedback["Reasoning & Flow"] = "Include logical connectors to improve flow and guide the reader through your argument."
    else:
        feedback["Reasoning & Flow"] = "Ideas flow well with connectors."

    # Sentence Structure
    sentences = re.split(r'[.!?]', text)
    if len(sentences) < 5:
        feedback["Sentence Structure"] = "Vary sentence length and structure for engagement. Use a mix of short and complex sentences."
    else:
        feedback["Sentence Structure"] = "Sentence structure is varied appropriately."

    # Word Choice & Tone
    informal_words = ["very", "really", "a lot", "thing", "stuff"]
    if any(w in text.lower() for w in informal_words):
        feedback["Word Choice & Tone"] = "Replace informal words with precise academic vocabulary. Maintain persuasive and formal tone."
    else:
        feedback["Word Choice & Tone"] = "Word choice is appropriate and persuasive."

    # Rhetorical Techniques
    modals = ["should", "must", "need to", "ought to"]
    if not any(m in text.lower() for m in modals):
        feedback["Rhetorical Techniques"] = "Use modal verbs to assert your stance strongly. Consider repetition or emphatic statements for persuasion."
    else:
        feedback["Rhetorical Techniques"] = "Good use of persuasive techniques."

    # Counter-arguments & Rebuttal
    counters = ["although", "some may argue", "on the other hand", "however"]
    if not any(c in text.lower() for c in counters):
        feedback["Counter-arguments & Rebuttal"] = "Address opposing views to make your argument stronger."
    else:
        feedback["Counter-arguments & Rebuttal"] = "Counter-arguments are acknowledged effectively."

    # Conclusion
    if not re.search(r"\b(in conclusion|to sum up|therefore|thus)\b", text.lower()):
        feedback["Conclusion Effectiveness"] = "Make sure your conclusion reinforces your argument and summarizes key points."
    else:
        feedback["Conclusion Effectiveness"] = "Conclusion is effective and persuasive."

    return feedback

# ---------------- UI ----------------
st.title("🎯 Persuasive Writing Studio")
st.markdown("Interactive, academic, and creative tool for Pakistani ESL undergraduates.")

col1, col2 = st.columns([2,1])
with col1:
    title = st.text_input("Draft Title")
    level = st.selectbox("Select Difficulty Level", ["Beginner", "Intermediate", "Advanced"])
    essay = st.text_area("Write or paste your essay here:", height=350)

with col2:
    st.subheader("📝 Persuasive Writing Categories")
    for elem in PERSUASIVE_ELEMENTS:
        st.markdown(f"- **{elem}**")

if st.button("Analyze Essay"):
    if essay.strip() == "":
        st.warning("Please enter text for analysis.")
    else:
        feedback = analyze_essay(essay, level)
        st.subheader("💡 Detailed Feedback")
        for k,v in feedback.items():
            st.info(f"**{k}:** {v}")
        if title:
            save_draft(title, essay, feedback)
            st.success("Draft saved successfully!")

# ---------------- Saved Drafts ----------------
st.subheader("📂 Saved Drafts")
drafts = load_drafts()
if drafts:
    selected = st.selectbox("Select a saved draft", list(drafts.keys()))
    st.text_area("Saved Draft", drafts[selected]["text"], height=200)
else:
    st.info("No drafts saved yet.")