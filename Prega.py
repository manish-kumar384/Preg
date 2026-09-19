import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import json

# ==========================================
# 1. APP CONFIG & SOOTHING THEME
# ==========================================
st.set_page_config(
    page_title="Bloom — Pregnancy Journey & Journal",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Gentle, calm aesthetic styling with warm neutrals, soft sage, and muted blush
CALM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Quicksand', sans-serif;
        color: #4A4036;
    }
    .stApp {
        background-color: #FAF7F2;
    }
    .main-card {
        background: #FFFFFF;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 18px rgba(180, 160, 140, 0.08);
        margin-bottom: 20px;
        border: 1px solid #F0EAE1;
    }
    .metric-bubble {
        background: #F4EBE2;
        border-radius: 14px;
        padding: 16px 20px;
        text-align: center;
        border: 1px solid #EADBCC;
    }
    .metric-val {
        font-size: 1.8rem;
        font-weight: 700;
        color: #8C6D62;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #7D746B;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .highlight-pill {
        background: #E8EFE9;
        color: #4A6B53;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
        display: inline-block;
    }
    .stButton>button {
        border-radius: 12px;
        border: 1px solid #D8C7B8;
        background-color: #F8F3ED;
        color: #5C4B41;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background-color: #EFE6DC;
        border-color: #CBB4A1;
        color: #3B2E27;
    }
</style>
"""
st.markdown(CALM_CSS, unsafe_allow_html=True)

# ==========================================
# 2. EMBEDDED KNOWLEDGE & MILESTONES DATA
# ==========================================
WEEKS_DATA = {
    4: {"size": "Poppy seed", "len": "1 mm", "wt": "< 1 g", "milestone": "Implantation complete; amniotic sac begins forming."},
    8: {"size": "Raspberry", "len": "1.6 cm", "wt": "1 g", "milestone": "Webbed fingers and toes emerge; neural pathways branch out."},
    12: {"size": "Plum", "len": "5.4 cm", "wt": "14 g", "milestone": "Reflexes develop; fingernails and kidneys begin operating."},
    16: {"size": "Avocado", "len": "11.6 cm", "wt": "100 g", "milestone": "Eyes can make subtle movements; quickening flutters may begin."},
    20: {"size": "Banana", "len": "25.6 cm", "wt": "300 g", "milestone": "Halfway milestone; anatomy ultrasound and distinct kicks."},
    24: {"size": "Cantaloupe", "len": "30 cm", "wt": "600 g", "milestone": "Lungs develop surfactant branches; responsive to familiar voices."},
    28: {"size": "Eggplant", "len": "37.6 cm", "wt": "1.0 kg", "milestone": "Welcome to Trimester 3; eyelashes blink open and close."},
    32: {"size": "Jicama", "len": "42.4 cm", "wt": "1.7 kg", "milestone": "Bones continue hardening; sleep and active cycles form."},
    36: {"size": "Honeydew melon", "len": "47.4 cm", "wt": "2.6 kg", "milestone": "Lungs nearly mature; baby drops closer into pelvic cradle."},
    40: {"size": "Watermelon", "len": "51.2 cm", "wt": "3.4 kg", "milestone": "Full term; ready to meet family and greet the world."},
}

DEFAULT_CHECKLIST = [
    {"cat": "Hospital Bag (Mom)", "item": "Warm comfortable non-slip socks & slippers", "done": False},
    {"cat": "Hospital Bag (Mom)", "item": "Loose button-down robe & soft nightgown", "done": False},
    {"cat": "Hospital Bag (Mom)", "item": "Long phone charger cable & lip balm", "done": True},
    {"cat": "Hospital Bag (Mom)", "item": "Comfortable nursing bras & soft pads", "done": False},
    {"cat": "Hospital Bag (Baby)", "item": "Installed rear-facing infant car seat", "done": False},
    {"cat": "Hospital Bag (Baby)", "item": "2-3 soft newborn onesies & knotted gowns", "done": False},
    {"cat": "Hospital Bag (Baby)", "item": "Swaddle blankets & gentle newborn hat", "done": False},
    {"cat": "Nursery & Home Prep", "item": "Washed baby bedding and clothes", "done": False},
    {"cat": "Nursery & Home Prep", "item": "Safe sleep crib or bassinet assembled", "done": False},
    {"cat": "Nursery & Home Prep", "item": "Batch freeze healthy postpartum meals", "done": False},
]

APPOINTMENTS_DATA = [
    {"week": 8, "title": "First Confirmation Ultrasound & Baseline Labs", "focus": "Heartbeat detection, due date confirmation, routine panel."},
    {"week": 12, "title": "Nuchal Translucency (NT) & Optional Cell-Free DNA", "focus": "Chromosomal wellness screening & early anatomical view."},
    {"week": 20, "title": "Detailed Mid-Pregnancy Anatomy Scan", "focus": "Complete structural review from head to toe, heart chambers, fluid check."},
    {"week": 28, "title": "Glucose Tolerance Screen & Rh Incompatibility Check", "focus": "Gestational diabetes screening & vital maternal blood counts."},
    {"week": 36, "title": "Group B Strep (GBS) Screen & Growth Assessment", "focus": "Gentle swab, monitoring fetal position and delivery roadmap."},
]

# ==========================================
# 3. STATE INITIALIZATION
# ==========================================
if "conception_or_due" not in st.session_state:
    st.session_state.conception_or_due = date.today() + timedelta(weeks=26)
if "calc_method" not in st.session_state:
    st.session_state.calc_method = "Due Date"
if "journal_entries" not in st.session_state:
    st.session_state.journal_entries = [
        {"date": str(date.today() - timedelta(days=18)), "week": 12, "mood": "Serene 🌿", "symptoms": ["Mild Fatigue"], "notes": "Heard the strong, steady heartbeat for the first time. Pure relief.", "photo_caption": "First ultrasound keepsake"},
        {"date": str(date.today() - timedelta(days=4)), "week": 14, "mood": "Energetic ☀️", "symptoms": ["Hunger Waves"], "notes": "Second trimester energy has kicked in. Went for a tranquil morning garden walk.", "photo_caption": ""},
    ]
if "kick_sessions" not in st.session_state:
    st.session_state.kick_sessions = [
        {"timestamp": (datetime.now() - timedelta(hours=36)).strftime("%Y-%m-%d %H:%M"), "count": 10, "minutes": 18, "notes": "Very active right after a cool glass of apple juice."},
        {"timestamp": (datetime.now() - timedelta(hours=14)).strftime("%Y-%m-%d %H:%M"), "count": 10, "minutes": 22, "notes": "Evening kicks while listening to acoustic music."},
    ]
if "checklist" not in st.session_state:
    st.session_state.checklist = DEFAULT_CHECKLIST.copy()
if "baby_names" not in st.session_state:
    st.session_state.baby_names = [
        {"name": "Mira", "meaning": "Peace, Ocean, Wonder", "liked_by": "Both"},
        {"name": "Julian", "meaning": "Youthful, Sky father", "liked_by": "Partner"},
        {"name": "Aria", "meaning": "Gentle air, melody", "liked_by": "Mom"},
    ]

# ==========================================
# 4. HELPER COMPUTATIONS
# ==========================================
def calculate_timeline(base_date: date, method: str):
    if method == "Due Date":
        due_date = base_date
        lmp_date = due_date - timedelta(days=280)
    elif method == "First Day of Last Period (LMP)":
        lmp_date = base_date
        due_date = lmp_date + timedelta(days=280)
    else:  # Conception date
        lmp_date = base_date - timedelta(days=14)
        due_date = lmp_date + timedelta(days=280)

    days_pregnant = max(0, (date.today() - lmp_date).days)
    weeks = min(42, days_pregnant // 7)
    days_rem = days_pregnant % 7
    days_to_go = max(0, (due_date - date.today()).days)
    progress_pct = min(1.0, max(0.0, days_pregnant / 280))

    if weeks < 13:
        trimester = "1st Trimester (Nesting & Foundation)"
    elif weeks < 27:
        trimester = "2nd Trimester (The Golden Bloom)"
    else:
        trimester = "3rd Trimester (Anticipation & Arrival)"

    return {
        "lmp": lmp_date,
        "due": due_date,
        "weeks": weeks,
        "days": days_rem,
        "days_pregnant": days_pregnant,
        "days_left": days_to_go,
        "progress": progress_pct,
        "trimester": trimester
    }

def get_fruit_comparison(current_week: int):
    benchmarks = sorted(WEEKS_DATA.keys())
    closest = min(benchmarks, key=lambda w: abs(w - current_week))
    return WEEKS_DATA[closest]

# ==========================================
# 5. SIDEBAR: PERSONAL SETUP
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='color:#6B5448; margin-bottom:0;'>🌸 Bloom Sanctuary</h2>", unsafe_allow_html=True)
    st.caption("A peaceful companion for your journey to parenthood.")
    st.write("---")

    calc_method = st.selectbox(
        "Calculate journey based on:",
        ["Due Date", "First Day of Last Period (LMP)", "Conception Date"],
        index=0
    )
    st.session_state.calc_method = calc_method

    picked_date = st.date_input(
        f"Select your {calc_method.lower()}:",
        value=st.session_state.conception_or_due
    )
    st.session_state.conception_or_due = picked_date

    tl = calculate_timeline(picked_date, calc_method)

    st.write("---")
    st.markdown("### 🕊️ Today's Daily Affirmation")
    affirmations = [
        "My body knows exactly how to nurture, shelter, and grow this precious life.",
        "I welcome each feeling and change with gentle grace and patience.",
        "Peace flows through me, giving peaceful serenity to my little one.",
        "Today, I slow down, breathe deeply, and trust the innate wisdom of nature."
    ]
    st.info(affirmations[tl["weeks"] % len(affirmations)])

# ==========================================
# 6. MAIN CONTENT TABS
# ==========================================
tab_overview, tab_journal, tab_kick, tab_checklist, tab_names, tab_care = st.tabs([
    "🌿 Journey Overview",
    "📖 Memory Journal",
    "👣 Kick Counter",
    "🎒 Hospital & Nesting",
    "✨ Baby Names Garden",
    "🩺 Prenatal Milestones"
])

# ----------------------------------------------------
# TAB 1: JOURNEY OVERVIEW
# ----------------------------------------------------
with tab_overview:
    fruit = get_fruit_comparison(tl["weeks"])

    st.markdown(f"""
    <div class='main-card' style='background: linear-gradient(135deg, #FFFFFF 0%, #FAF3EC 100%);'>
        <div style='display: flex; justify-content: space-between; align-items: baseline; flex-wrap: wrap;'>
            <span class='highlight-pill'>{tl["trimester"]}</span>
            <span style='color: #8C7B70; font-size: 0.95rem;'>Estimated Due Date: <b>{tl['due'].strftime('%B %d, %Y')}</b></span>
        </div>
        <h1 style='color: #534138; margin-top: 12px; margin-bottom: 4px;'>Week {tl['weeks']} + {tl['days']} days</h1>
        <p style='color: #7A695E; font-size: 1.05rem; margin-bottom: 20px;'>{fruit["milestone"]}</p>
    </div>
    """, unsafe_allow_html=True)

    # Key Metrics Overview
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"<div class='metric-bubble'><div class='metric-val'>{tl['days_left']}</div><div class='metric-label'>Days to Welcome Baby</div></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='metric-bubble'><div class='metric-val'>{fruit['size']}</div><div class='metric-label'>Comparable Size</div></div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='metric-bubble'><div class='metric-val'>{fruit['len']}</div><div class='metric-label'>Approx. Length</div></div>", unsafe_allow_html=True)
    with c4:
        st.markdown(f"<div class='metric-bubble'><div class='metric-val'>{fruit['wt']}</div><div class='metric-label'>Approx. Weight</div></div>", unsafe_allow_html=True)

    st.write("")
    st.markdown("<p style='font-weight:600; color:#6B584D; margin-bottom:4px;'>Journey Progression</p>", unsafe_allow_html=True)
    st.progress(tl["progress"])
    st.caption(f"{int(tl['progress']*100)}% completed — Every day is an extraordinary chapter of growth.")

    st.write("---")
    st.subheader("💡 Gentle Wellness Reflection for this Stage")
    co1, co2 = st.columns(2)
    with co1:
        st.markdown("""
        **Rest & Restoration**
        * Prioritize elevated feet for 15-20 minutes in the late afternoon.
        * Stay hydrated with room-temperature water infused with lemon or mint.
        * Allow yourself afternoon micro-naps without guilt.
        """)
    with co2:
        st.markdown("""
        **Mindful Connection**
        * Spend 5 minutes every evening placing warm hands over the belly.
        * Soft humming and familiar voices stimulate auditory nerve development.
        * Simple stretching or pelvic tilts keep hips loose and comfortable.
        """)

# ----------------------------------------------------
# TAB 2: MEMORY JOURNAL
# ----------------------------------------------------
with tab_journal:
    st.subheader("📖 Your Keepsake Journal")
    st.caption("Documenting the small wonders, thoughts, and fluttery milestones you'll treasure later.")

    with st.expander("✍️ Pen a New Entry / Memory", expanded=False):
        col_j1, col_j2 = st.columns([1, 2])
        with col_j1:
            entry_date = st.date_input("Entry Date", date.today())
            entry_mood = st.selectbox("Current Mood", ["Serene 🌿", "Grateful 🌸", "A Bit Tired ☁️", "Radiant & Joyful ☀️", "Sensitive 🌊"])
            entry_symptoms = st.multiselect("Physical Signs & Sensations", [
                "Morning Sickness", "Fluttering Kicks", "Glowing Skin",
                "Heartburn", "Food Cravings", "Mild Fatigue", "Back Stretch"
            ])
            entry_caption = st.text_input("Memory Label / Tag", placeholder="e.g., Felt first kick today!")
        with col_j2:
            entry_notes = st.text_area("Your Words, Reflections & Notes to Baby", height=160, placeholder="Write a few gentle thoughts about what today felt like...")

        if st.button("Save Memory to Journal"):
            new_entry = {
                "date": str(entry_date),
                "week": tl["weeks"],
                "mood": entry_mood,
                "symptoms": entry_symptoms,
                "notes": entry_notes,
                "photo_caption": entry_caption
            }
            st.session_state.journal_entries.insert(0, new_entry)
            st.success("Memory woven into your journal archive.")

    st.write("")
    for item in st.session_state.journal_entries:
        st.markdown(f"""
        <div class='main-card'>
            <div style='display:flex; justify-content:space-between; align-items:center;'>
                <span style='font-size:1.1rem; font-weight:700; color:#5D4A3E;'>Week {item['week']} — {item['date']}</span>
                <span class='highlight-pill'>{item['mood']}</span>
            </div>
            <p style='color:#75655A; font-style:italic; margin-top:8px; margin-bottom:10px;'>"{item['notes']}"</p>
            <div style='font-size:0.85rem; color:#8D7F75;'>
                <b>Noted Sensations:</b> {', '.join(item['symptoms']) if item['symptoms'] else 'Peaceful resting'}
                {f" · <b>Tag:</b> {item['photo_caption']}" if item.get('photo_caption') else ''}
            </div>
        </div>
        """, unsafe_allow_html=True)

# ----------------------------------------------------
# TAB 3: KICK COUNTER
# ----------------------------------------------------
with tab_kick:
    st.subheader("👣 Fetal Movement & Kick Session Tracker")
    st.caption("Doctors often recommend noting the time it takes to count 10 distinct movements (usually within two hours).")

    k_col1, k_col2 = st.columns([1, 1])
    with k_col1:
        st.markdown("""
        <div class='main-card'>
            <h4>Record a Movement Session</h4>
            <p style='color:#7A6E64; font-size:0.9rem;'>Settle into a comfortable side-lying position, relax, and log when your baby is active.</p>
        </div>
        """, unsafe_allow_html=True)
        session_minutes = st.number_input("Minutes taken to reach 10 kicks:", min_value=1, max_value=180, value=20)
        session_notes = st.text_input("Context / Observations:", placeholder="e.g., After cold smoothie, music playing")

        if st.button("Save Kick Session"):
            st.session_state.kick_sessions.insert(0, {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "count": 10,
                "minutes": int(session_minutes),
                "notes": session_notes
            })
            st.success("Session saved.")

    with k_col2:
        st.markdown("#### Recent Movement Sessions")
        if st.session_state.kick_sessions:
            df_kicks = pd.DataFrame(st.session_state.kick_sessions)
            st.dataframe(df_kicks, hide_index=True, use_container_width=True)
        else:
            st.info("No recorded kick sessions yet.")

# ----------------------------------------------------
# TAB 4: HOSPITAL BAG & NESTING CHECKLIST
# ----------------------------------------------------
with tab_checklist:
    st.subheader("🎒 Hospital Bag & Home Nesting Checklist")
    st.caption("Check off items gently as you complete them so you feel confident and prepared.")

    categories = list(set(i["cat"] for i in st.session_state.checklist))
    for cat in sorted(categories):
        st.markdown(f"##### {cat}")
        items = [x for x in st.session_state.checklist if x["cat"] == cat]
        for idx, item in enumerate(items):
            key = f"chk_{cat}_{idx}"
            checked = st.checkbox(item["item"], value=item["done"], key=key)
            item["done"] = checked

    with st.expander("➕ Add Custom Preparation Item"):
        c_cat = st.selectbox("Category", ["Hospital Bag (Mom)", "Hospital Bag (Baby)", "Nursery & Home Prep", "Partner Essentials"])
        c_item = st.text_input("Item Description")
        if st.button("Add to List"):
            if c_item.strip():
                st.session_state.checklist.append({"cat": c_cat, "item": c_item.strip(), "done": False})
                st.rerun()

# ----------------------------------------------------
# TAB 5: BABY NAMES GARDEN
# ----------------------------------------------------
with tab_names:
    st.subheader("✨ Baby Names Garden")
    st.caption("Collect and review names you and your partner cherish.")

    n1, n2, n3 = st.columns([2, 3, 2])
    with n1:
        n_name = st.text_input("Name")
    with n2:
        n_meaning = st.text_input("Meaning or Origin")
    with n3:
        n_pref = st.selectbox("Loved By", ["Both", "Mom", "Partner"])

    if st.button("Save Name"):
        if n_name.strip():
            st.session_state.baby_names.append({"name": n_name.strip(), "meaning": n_meaning.strip(), "liked_by": n_pref})
            st.success(f"Added {n_name} to your garden.")

    st.write("---")
    if st.session_state.baby_names:
        df_names = pd.DataFrame(st.session_state.baby_names)
        df_names.columns = ["Name", "Meaning / Notes", "Loved By"]
        st.dataframe(df_names, hide_index=True, use_container_width=True)
    else:
        st.info("Your naming list is empty. Add your favorite inspirations above.")

# ----------------------------------------------------
# TAB 6: PRENATAL MILESTONES ROADMAP
# ----------------------------------------------------
with tab_care:
    st.subheader("🩺 Standard Clinical Checkups Roadmap")
    st.caption("A helpful overview of routine clinical check-ins across the 40 weeks.")

    for appt in APPOINTMENTS_DATA:
        passed = tl["weeks"] >= appt["week"]
        status = "✨ Completed / Passed" if passed else f"Upcoming (~Week {appt['week']})"
        color = "#6E8271" if passed else "#A89B8F"

        st.markdown(f"""
        <div class='main-card' style='border-left: 5px solid {color};'>
            <div style='display:flex; justify-content:space-between;'>
                <span style='font-size:1.05rem; font-weight:700; color:#4E3E34;'>Week {appt['week']}: {appt['title']}</span>
                <span style='font-size:0.85rem; color:{color}; font-weight:600;'>{status}</span>
            </div>
            <p style='color:#756559; margin-top:6px; margin-bottom:0;'>{appt['focus']}</p>
        </div>
        """, unsafe_allow_html=True)
