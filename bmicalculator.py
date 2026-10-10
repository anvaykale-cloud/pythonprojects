import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="BMI Calculator",  layout="wide")

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(to right, #ffecd2, #fcb69f 100%);
    }

    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {
        color: #2c3e50 !important;
    }

    .stApp p, .stApp label, .stApp span, .stApp div {
        color: #34495e !important;
    }

    div[data-testid="stRadio"] label p {
        color: #2c3e50 !important;
        font-size: 1.15rem !important;
        font-weight: 500 !important;
    }

    div[data-testid="stWidgetLabel"] p {
        color: #2c3e50 !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        margin-bottom: 5px !important;
    }

    button[data-baseweb="button"] p {
        font-size: 1.25rem !important;
        font-weight: 700 !important;
        color: #2c3e50 !important;
        margin-top: 5px !important;
    }

    button[data-baseweb="button"] {
        font-size: 1.25rem !important;
        font-weight: 700 !important;
        color: #2c3e50 !important;
    }

    .bmi-badge {
        padding: 6px 16px;
        border-radius: 20px;
        color: white !important;
        background-color: #2c3e50;
        display: inline-block;
        font-size: 1.2rem;
    }

    .health-card {
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
        margin-bottom: 20px;
        padding: 16px;
    }

    .health-card p, .health-card h4 {
        color: #2c3e50 !important;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ──────────────────────────────────────────
st.markdown("<h1 style='text-align: center; color: #2c3e50; margin-bottom: 5px;'> Pro Health & BMI Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #34495e;'>Advanced biological metrics for health monitoring</p>", unsafe_allow_html=True)

# ── Session state — must be OUTSIDE columns ──────────
if 'bmi_history' not in st.session_state:
    st.session_state.bmi_history = []

# ── Layout ───────────────────────────────────────────
main_col1, main_col2 = st.columns([1, 1.2], gap="large")

with main_col1:
    st.markdown("###  Enter your parameters")
    st.info("**What is BMI?** Body Mass Index uses your height and weight to estimate whether you are underweight, normal weight, overweight, or obese.")

    with st.container():
        col_a, col_g = st.columns(2)

    with col_a:
        age = st.number_input("Age (years):", min_value=1, max_value=120, value=25)

    with col_g:
        gender = st.radio("Gender:", ("Male", "Female"))

    activity_level = st.selectbox(
        "Activity level:",
        ["Sedentary", "Lightly active", "Moderately active", "Very active", "Extra active"]
    )

    # Unit selector
    unit = st.radio("Unit system:", ["Metric (kg, cm)", "Imperial (lbs, ft)"])
    st.divider()

    col_w, col_h = st.columns(2)

    with col_w:
        if unit == "Metric (kg, cm)":
            weight = st.number_input("Weight (kg):", min_value=1.0, max_value=300.0, value=70.0, step=0.5)
        else:
            weight_lbs = st.number_input("Weight (lbs):", min_value=1.0, max_value=700.0, value=154.0, step=0.5)
            weight = weight_lbs * 0.453592

    with col_h:
        if unit == "Metric (kg, cm)":
            height_cm = st.number_input("Height (cm):", min_value=50.0, max_value=250.0, value=170.0, step=0.5)
            height_m = height_cm / 100
        else:
            height_ft = st.number_input("Height (ft):", min_value=1.0, max_value=9.0, value=5.7, step=0.1)
            height_m = height_ft * 0.3048

    calculate = st.button("Calculate BMI ", use_container_width=True)

# ── Results column ────────────────────────────────────
with main_col2:
    if calculate:
        # ── BMI calculation ──
        bmi = weight / (height_m ** 2)

        # ── Category ──
        if bmi < 18.5:
            category = "Underweight"
            color = "#3498db"
            advice = "You may need to increase calorie intake. Consult a nutritionist."
        elif bmi < 25:
            category = "Normal weight"
            color = "#2ecc71"
            advice = "Great! Maintain your current lifestyle with regular exercise and a balanced diet."
        elif bmi < 30:
            category = "Overweight"
            color = "#f39c12"
            advice = "Consider light exercise and dietary improvements. Consult your doctor."
        else:
            category = "Obese"
            color = "#e74c3c"
            advice = "Please consult a healthcare professional for a personalised plan."

        # ── Activity multiplier for TDEE ──
        activity_multipliers = {
            "Sedentary": 1.2,
            "Lightly active": 1.375,
            "Moderately active": 1.55,
            "Very active": 1.725,
            "Extra active": 1.9
        }
        multiplier = activity_multipliers[activity_level]

        # ── BMR (Mifflin-St Jeor) ──
        if gender == "Male":
            bmr = 10 * weight + 6.25 * (height_m * 100) - 5 * age + 5
        else:
            bmr = 10 * weight + 6.25 * (height_m * 100) - 5 * age - 161

        tdee = bmr * multiplier

        # ── Save to history ──
        st.session_state.bmi_history.append({
            "time": datetime.now().strftime("%H:%M:%S"),
            "bmi": round(bmi, 1),
            "category": category
        })

        # ── Display results ──
        st.markdown("###  Your Results")

        m1, m2, m3 = st.columns(3)
        m1.metric("BMI Score", f"{bmi:.1f}")
        m2.metric("Category", category)
        m3.metric("Daily Calories (TDEE)", f"{tdee:.0f} kcal")

        # ── Colour badge ──
        st.markdown(
            f"<span class='bmi-badge' style='background-color:{color}'>{category}</span>",
            unsafe_allow_html=True
        )
        st.write("")

        # ── Advice card ──
        st.markdown(
            f"<div class='health-card'><h4> Health Advice</h4><p>{advice}</p></div>",
            unsafe_allow_html=True
        )

        # ── BMI gauge chart ──
        st.markdown("#### BMI Gauge")
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=bmi,
            title={"text": "BMI", "font": {"size": 18}},
            gauge={
                "axis": {"range": [10, 45], "tickwidth": 1},
                "bar": {"color": color},
                "steps": [
                    {"range": [10, 18.5], "color": "#aed6f1"},
                    {"range": [18.5, 25], "color": "#a9dfbf"},
                    {"range": [25, 30],  "color": "#fad7a0"},
                    {"range": [30, 45],  "color": "#f1948a"},
                ],
                "threshold": {
                    "line": {"color": "#2c3e50", "width": 4},
                    "thickness": 0.75,
                    "value": bmi
                }
            }
        ))
        fig.update_layout(
            height=280,
            margin=dict(t=40, b=10, l=20, r=20),
            paper_bgcolor="rgba(0,0,0,0)",
            font={"color": "#2c3e50"}
        )
        st.plotly_chart(fig, use_container_width=True)

        # ── Ideal weight range ──
        ideal_min = round(18.5 * height_m ** 2, 1)
        ideal_max = round(24.9 * height_m ** 2, 1)
        st.info(f" **Ideal weight range for your height:** {ideal_min} kg – {ideal_max} kg")

    else:
        st.markdown("###  Your Results")
        st.info(" Fill in your details on the left and click **Calculate BMI** to see your results.")

# ── History section ───────────────────────────────────
if st.session_state.bmi_history:
    st.divider()
    st.markdown("###  BMI History (this session)")
    history_df = pd.DataFrame(st.session_state.bmi_history)
    st.dataframe(history_df, use_container_width=True, hide_index=True)

    if st.button("Clear history"):
        st.session_state.bmi_history = []
        st.rerun()
