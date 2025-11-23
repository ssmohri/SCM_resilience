import os
from pathlib import Path
import streamlit as st
import pandas as pd
from PIL import Image

# =========================================================
# MUST BE FIRST STREAMLIT COMMAND
# =========================================================
st.set_page_config(
    page_title="Data Analytics in Supply Chain Resilience",
    page_icon="📦",
    layout="wide"
)

# =========================================================
# PATHS
# =========================================================
SCRIPT_PATH = Path(__file__).resolve()
APP_DIR = SCRIPT_PATH.parent
ASSETS_DIR = APP_DIR / "assets"

# =========================================================
# RESOLVE IMAGE PATH
# =========================================================
def resolve_image_path(basename: str):
    """
    Finds an image in assets/ by basename:
    - ignores case
    - accepts .png .jpg .jpeg .gif .webp .bmp
    - matches names starting with basename
    """
    if not ASSETS_DIR.exists():
        return None

    base_lower = basename.lower()
    img_exts = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp")

    files = list(ASSETS_DIR.iterdir())
    candidates = [f for f in files if f.name.lower().startswith(base_lower)]

    if not candidates:
        return None

    for f in candidates:
        if f.name.lower().endswith(img_exts):
            return str(f)

    return str(candidates[0])

# =========================================================
# CLEAN IMAGE DISPLAY (PIL + SMALLER SIZE)
# =========================================================
def show_image_clean(basename: str, caption: str, width: int = 600):
    """
    Clean reliable image display:
    - Loads via PIL (bypasses Streamlit media server)
    - No box / no extra UI
    - Smaller width by default
    """
    local_path = resolve_image_path(basename)
    if local_path and os.path.isfile(local_path):
        try:
            img = Image.open(local_path).convert("RGB")
            st.image(img, caption=caption, width=width)
            return
        except Exception:
            pass

    # If a file is truly missing, allow manual upload (quiet fallback)
    uploaded = st.file_uploader(
        f"Image '{basename}' missing. Upload it:",
        type=["png", "jpg", "jpeg", "gif", "webp", "bmp"],
        key=f"upload_{basename}"
    )
    if uploaded is not None:
        img = Image.open(uploaded).convert("RGB")
        st.image(img, caption=caption, width=width)

# =========================================================
# NAVIGATION
# =========================================================
PAGES = [
    "Basic (Resilience definition)",
    "Basic (Resilience Example)",
    "Basic (Data analytics definition)",
    "Opportunities",
    "Dynamic re-routing",   # <-- ADD THIS
    "Challenges",
    "Quiz"
]

page = st.sidebar.radio("Navigate", PAGES)
st.title("📦 Data Analytics in Supply Chain Resilience")

# =========================================================
# PAGE 1 — RESILIENCE DEFINITION (progressive reveal)
# =========================================================
if page == "Basic (Resilience definition)":

    # --------------------------------------------
    # Initialise step state for Page 1
    # --------------------------------------------
    if "step_p1" not in st.session_state:
        st.session_state.step_p1 = 1   # Start with step 1

    step = st.session_state.step_p1

    # ============================================
    # STEP 1 — Definition of Supply Chain Resilience
    # (show if step >= 1)
    # ============================================
    if step >= 1:
        st.markdown("""
        <div style="font-size:26px; font-weight:600; margin-bottom:6px;">
        What is supply chain resilience?
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="font-size:22px; line-height:1.6;">
        The ability of a supply chain to return to its original state or move to a new, more desirable state after being disturbed.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="font-size:14px; color:gray; margin-top:6px;">
        Ivanov, D., &amp; Dolgui, A. (2020). Viability of intertwined supply networks: extending the supply chain resilience angles.
        <i>International Journal of Production Research</i>, 58(10), 2904–2915.
        </div>
        """, unsafe_allow_html=True)

    # ============================================
    # STEP 2 — Robustness vs Resilience
    # (show if step >= 2)
    # ============================================
    if step >= 2:
        st.markdown("""
        <div style="font-size:26px; font-weight:600; margin-bottom:8px; margin-top:14px;">
        Difference Between Robustness and Resilience
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="font-size:22px; line-height:1.6; margin-left:5px;">
        • <b>Robustness</b>: Ability to resist change<br>
        • <b>Resilience</b>: Ability to recover once change has occurred
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="font-size:14px; color:gray; margin-top:6px;">
        Ukraintseva, S., Yashin, A.I. & Arbeev, K.G. (2016). Resilience versus robustness in aging.
        </div>
        """, unsafe_allow_html=True)

    # ============================================
    # STEP 3 — Diagram
    # (show if step >= 3)
    # ============================================
    if step >= 3:
        st.markdown("---")
        show_image_clean("RR_diff", "Robustness vs Resilience", width=800)

    # ============================================
    # PREVIOUS / NEXT NAVIGATION BUTTONS
    # ============================================
    col_prev, col_next = st.columns([1, 1])
    
    with col_prev:
        if step > 1:
            if st.button("⬅ Previous", key="p1_prev"):
                st.session_state.step_p1 -= 1
                st.rerun()
    
    with col_next:
        if step < 3:
            if st.button("Next ➜", key="p1_next"):
                st.session_state.step_p1 += 1
                st.rerun()


# =========================================================
# PAGE 2 — RESILIENCE EXAMPLE (Step-by-step reveal)
# =========================================================
elif page == "Basic (Resilience Example)":

    # Initialise page-specific step counter
    if "page2_step" not in st.session_state:
        st.session_state.page2_step = 1

    # Optional restart button
    if st.button("Restart Page"):
        st.session_state.page2_step = 1
        st.rerun()

    # ========== STEP 1 ==========
    if st.session_state.page2_step == 1:

        st.subheader("Toyota's Supply Chain Resilience Post-2011 Earthquake")

        st.markdown("""
        <div style="font-size:22px; line-height:1.6;">
        The 2011 Great East Japan Earthquake and tsunami caused widespread disruption to Japan’s industrial infrastructure, 
        critically impacting Toyota’s production network. As operations halted and supplier facilities were severely damaged, 
        Toyota faced a significant threat to its global supply chain continuity.
        </div>
        """, unsafe_allow_html=True)

        show_image_clean("japan", "Japan Earthquake 2011", width=800)

        # NEXT button only
        if st.button("Next ➜"):
            st.session_state.page2_step = 2
            st.rerun()

    # ========== STEP 2 (final step — ONLY Previous) ==========
    elif st.session_state.page2_step == 2:

        st.markdown("""
        <div style="font-size:22px; line-height:1.6;">
        The disaster revealed vulnerabilities in Toyota’s just-in-time (JIT) model.  
        To address this, Toyota undertook several strategic resilience-building initiatives:
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="font-size:22px; line-height:1.6; margin-left:5px;">
        • <b>Supplier diversification:</b> Reducing dependence on sole-source and geographically concentrated suppliers.<br>
        • <b>Strategic stockpiling:</b> Increasing inventory of critical parts while maintaining lean principles elsewhere.<br>
        • <b>Supply chain visibility:</b> Investing in digital platforms for real-time monitoring of supplier status and logistics risks.
        </div>
        """, unsafe_allow_html=True)

        # ONLY Previous button (no next page)
        if st.button("⬅ Previous"):
            st.session_state.page2_step = 1
            st.rerun()

# =========================================================
# PAGE 3 — DATA ANALYTICS DEFINITION (Step-by-step reveal)
# =========================================================
elif page == "Basic (Data analytics definition)":

    # Initialise step counter
    if "page3_step" not in st.session_state:
        st.session_state.page3_step = 1

    # Reset button (optional)
    if st.button("Restart Page"):
        st.session_state.page3_step = 1
        st.rerun()

    step = st.session_state.page3_step

    # ============================
    # STEP 1 (show only in steps 1 and 2)
    # ============================
    if step in [1, 2]:
        st.subheader("What is data analytics?")
        st.markdown("""
        <div style="font-size:22px; line-height:1.6;">
        Data analytics is the process of systematically collecting, cleaning, transforming, and analysing data  
        to extract meaningful insights and support better decision-making.

        Supply chains generate massive data → analytics helps organisations <b>see early</b>, <b>react fast</b>, and <b>plan ahead</b>.
        </div>
        """, unsafe_allow_html=True)

        # NEXT button for Step 1
        if step == 1:
            if st.button("Next ➜"):
                st.session_state.page3_step = 2
                st.rerun()

    # ============================
    # STEP 2 (append after Step 1)
    # ============================
    if step == 2:
        st.subheader("From Data to Information")
        st.markdown("""
        <div style="display:flex; align-items:center; gap:25px; flex-wrap:wrap;">
            <div style="border:1px solid #444; padding:6px 20px; border-radius:6px;">Data</div>
            <div>➡ <i>technique</i> ➡</div>
            <div style="border:1px solid #444; padding:6px 20px; border-radius:6px;">Information</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        col_prev, col_next = st.columns([1, 1])
        with col_prev:
            if st.button("⬅ Previous"):
                st.session_state.page3_step = 1
                st.rerun()
        with col_next:
            if st.button("Next ➜"):
                st.session_state.page3_step = 3
                st.rerun()

    # ============================
    # STEP 3 (final step — hide ALL previous)
    # ============================
    if step == 3:
        st.subheader("Main Types of Data Analytics")

        df = pd.DataFrame({
            "Type": ["Descriptive Analytics", "Predictive Analytics", "Prescriptive Analytics"],
            "Purpose": [
                "Summarises past data to show what happened",
                "Uses historical data to forecast future trends",
                "Recommends actions based on analysis"
            ],
            "Example": [
                "Sales reports, performance dashboards",
                "Demand forecasting, risk modelling",
                "Route optimisation, inventory management"
            ]
        })
        st.table(df)

        st.markdown("---")
        show_image_clean("data", "Data analytics illustration", width=1200)

        # Only PREVIOUS button (last step)
        if st.button("⬅ Previous"):
            st.session_state.page3_step = 2
            st.rerun()



# =========================================================
# PAGE 4 — OPPORTUNITIES (Step-by-step reveal)
# =========================================================
elif page == "Opportunities":

    # Initialise step counter
    if "page4_step" not in st.session_state:
        st.session_state.page4_step = 1

    # Optional restart
    if st.button("Restart Page", key="p4_restart"):
        st.session_state.page4_step = 1
        st.rerun()

    step = st.session_state.page4_step

    # ============================
    # STEP 1 — Intro + First Image
    # ============================
    if step == 1:

        st.markdown("""
        <div style="font-size:22px; line-height:1.6;">
        Data analytics provides valuable opportunities for increasing resilience in supply chains.  
        In this context, we explore key opportunities offered by various analytical techniques 
        across different phases of disaster and disruption management.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="margin-left:160px;">
        """, unsafe_allow_html=True)
        
        show_image_clean("disaster", "Disaster and disruption phases overview", width=600)
        
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")

        if st.button("Next ➜", key="p4_next1"):
            st.session_state.page4_step = 2
            st.rerun()

    # ============================
    # STEP 2 — Second Image + References
    # ============================
    elif step == 2:

        # Center second image too
        st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
        show_image_clean("2d", "Opportunities across disaster phases", width=1200)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")

        st.markdown("""
        <small>
        Tian, Y. & Cui, L. (2025). Supply chain resilience and digital transformation: perspectives from a supply chain network. 
        <em>Humanities and Social Sciences Communications</em>, 12(1), 1738.<br><br>

        Zamani, E.D., Smyth, C., Gupta, S. & Dennehy, D. (2023).  
        Artificial intelligence and big data analytics for supply chain resilience: a systematic literature review.  
        <em>Annals of Operations Research</em>, 327(2), 605–632.<br><br>

        Adewusi, A.O., Komolafe, A.M., Ejairu, E., Aderotoye, I.A., Abiona, O.O. & Oyeniran, O.C. (2024).  
        The role of predictive analytics in optimizing supply chain resilience: techniques and case studies.  
        <em>International Journal of Management & Entrepreneurship Research</em>, 6(3), 815–837.
        </small>
        """, unsafe_allow_html=True)

        if st.button("⬅ Previous", key="p4_prev2"):
            st.session_state.page4_step = 1
            st.rerun()



# =========================================================
# PAGE 5 — CHALLENGES
# =========================================================
elif page == "Challenges":

    st.markdown("""
    <div style="font-size:22px; line-height:1.6;">
    Applying data analytics for supply chain resilience is powerful but not easy.  
    Organisations face several challenges when trying to use analytics in practice.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    show_image_clean("challenges", "Key challenges", width=1200)

    st.markdown("---")
    st.markdown("""
    <small>
    Iftikhar, A., Ali, I., Arslan, A. and Tarba, S., 2024. Digital innovation, data analytics, and supply chain resiliency. 
    <em>Annals of Operations Research</em>, 333(2), pp.825–848.<br>
    Hosseini Shekarabi, S.A., Kiani Mavi, R. and Romero Macau, F., 2025. Supply chain resilience: a critical review. 
    <em>Global Journal of Flexible Systems Management</em>, pp.1–55.
    </small>
    """, unsafe_allow_html=True)

# =========================================================
# PAGE 6 — QUIZ
# =========================================================
elif page == "Quiz":

    import datetime
    import matplotlib.pyplot as plt

    # ---------- Persistent CSV path inside assets ----------
    SCORES_CSV = ASSETS_DIR / "quiz_scores.csv"

    # ---------- Session state ----------
    if "quiz_started" not in st.session_state:
        st.session_state.quiz_started = False
        st.session_state.selected_hazard = None
        st.session_state.current_q = 0
        st.session_state.score = 0
        st.session_state.answered = False
        st.session_state.last_feedback = ""

        # new states for username + saving
        st.session_state.username = ""
        st.session_state.username_set = False
        st.session_state.score_saved = False

    # ---------- Hazards (more disaster-focused, mixed types) ----------
    hazards = [
        "Earthquake (industrial zone)",
        "Flood (urban logistics network)",
        "Wildfire (regional supply routes)",
        "Pandemic (workforce + demand shock)",
        "Cyberattack (IT / visibility outage)",
        "Port Strike (international imports)",
        "Fuel Crisis (price spike + shortages)",
        "Major Highway Collapse (critical corridor)",
        "Extreme Heatwave (cold-chain risk)",
        "Severe Storm / Cyclone (multi-node disruption)"
    ]

    # ---------- 5 questions per hazard ----------
    hazard_questions = {
        "Earthquake (industrial zone)": [
            ("After a major earthquake damages factories and roads in one region, your company wants a quick picture of what happened. "
             "You compile a dashboard showing which suppliers are offline, which lanes are blocked, and how deliveries performed in the last 48 hours.",
             "Descriptive", "Response"),
            ("You use historical earthquake impacts and current sensor/traffic updates to estimate how long each damaged lane will remain disrupted "
             "and which distribution centres are most likely to face stockouts next week.",
             "Predictive", "Preparedness"),
            ("Based on predicted lane recovery times, you decide how to reassign customers to alternative DCs and reroute shipments to minimise total delay and cost.",
             "Prescriptive", "Response"),
            ("You review post-event performance to compare time-to-recovery and cost overruns across products, regions, and partners.",
             "Descriptive", "Recovery"),
            ("You redesign the supplier base by selecting backup suppliers in safer zones and setting minimum inventory buffers for critical parts.",
             "Prescriptive", "Mitigation"),
        ],

        "Flood (urban logistics network)": [
            ("During heavy flooding, you map real-time courier failures and late deliveries across suburbs to understand the most affected zones.",
             "Descriptive", "Response"),
            ("Using rainfall forecasts, river-level sensors, and past flood patterns, you estimate which warehouses will become inaccessible within 24–48 hours.",
             "Predictive", "Preparedness"),
            ("You choose which customer orders to prioritise, which to postpone, and which temporary staging areas to activate to maintain service.",
             "Prescriptive", "Response"),
            ("You calculate how much extra travel was induced by flood detours and which carriers were most resilient.",
             "Descriptive", "Recovery"),
            ("Before the next rainy season, you simulate alternative depot locations to reduce exposure to flood-prone corridors.",
             "Prescriptive", "Mitigation"),
        ],

        "Wildfire (regional supply routes)": [
            ("A wildfire closes several highways. You summarise yesterday’s delivery delays by route and carrier to see the immediate damage.",
             "Descriptive", "Response"),
            ("You use wind direction, satellite fire spread data, and traffic feeds to forecast which routes are likely to close next and for how long.",
             "Predictive", "Response"),
            ("Given predicted closures, you compute the best re-routing and temporary micro-hub placement to keep deliveries moving.",
             "Prescriptive", "Response"),
            ("After the event, you analyse recovery speed and the cost of emergency transport per product category.",
             "Descriptive", "Recovery"),
            ("You identify high-risk rural suppliers and add redundancy (multiple suppliers + stock buffers) for future fire seasons.",
             "Prescriptive", "Mitigation"),
        ],

        "Pandemic (workforce + demand shock)": [
            ("You track daily order volumes, absentee rates, and warehouse throughput to understand how the pandemic is affecting operations right now.",
             "Descriptive", "Response"),
            ("You forecast future demand spikes for essentials and predict staffing shortages using infection trend data.",
             "Predictive", "Preparedness"),
            ("You decide how to allocate scarce labour and transport capacity across products and regions to maintain essential supply.",
             "Prescriptive", "Response"),
            ("You review which emergency policies (extra shifts, priority lanes) worked best and how quickly performance recovered.",
             "Descriptive", "Recovery"),
            ("You set long-term contingency plans such as cross-training staff and contracting flexible transport providers.",
             "Prescriptive", "Mitigation"),
        ],

        "Cyberattack (IT / visibility outage)": [
            ("After a cyberattack disables tracking, you report which systems are down and what shipment data is missing.",
             "Descriptive", "Response"),
            ("You estimate the likely delay growth over the next 2–3 days by comparing with past IT outage cases.",
             "Predictive", "Response"),
            ("You switch to manual routing rules and decide which shipments should be diverted or held to minimise knock-on disruption.",
             "Prescriptive", "Response"),
            ("You quantify recovery time and the financial impact of losing real-time visibility.",
             "Descriptive", "Recovery"),
            ("You invest in redundant data systems and cybersecurity monitoring to reduce attack vulnerability.",
             "Prescriptive", "Mitigation"),
        ],

        "Port Strike (international imports)": [
            ("You summarise which inbound containers are delayed, by commodity and origin port, to see what is immediately affected.",
             "Descriptive", "Response"),
            ("You forecast inventory depletion dates at each DC based on strike duration scenarios.",
             "Predictive", "Preparedness"),
            ("You decide how to reallocate remaining stock and which substitute products to ship to priority customers.",
             "Prescriptive", "Response"),
            ("You evaluate the strike’s long-term cost impact and which suppliers were most critical.",
             "Descriptive", "Recovery"),
            ("You diversify ports and add alternative shipping options to reduce dependence on a single gateway.",
             "Prescriptive", "Mitigation"),
        ],

        "Fuel Crisis (price spike + shortages)": [
            ("You monitor route costs and fuel usage trends over the last week to quantify the immediate shock.",
             "Descriptive", "Response"),
            ("You predict how fuel price trajectories will affect transport costs next month.",
             "Predictive", "Preparedness"),
            ("You redesign delivery schedules and consolidate loads to minimise fuel burn while maintaining service levels.",
             "Prescriptive", "Response"),
            ("You assess which fleet types and regions recovered fastest from cost increases.",
             "Descriptive", "Recovery"),
            ("You plan a gradual shift to EVs and alternative fuels to reduce future exposure.",
             "Prescriptive", "Mitigation"),
        ],

        "Major Highway Collapse (critical corridor)": [
            ("You map which shipments failed yesterday due to the collapsed corridor.",
             "Descriptive", "Response"),
            ("You forecast detour congestion impacts over the next two weeks using live traffic feeds.",
             "Predictive", "Response"),
            ("You compute optimal reroutes and revise delivery time windows to reduce penalty costs.",
             "Prescriptive", "Response"),
            ("You review recovery costs and service disruptions by partner carrier.",
             "Descriptive", "Recovery"),
            ("You simulate alternative hub locations to reduce reliance on single corridors.",
             "Prescriptive", "Mitigation"),
        ],

        "Extreme Heatwave (cold-chain risk)": [
            ("You report which refrigerated shipments experienced temperature excursions in the last 24 hours.",
             "Descriptive", "Response"),
            ("You forecast which routes are most likely to breach temperature limits tomorrow given weather predictions.",
             "Predictive", "Preparedness"),
            ("You decide which routes need extra cooling resources or faster transport modes.",
             "Prescriptive", "Response"),
            ("You analyse recovery time and product loss costs after the heatwave.",
             "Descriptive", "Recovery"),
            ("You upgrade packaging and cooling capacity for long-term resilience.",
             "Prescriptive", "Mitigation"),
        ],

        "Severe Storm / Cyclone (multi-node disruption)": [
            ("You summarise which depots and lanes are disrupted right now to understand the storm’s footprint.",
             "Descriptive", "Response"),
            ("You predict likely closure times and demand surges in affected regions using storm-track forecasts.",
             "Predictive", "Preparedness"),
            ("You choose emergency stock positioning and rerouting plans to keep essential flows running.",
             "Prescriptive", "Response"),
            ("You evaluate which emergency actions shortened recovery time.",
             "Descriptive", "Recovery"),
            ("You build redundancy into depot networks and carriers for future storms.",
             "Prescriptive", "Mitigation"),
        ],
    }

    # ---------- STEP 1: Choose hazard ----------
    if not st.session_state.quiz_started:
        st.subheader("Step 1 — Choose a disruption scenario")
        cols = st.columns(2)
        for i, h in enumerate(hazards):
            if cols[i % 2].button(h, use_container_width=True):
                st.session_state.quiz_started = True
                st.session_state.selected_hazard = h
                st.session_state.current_q = 0
                st.session_state.score = 0
                st.session_state.answered = False
                st.session_state.last_feedback = ""
                st.session_state.username_set = False
                st.session_state.score_saved = False
                st.rerun()

    # ---------- STEP 1.5: Ask username ----------
    elif not st.session_state.username_set:
        st.markdown(
            f"""
            <div style="font-size:22px; font-weight:700; margin-bottom:8px;">
                Scenario selected: {st.session_state.selected_hazard}
            </div>
            <div style="font-size:18px; margin-bottom:10px;">
                Please enter your username to start the quiz:
            </div>
            """,
            unsafe_allow_html=True
        )

        username_input = st.text_input("Username", value=st.session_state.username)

        colA, colB = st.columns([1, 3])
        with colA:
            if st.button("Start quiz"):
                if username_input.strip() == "":
                    st.error("Please enter a username.")
                else:
                    st.session_state.username = username_input.strip()
                    st.session_state.username_set = True
                    st.rerun()

        with colB:
            if st.button("Back to scenarios"):
                st.session_state.quiz_started = False
                st.session_state.selected_hazard = None
                st.rerun()

    # ---------- STEP 2: Quiz ----------
    else:
        selected = st.session_state.selected_hazard
        questions = hazard_questions[selected]
        q = st.session_state.current_q

        if q < len(questions):
            qtext, correct_type, correct_phase = questions[q]

            # Big scenario & question text
            st.markdown(
                f"""
                <div style="font-size:22px; font-weight:700; margin-bottom:6px;">
                    Scenario: {selected}
                </div>
                <div style="font-size:20px; margin-bottom:10px;">
                    Question {q+1} of {len(questions)}
                </div>
                <div style="font-size:19px; line-height:1.6; margin-bottom:12px;">
                    {qtext}
                </div>
                """,
                unsafe_allow_html=True
            )

            ans_type = st.radio(
                "Analytics Type:",
                ["Descriptive", "Predictive", "Prescriptive"],
                key=f"type_{q}"
            )
            ans_phase = st.radio(
                "Disruption Phase:",
                ["Mitigation", "Preparedness", "Response", "Recovery"],
                key=f"phase_{q}"
            )

            # Submit only if not answered yet
            if not st.session_state.answered:
                if st.button("Submit answer"):
                    if ans_type == correct_type and ans_phase == correct_phase:
                        st.session_state.score += 1
                        st.session_state.last_feedback = (
                            f"✅ Correct! This is **{correct_type}** analytics in the **{correct_phase}** phase."
                        )
                    else:
                        st.session_state.last_feedback = (
                            f"❌ Not quite. The correct answer is **{correct_type}** analytics in the **{correct_phase}** phase."
                        )
                    st.session_state.answered = True
                    st.rerun()

            # After submit, show feedback + Next button
            else:
                st.markdown(st.session_state.last_feedback)
                st.markdown("---")
                if st.button("Next question ➜"):
                    st.session_state.current_q += 1
                    st.session_state.answered = False
                    st.session_state.last_feedback = ""
                    st.rerun()

        # ---------- END OF QUIZ ----------
        else:
            total_q = len(questions)
            final_score = st.session_state.score
            username = st.session_state.username

            st.success(f"Quiz complete! **{username}**, your score: {final_score} / {total_q}")

            # ---- Save score once per attempt ----
            if not st.session_state.score_saved:
                new_row = pd.DataFrame([{
                    "username": username,
                    "hazard": selected,
                    "score": final_score,
                    "total": total_q,
                    "timestamp": datetime.datetime.now().isoformat(timespec="seconds")
                }])

                if SCORES_CSV.exists():
                    old = pd.read_csv(SCORES_CSV)
                    updated = pd.concat([old, new_row], ignore_index=True)
                else:
                    updated = new_row

                updated.to_csv(SCORES_CSV, index=False)
                st.session_state.score_saved = True

            # ---- Load all scores for chart ----
            if SCORES_CSV.exists():
                df_scores = pd.read_csv(SCORES_CSV)

                # keep latest attempt per username
                df_scores["timestamp"] = pd.to_datetime(df_scores["timestamp"], errors="coerce")
                df_latest = (
                    df_scores.sort_values("timestamp")
                    .groupby("username", as_index=False)
                    .tail(1)
                )

                # sort by score descending for nicer plot
                df_latest = df_latest.sort_values("score", ascending=False)

                labels = df_latest["username"].tolist()
                values = df_latest["score"].tolist()
                colors = ["red" if u == username else "blue" for u in labels]

                fig, ax = plt.subplots(figsize=(8, 4.5))
                ax.bar(labels, values, color=colors)
                ax.set_xlabel("Username")
                ax.set_ylabel("Score")
                ax.set_title("Scores of all players so far")
                ax.tick_params(axis="x", rotation=45)

                st.pyplot(fig)

            st.markdown("---")
            if st.button("Restart quiz"):
                st.session_state.quiz_started = False
                st.session_state.selected_hazard = None
                st.session_state.current_q = 0
                st.session_state.score = 0
                st.session_state.answered = False
                st.session_state.last_feedback = ""
                st.session_state.username = ""
                st.session_state.username_set = False
                st.session_state.score_saved = False
                st.rerun()


# =========================================================
# PAGE X — DYNAMIC RE-ROUTING (5×5, 12 retailers, improved UI)
# =========================================================
elif page == "Dynamic re-routing":

    import random
    import matplotlib.pyplot as plt

    GRID = 5
    NUM_RETAILERS = 12

    # -------------------------------------------------------
    # Step controller: 1 = intro, 2 = game
    # -------------------------------------------------------
    if "dr_step" not in st.session_state:
        st.session_state.dr_step = 1

    # -------------------------------------------------------
    # Helpers
    # -------------------------------------------------------
    def edge(a, b):
        return tuple(sorted([a, b]))

    def route_distance(r):
        return max(0, len(r) - 1)

    # Generate warehouse + retailer positions
    def init_problem():
        random.seed(42)
        warehouse = (GRID // 2, GRID // 2)
        all_nodes = [(i, j) for i in range(GRID) for j in range(GRID)]
        all_nodes.remove(warehouse)
        retailers = random.sample(all_nodes, NUM_RETAILERS)
        return warehouse, retailers

    # Select random closed edges from the route
    def make_closures(route):
        edges_on_route = [edge(route[i], route[i+1]) for i in range(len(route)-1)]
        unique_edges = list(dict.fromkeys(edges_on_route))
        k = min(4, max(2, len(unique_edges)//5))
        return set(random.sample(unique_edges, k))

    # -------------------------------------------------------
    # Draw the grid and route (with improved sizing)
    # -------------------------------------------------------
    def draw_scene(route, retailers, warehouse, closed_edges, title):

        fig, ax = plt.subplots(figsize=(2.45, 2.45))

        # Grid lines
        for i in range(GRID):
            ax.plot([0, GRID-1], [i, i], linewidth=1, alpha=0.45, color="black")
            ax.plot([i, i], [0, GRID-1], linewidth=1, alpha=0.45, color="black")

        # Closed edges
        for (u, v) in closed_edges:
            (x1, y1), (x2, y2) = u, v
            ax.plot([x1, x2], [y1, y2], linewidth=3, alpha=0.95, color="red")

        # Retailers — half size
        rx = [p[0] for p in retailers]
        ry = [p[1] for p in retailers]
        ax.scatter(rx, ry, s=28, marker="s", label="Retailer", color="black")

        # Warehouse — half size
        ax.scatter([warehouse[0]], [warehouse[1]],
                   s=60, marker="*", label="Warehouse", color="black")

        # Route
        if len(route) > 1:
            xs = [p[0] for p in route]
            ys = [p[1] for p in route]
            ax.plot(xs, ys, linewidth=3, color="black")

        # Axes formatting
        ax.set_xlim(-0.5, GRID - 0.5)
        ax.set_ylim(-0.5, GRID - 0.5)
        ax.set_xticks(range(GRID))
        ax.set_yticks(range(GRID))
        ax.set_aspect("equal")
        ax.tick_params(axis="both", labelsize=6)

        ax.set_title(title, fontsize=6)

        # Legend with padding
        ax.legend(
            loc="center left",
            bbox_to_anchor=(1.02, 0.5),
            fontsize=5,
            frameon=True,
            borderpad=0.6,
            labelspacing=0.4,
            handletextpad=0.6,
            borderaxespad=0.8
        )

        ax.grid(False)
        st.pyplot(fig)

    # -------------------------------------------------------
    # STEP 1 — Intro
    # -------------------------------------------------------
    if st.session_state.dr_step == 1:

        st.subheader("Dynamic re-routing: build a resilient delivery tour")

        st.markdown("""
        <div style="font-size:18px; line-height:1.6;">
        You are operating on a <b>5×5 grid</b>. You can move only along grid links (up, down, left, right).  
        There is <b>1 warehouse</b> and <b>12 retailers</b>.<br><br>

        <b>Task 1:</b> Build a route that starts at the warehouse, visits all retailers, and returns to the warehouse.<br>
        <b>Task 2:</b> After road closures (red links), re-route to complete the tour again.<br><br>

        This demonstrates how <b>resilient routing</b> reduces disruption impact.
        </div>
        """, unsafe_allow_html=True)

        if st.button("Next ➜ Start the game"):
            st.session_state.dr_step = 2
            st.rerun()

    # -------------------------------------------------------
    # STEP 2 — Main Game
    # -------------------------------------------------------
    else:

        # -----------------------------------------
        # Session state initialisation
        # -----------------------------------------
        if "dr_warehouse" not in st.session_state:
            wh, ret = init_problem()
            st.session_state.dr_warehouse = wh
            st.session_state.dr_retailers = ret
            st.session_state.dr_route = [wh]
            st.session_state.dr_visited = set()
            st.session_state.dr_phase = "initial"
            st.session_state.dr_closed = set()
            st.session_state.dr_initial_dist = None
            st.session_state.dr_reroute_dist = None

        warehouse = st.session_state.dr_warehouse
        retailers = st.session_state.dr_retailers
        route = st.session_state.dr_route
        visited = st.session_state.dr_visited
        phase = st.session_state.dr_phase
        closed_edges = st.session_state.dr_closed
        current = route[-1]

        # -----------------------------------------
        # Layout: plot left, stats right
        # -----------------------------------------
        col_plot, col_stats = st.columns([1.1, 0.9], gap="large")

        with col_plot:
            title = (
                "Task 1: Build your first tour" if phase == "initial"
                else "Task 2: Re-route with closures (red links)"
            )
            draw_scene(route, retailers, warehouse, closed_edges, title)

        with col_stats:
            remaining = len(set(retailers) - visited)
            st.markdown(
                f"""
                <div style="font-size:18px; line-height:1.6; padding-left:25px;">
                <b>Current location:</b> {current} <br><br>
                <b>Retailers visited:</b> {len(visited)} / {NUM_RETAILERS} <br>
                <b>Remaining:</b> {remaining} <br><br>
                <b>Distance so far:</b> {route_distance(route)}
                </div>
                """,
                unsafe_allow_html=True
            )

        # -----------------------------------------
        # Movement buttons (compact D-pad)
        # -----------------------------------------
        st.markdown("<div style='font-size:18px; font-weight:600;'>Choose your next link:</div>",
                    unsafe_allow_html=True)

        def attempt_move(dx, dy):
            x, y = current
            nxt = (x + dx, y + dy)

            if not (0 <= nxt[0] < GRID and 0 <= nxt[1] < GRID):
                st.warning("You cannot move outside the grid.")
                return

            e = edge(current, nxt)
            if phase == "reroute" and e in closed_edges:
                st.error("That link is closed (red). Choose another direction.")
                return

            route.append(nxt)
            st.session_state.dr_route = route

            if nxt in retailers:
                visited.add(nxt)
                st.session_state.dr_visited = visited

            st.rerun()

        # Up
        row1 = st.columns([1, 1, 1])
        with row1[1]:
            if st.button("⬆️ Up"):
                attempt_move(0, 1)

        # Left / Right
        row2 = st.columns([1, 1, 1])
        with row2[0]:
            if st.button("⬅️ Left"):
                attempt_move(-1, 0)
        with row2[2]:
            if st.button("➡️ Right"):
                attempt_move(1, 0)

        # Down
        row3 = st.columns([1, 1, 1])
        with row3[1]:
            if st.button("⬇️ Down"):
                attempt_move(0, -1)

        # -----------------------------------------
        # Undo / Reset
        # -----------------------------------------
        st.markdown("---")
        colU, colR = st.columns([1, 1])

        with colU:
            if st.button("Undo last move"):
                if len(route) > 1:
                    route.pop()
                    st.session_state.dr_route = route
                    st.session_state.dr_visited = {
                        n for n in route if n in retailers
                    }
                    st.rerun()

        with colR:
            if st.button("Reset route"):
                st.session_state.dr_route = [warehouse]
                st.session_state.dr_visited = set()
                st.rerun()

        # -----------------------------------------
        # Completion logic
        # -----------------------------------------
        def is_complete_tour():
            return (
                len(visited) == NUM_RETAILERS
                and current == warehouse
                and len(route) > 1
            )

        if is_complete_tour():

            # First pass
            if phase == "initial":
                dist1 = route_distance(route)
                st.success(f"Initial complete! Distance = {dist1}")
                st.session_state.dr_initial_dist = dist1
                st.session_state.dr_closed = make_closures(route)
                st.session_state.dr_phase = "reroute"
                st.session_state.dr_route = [warehouse]
                st.session_state.dr_visited = set()
                st.info("Some links are now closed (red). Re-route to complete the task.")
                st.rerun()

            # Second pass (reroute)
            else:
                dist2 = route_distance(route)
                dist1 = st.session_state.dr_initial_dist
                deviation = ((dist2 - dist1) / dist1) * 100 if dist1 else 0

                st.success(f"Re-routing complete! New distance = {dist2}")
                st.markdown(
                    f"<div style='font-size:20px;'>Deviation from original = <b>{deviation:.1f}%</b></div>",
                    unsafe_allow_html=True
                )

                if st.button("Start a new problem"):
                    wh, ret = init_problem()
                    st.session_state.dr_warehouse = wh
                    st.session_state.dr_retailers = ret
                    st.session_state.dr_route = [wh]
                    st.session_state.dr_visited = set()
                    st.session_state.dr_phase = "initial"
                    st.session_state.dr_closed = set()
                    st.session_state.dr_initial_dist = None
                    st.session_state.dr_reroute_dist = None
                    st.rerun()

