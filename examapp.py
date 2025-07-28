import streamlit as st
import json
import os

# === Load Questions ===
with open("questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

# Fix image paths for Linux (Streamlit Cloud)
for q in questions:
    if q.get("image"):
        q["image"] = q["image"].replace("\\", "/")

questions_per_page = 10
total_pages = (len(questions) + questions_per_page - 1) // questions_per_page

# === Initialize session state ===
if "current_page" not in st.session_state:
    st.session_state.current_page = 1
if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}

# === UI Header ===
st.title("MMV 2nd Year Quiz App (Streamlit)")
st.markdown(f"**Page {st.session_state.current_page} of {total_pages}**")

# === Pagination ===
start = (st.session_state.current_page - 1) * questions_per_page
end = start + questions_per_page
current_questions = questions[start:end]

# === Render Questions ===
for q in current_questions:
    st.subheader(f"Q{q['number']}: {q['question']}")

    # ✅ Safe image loading
    if q.get("image"):
        if os.path.exists(q["image"]):
            st.image(q["image"])
        else:
            st.warning(f"⚠️ Image not found: {q['image']} (Q{q['number']})")

    # ✅ Safe radio default selection
    option_keys = list(q["options"].keys())
    user_answer = st.session_state.user_answers.get(q["number"])

    # Optional debug warning
    if user_answer and user_answer not in option_keys:
        st.warning(f"⚠️ Invalid saved answer '{user_answer}' for Q{q['number']}' — resetting selection.")

    # Set default index safely
    default_index = option_keys.index(user_answer) if user_answer in option_keys else 0

    selected = st.radio(
        f"Choose your answer for Q{q['number']}:",
        option_keys,
        format_func=lambda x: f"{x}. {q['options'][x]}",
        key=f"q{q['number']}",
        index=default_index
    )
    st.session_state.user_answers[q["number"]] = selected

# === Navigation Buttons ===
col1, col2, col3 = st.columns([1, 1, 2])
with col1:
    if st.button("Previous") and st.session_state.current_page > 1:
        st.session_state.current_page -= 1
with col2:
    if st.button("Next") and st.session_state.current_page < total_pages:
        st.session_state.current_page += 1
with col3:
    if st.button("Submit Quiz"):
        total = len(questions)
        correct = 0
        st.subheader("📝 Quiz Result Summary")

        for q in questions:
            user_ans = st.session_state.user_answers.get(q["number"])
            correct_ans = q.get("answer")
            if user_ans == correct_ans:
                correct += 1
            st.markdown(
                f"**Q{q['number']}**: Your answer: `{user_ans}` | "
                f"Correct: `{correct_ans}` {'✅' if user_ans == correct_ans else '❌'}"
            )

        st.success(f"🎯 You scored {correct} out of {total}")
