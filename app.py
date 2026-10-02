import streamlit as st

from meal_analyzer import analyze_meal
from nutrition_chat import ask_macromate
from telegram import get_telegram_chat_id, send_telegram_message


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="MacroMate",
    page_icon="🥗",
    layout="centered"
)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "meal_result" not in st.session_state:
    st.session_state.meal_result = None

if "chat_answer" not in st.session_state:
    st.session_state.chat_answer = None


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🥗 MacroMate")
st.subheader("Your AI Nutrition Buddy")

st.write(
    "Understand your food, track your nutrition, "
    "and Know your nutrition.."
)

st.divider()


# --------------------------------------------------
# ABOUT YOU
# --------------------------------------------------

st.header("👤 About You")

name = st.text_input(
    "Your Name",
    placeholder="Enter your name"
)

if name:
    st.success(f"Welcome, {name}! 👋")


# --------------------------------------------------
# MEAL ANALYSIS
# --------------------------------------------------

st.header("📸 Analyze Your Meal")

st.write(
    "Upload a clear photo of your meal and "
    "MacroMate will estimate its nutrition."
)

uploaded_image = st.file_uploader(
    "Choose a meal photo",
    type=["jpg", "jpeg", "png"]
)


if uploaded_image:

    st.image(
        uploaded_image,
        caption="Your uploaded meal",
        use_container_width=True
    )

    if st.button(
        "🔍 Analyze Meal",
        type="primary",
        use_container_width=True
    ):

        with st.spinner(
            "🤖 MacroMate is analyzing your meal..."
        ):

            try:

                result = analyze_meal(uploaded_image)

                st.session_state.meal_result = result

                st.success(
                    "Meal analyzed successfully! ✅"
                )

            except Exception as e:

                st.error(
                    "❌ Unable to analyze the meal."
                )

                st.code(str(e))


# --------------------------------------------------
# NUTRITION RESULT
# --------------------------------------------------

if st.session_state.meal_result is not None:

    result = st.session_state.meal_result

    st.divider()

    st.header("📊 Nutrition Result")

    st.write(
        "Estimated nutrition based on your uploaded meal:"
    )

    # -------------------------------
    # FOOD
    # -------------------------------

    st.subheader("🍽️ Food Detected")

    st.info(
        result["food_detected"]
    )

    st.write("")

    # -------------------------------
    # NUTRITION CARDS
    # -------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            label="🔥 Calories",
            value=f'{result["calories"]} kcal'
        )

    with col2:

        st.metric(
            label="💪 Protein",
            value=f'{result["protein"]} g'
        )


    col3, col4 = st.columns(2)

    with col3:

        st.metric(
            label="🍚 Carbohydrates",
            value=f'{result["carbs"]} g'
        )

    with col4:

        st.metric(
            label="🥑 Fat",
            value=f'{result["fat"]} g'
        )


    st.write("")

    # -------------------------------
    # SUMMARY
    # -------------------------------

    st.subheader("💡 Nutrition Summary")

    st.write(
        result["summary"]
    )

    st.caption(
        "ℹ️ Nutritional values are AI-generated estimates "
        "and may vary depending on portion size, ingredients, "
        "and preparation."
    )


    # --------------------------------------------------
    # TELEGRAM
    # --------------------------------------------------

    st.divider()

    st.subheader("📲 Send Result to Telegram")

    st.write(
        "Save your nutrition report by sending it "
        "directly to Telegram."
    )

    if st.button(
        "📤 Send to Telegram",
        use_container_width=True
    ):

        chat_id = get_telegram_chat_id()

        if chat_id is None:

            st.warning(
                "Please open your MacroMate Telegram bot "
                "and send /start first. Then click this "
                "button again."
            )

        else:

            telegram_message = f"""
🍎 MacroMate Nutrition Result

🍽️ Food:
{result["food_detected"]}

🔥 Calories:
{result["calories"]} kcal

💪 Protein:
{result["protein"]} g

🍚 Carbohydrates:
{result["carbs"]} g

🥑 Fat:
{result["fat"]} g

💡 Summary:
{result["summary"]}

⚠️ These nutritional values are AI-generated estimates.
"""

            response = send_telegram_message(
                chat_id,
                telegram_message
            )

            if response.get("ok"):

                st.success(
                    "📲 Nutrition result sent to Telegram! ✅"
                )

            else:

                st.error(
                    "❌ Telegram could not send the message."
                )

                st.code(str(response))


# --------------------------------------------------
# AI CHAT
# --------------------------------------------------

st.divider()

st.header("💬 Ask MacroMate")

st.write(
    "Get simple answers to your everyday nutrition questions."
)

st.subheader("🥗 Quick Questions")

quick_col1, quick_col2 = st.columns(2)

with quick_col1:
    quick_question_1 = st.button(
        "🥚 Protein in 2 eggs?",
        use_container_width=True
    )

with quick_col2:
    quick_question_2 = st.button(
        "🍌 Is banana healthy?",
        use_container_width=True
    )

quick_col3, quick_col4 = st.columns(2)

with quick_col3:
    quick_question_3 = st.button(
        "💪 High-protein foods",
        use_container_width=True
    )

with quick_col4:
    quick_question_4 = st.button(
        "💧 How much water daily?",
        use_container_width=True
    )


question = st.text_input(
    "Your Nutrition Question",
    placeholder="Example: How much protein is in 2 eggs?"
)


# Select quick question
selected_question = question

if quick_question_1:
    selected_question = "How much protein is in 2 eggs?"

elif quick_question_2:
    selected_question = "Is banana healthy?"

elif quick_question_3:
    selected_question = "What are some high-protein foods?"

elif quick_question_4:
    selected_question = "How much water should a person drink daily?"


if st.button(
    "🤖 Ask MacroMate",
    type="primary",
    use_container_width=True
):

    if selected_question.strip() == "":
        st.warning(
            "Please enter a nutrition question."
        )

    else:

        with st.spinner(
            "🤖 MacroMate is thinking..."
        ):

            try:

                answer = ask_macromate(
                    selected_question
                )

                st.session_state.chat_answer = answer

            except Exception as e:

                st.error(
                    "❌ Unable to get an answer."
                )

                st.code(str(e))


# --------------------------------------------------
# ANSWER
# --------------------------------------------------

if st.session_state.chat_answer is not None:

    st.subheader("💡 MacroMate's Answer")

    st.info(
        st.session_state.chat_answer
    )

    st.caption(
        "ℹ️ Answers are AI-generated general nutrition "
        "information and are not medical advice."
    )

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "🍎 MacroMate • AI Nutrition Buddy"
)

st.caption(
    "AI-generated nutrition estimates • "
    "For general informational purposes"
)