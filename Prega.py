import streamlit as st
import pandas as pd
import random
from datetime import datetime, date, timedelta

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
        height: 100%;
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
    .name-card {
        background: #FFFBF7;
        border-left: 4px solid #D8C7B8;
        padding: 15px;
        margin-bottom: 10px;
        border-radius: 8px;
    }
</style>
"""
st.markdown(CALM_CSS, unsafe_allow_html=True)

# ==========================================
# 2. EMBEDDED KNOWLEDGE DATA
# ==========================================

# Overview Benchmarks
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

# Detailed Fetal Development milestones (Anatomy & Sensory)
FETAL_DEVELOPMENT = {
    "Weeks 4-6": {
        "title": "The Foundation",
        "structure": "The embryo develops three layers (ectoderm, mesoderm, endoderm) that will form all organs and tissues. The neural tube (future brain and spinal cord) closes. Tiny arm and leg buds begin to appear.",
        "senses": "The tiny heart tube begins to pulse. Structures that will eventually become the eyes, ears, and mouth begin to take form."
    },
    "Weeks 7-10": {
        "title": "Limbs & Major Organs",
        "structure": "All major organs begin developing. Webbed hands and feet emerge and slowly lose their webbing to become distinct fingers and toes. Elbows can now bend. Cartilage starts transitioning to bone.",
        "senses": "The head becomes rounder and the face takes a more human profile. Taste buds begin forming, and the initial buds for future teeth appear in the gums."
    },
    "Weeks 11-14": {
        "title": "Reflexes & Growth",
        "structure": "The fetus has a fully developed umbilical cord. Kidneys start producing urine, and the liver produces bile. Vocal cords are forming. The external genitals develop fully.",
        "senses": "The fetus starts practicing movements like opening/closing fists and the mouth. It begins swallowing amniotic fluid and can even yawn or stretch."
    },
    "Weeks 15-19": {
        "title": "Movement & Senses",
        "structure": "A soft, fine hair called 'lanugo' covers the body to keep the baby warm. The skeleton continues hardening. A white protective coating (vernix) covers the skin.",
        "senses": "Ears move to their final position and become sensitive enough to hear your voice and heartbeat. Eyes remain closed but can react to bright light. Quickening (feeling the baby move) typically begins."
    },
    "Weeks 20-24": {
        "title": "Halfway & Viability",
        "structure": "Bone marrow begins producing blood cells. The lungs start developing 'surfactant', a substance that keeps air sacs open. Fingerprints and footprints are permanently formed.",
        "senses": "The area of the brain responsible for the five senses rapidly develops. The baby establishes distinct sleep-wake cycles and responds to external sounds with a change in pulse or movement."
    },
    "Weeks 25-29": {
        "title": "Opening Eyes",
        "structure": "Fat continues to accumulate under the skin, smoothing out wrinkles. The brain undergoes massive growth, developing deep ridges and folds.",
        "senses": "Eyelids, which have been fused shut, blink open. The baby can see light and shadows. Lung practice breathing motions become more rhythmic."
    },
    "Weeks 30-35": {
        "title": "Gaining Weight & Strength",
        "structure": "Lanugo (fine hair) begins to fall off. The bones are fully formed but remain somewhat pliable. The baby gains roughly half a pound a week.",
        "senses": "Pupils can dilate and constrict in response to light. Hearing is fully mature. Kicks become strong and forceful."
    },
    "Weeks 36-40": {
        "title": "Full Term & Preparation",
        "structure": "Lungs are mature and ready for the first breath. The baby often 'drops' lower into the mother's pelvis. The skull bones remain unfused to allow passage through the birth canal.",
        "senses": "The digestive system contains meconium (first stool). The baby is fully capable of sensory processing outside the womb and is ready to be born!"
    }
}

# Indian Baby Names Database
INDIAN_NAMES = [
    {"name": "Aarav", "gender": "Boy", "meaning": "Peaceful, calm", "origin": "Modern Sanskrit"},
    {"name": "Advik", "gender": "Boy", "meaning": "Unique, one of a kind", "origin": "Modern Hindu"},
    {"name": "Vivaan", "gender": "Boy", "meaning": "Full of life, rays of the morning sun", "origin": "Modern Sanskrit"},
    {"name": "Reyansh", "gender": "Boy", "meaning": "Ray of light, part of Lord Vishnu", "origin": "Spiritual"},
    {"name": "Shaurya", "gender": "Boy", "meaning": "Bravery, heroism", "origin": "Traditional"},
    {"name": "Ishaan", "gender": "Boy", "meaning": "Sun, Lord Shiva", "origin": "Spiritual"},
    {"name": "Atharv", "gender": "Boy", "meaning": "Sacred Vedic name, Lord Ganesha", "origin": "Traditional"},
    {"name": "Kiaan", "gender": "Boy", "meaning": "Grace of God, ancient", "origin": "Modern Hindu"},
    {"name": "Ojas", "gender": "Boy", "meaning": "Energy, brilliance, vitality", "origin": "Traditional"},
    {"name": "Vedant", "gender": "Boy", "meaning": "Knowledge of the Vedas", "origin": "Spiritual"},
    
    {"name": "Aadhya", "gender": "Girl", "meaning": "First power, Goddess Durga", "origin": "Spiritual"},
    {"name": "Anaya", "gender": "Girl", "meaning": "Caring, protection, God's answer", "origin": "Modern Hindu"},
    {"name": "Myra", "gender": "Girl", "meaning": "Beloved, divine, sweet", "origin": "Modern"},
    {"name": "Kiara", "gender": "Girl", "meaning": "Bright, clear, dark-haired", "origin": "Modern"},
    {"name": "Saanvi", "gender": "Girl", "meaning": "Goddess Lakshmi, one who is followed", "origin": "Spiritual"},
    {"name": "Avni", "gender": "Girl", "meaning": "The Earth", "origin": "Nature-inspired"},
    {"name": "Veda", "gender": "Girl", "meaning": "Sacred knowledge, wisdom", "origin": "Traditional"},
    {"name": "Ira", "gender": "Girl", "meaning": "Goddess Saraswati, Earth", "origin": "Spiritual"},
    {"name": "Kavya", "gender": "Girl", "meaning": "Poetry in motion", "origin": "Traditional"},
    {"name": "Prisha", "gender": "Girl", "meaning": "God's gift, beloved", "origin": "Traditional"}
]

DEFAULT_CHECKLIST = [
    {"cat": "Hospital Bag (Mom)", "item": "Warm comfortable non-slip socks & slippers", "done": False},
    {"cat": "Hospital Bag (Mom)", "item": "Comfortable nursing bras & soft pads", "done": False},
    {"cat": "Hospital Bag (Baby)", "item": "Installed rear-facing infant car seat", "done": False},
    {"cat": "Hospital Bag (Baby)", "item": "2-3 soft newborn onesies & swaddle blankets", "done": False},
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
    st.session_state.journal_entries = []
if "kick_sessions" not in st.session_state:
    st.session_state.kick_sessions = []
if "checklist" not in st.session_state:
    st.session_state.checklist = DEFAULT_CHECKLIST.copy()
if "baby_names" not in st.session_state:
    st.session_state.baby_names = []

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
        "lmp": lmp_date, "due": due_date, "weeks": weeks, "days": days_rem,
        "days_pregnant": days_pregnant, "days_left": days_to_go,
        "progress": progress_pct, "trimester": trimester
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

    calc_method = st.selectbox("Calculate journey based on:", ["Due Date", "First Day of Last Period (LMP)", "Conception Date"], index=0)
    st.session_state.calc_method = calc_method
    picked_date = st.date_input(f"Select your {calc_method.lower()}:", value=st.session_state.conception_or_due)
    st.session_state.conception_or_due = picked_date

    tl = calculate_timeline(picked_date, calc_method)

    st.write("---")
    st.markdown("### 🕊️ Today's Affirmation")
    affirmations = [
        "My body knows exactly how to nurture and shelter this precious life.",
        "I welcome each feeling and change with gentle grace and patience.",
        "Peace flows through me, giving peaceful serenity to my little one.",
        "Today, I slow down, breathe deeply, and trust the innate wisdom of nature."
    ]
    st.info(affirmations[tl["weeks"] % len(affirmations)])

# ==========================================
# 6. MAIN CONTENT TABS
# ==========================================
tabs = st.tabs([
    "🌿 Overview", "🌱 Fetal Dev", "📖 Journal", "👣 Kicks", 
    "🎒 Nesting", "✨ Baby Names", "🩺 Checkups"
])

# ----------------------------------------------------
# TAB 1: JOURNEY OVERVIEW
# ----------------------------------------------------
with tabs[0]:
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

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(f"<div class='metric-bubble'><div class='metric-val'>{tl['days_left']}</div><div class='metric-label'>Days Left</div></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='metric-bubble'><div class='metric-val'>{fruit['size']}</div><div class='metric-label'>Comparable Size</div></div>", unsafe_allow_html=True)
    with c3: st.markdown(f"<div class='metric-bubble'><div class='metric-val'>{fruit['len']}</div><div class='metric-label'>Approx. Length</div></div>", unsafe_allow_html=True)
    with c4: st.markdown(f"<div class='metric-bubble'><div class='metric-val'>{fruit['wt']}</div><div class='metric-label'>Approx. Weight</div></div>", unsafe_allow_html=True)

    st.write("<br>", unsafe_allow_html=True)
    st.progress(tl["progress"])
    st.caption(f"{int(tl['progress']*100)}% completed — Every day is an extraordinary chapter of growth.")

# ----------------------------------------------------
# TAB 2: FETAL DEVELOPMENT (NEW)
# ----------------------------------------------------
with tabs[1]:
    st.subheader("🌱 Week-by-Week Fetal Development")
    st.caption("Explore how your baby's anatomy, organs, and senses miraculously unfold over 40 weeks.")
    
    selected_phase = st.select_slider(
        "Select a timeline phase to view details:",
        options=list(FETAL_DEVELOPMENT.keys()),
        value=list(FETAL_DEVELOPMENT.keys())[min(len(FETAL_DEVELOPMENT)-1, tl["weeks"] // 5)]
    )
    
    dev_data = FETAL_DEVELOPMENT[selected_phase]
    
    st.markdown(f"""
    <div class='main-card'>
        <h3 style='color:#6B584D; margin-top:0;'>{selected_phase}: {dev_data['title']}</h3>
        <hr style='border:1px solid #F0EAE1; margin-bottom:15px;'>
        <h5 style='color:#8C6D62;'>🧬 Structure & Organs</h5>
        <p style='color:#5D4A3E; line-height:1.6;'>{dev_data['structure']}</p>
        <br>
        <h5 style='color:#8C6D62;'>👂 Senses & Reflexes</h5>
        <p style='color:#5D4A3E; line-height:1.6;'>{dev_data['senses']}</p>
    </div>
    """, unsafe_allow_html=True)

# ----------------------------------------------------
# TAB 3: MEMORY JOURNAL
# ----------------------------------------------------
with tabs[2]:
    st.subheader("📖 Keepsake Journal")
    with st.expander("✍️ Pen a New Memory", expanded=False):
        j1, j2 = st.columns([1, 2])
        with j1:
            e_date = st.date_input("Date", date.today())
            e_mood = st.selectbox("Mood", ["Serene 🌿", "Grateful 🌸", "Tired ☁️", "Joyful ☀️"])
        with j2:
            e_notes = st.text_area("Your Reflections", height=100)
        if st.button("Save Memory"):
            st.session_state.journal_entries.insert(0, {"date": str(e_date), "week": tl["weeks"], "mood": e_mood, "notes": e_notes})
            st.success("Memory archived.")
            
    for item in st.session_state.journal_entries:
        st.markdown(f"<div class='main-card'><b>Week {item['week']} ({item['date']})</b> — {item['mood']}<br><br><i>\"{item['notes']}\"</i></div>", unsafe_allow_html=True)

# ----------------------------------------------------
# TAB 4: KICK COUNTER
# ----------------------------------------------------
with tabs[3]:
    st.subheader("👣 Kick Counter")
    c_mins = st.number_input("Minutes taken for 10 movements:", 1, 120, 20)
    c_notes = st.text_input("Context (e.g., after drinking juice)")
    if st.button("Log Kicks"):
        st.session_state.kick_sessions.insert(0, {"time": datetime.now().strftime("%Y-%m-%d %H:%M"), "mins": c_mins, "notes": c_notes})
    if st.session_state.kick_sessions:
        st.dataframe(pd.DataFrame(st.session_state.kick_sessions), use_container_width=True)

# ----------------------------------------------------
# TAB 5: NESTING CHECKLIST
# ----------------------------------------------------
with tabs[4]:
    st.subheader("🎒 Nesting & Hospital Prep")
    categories = list(set(i["cat"] for i in st.session_state.checklist))
    for cat in sorted(categories):
        st.markdown(f"##### {cat}")
        for idx, item in enumerate([x for x in st.session_state.checklist if x["cat"] == cat]):
            checked = st.checkbox(item["item"], value=item["done"], key=f"chk_{cat}_{idx}")
            item["done"] = checked

# ----------------------------------------------------
# TAB 6: INDIAN BABY NAMES (NEW)
# ----------------------------------------------------
with tabs[5]:
    st.subheader("✨ Indian Baby Name Generator")
    st.caption("Discover meaningful modern and traditional names. Save your favorites to your garden.")
    
    col_n1, col_n2, col_n3 = st.columns([1, 1, 1])
    with col_n1:
        gender_filter = st.selectbox("Gender", ["All", "Boy", "Girl"])
    with col_n2:
        letter_filter = st.selectbox("Starting Letter", ["Any"] + [chr(i) for i in range(65, 91)])
    with col_n3:
        st.write("<br>", unsafe_allow_html=True)
        if st.button("Surprise Me!", use_container_width=True):
            filtered_names = INDIAN_NAMES
            if gender_filter != "All":
                filtered_names = [n for n in filtered_names if n["gender"] == gender_filter]
            if letter_filter != "Any":
                filtered_names = [n for n in filtered_names if n["name"].startswith(letter_filter)]
            
            if filtered_names:
                st.session_state.suggested_name = random.choice(filtered_names)
            else:
                st.session_state.suggested_name = {"name": "None found", "meaning": "Try different filters", "gender": "-", "origin": "-"}

    # Display suggestion
    if "suggested_name" in st.session_state and st.session_state.suggested_name["name"] != "None found":
        n = st.session_state.suggested_name
        st.markdown(f"""
        <div class='metric-bubble' style='margin-bottom: 20px; background-color: #FDF9F1;'>
            <h2 style='color:#5C4B41; margin-bottom:5px;'>{n['name']}</h2>
            <p style='color:#7D746B; margin:0;'><b>Meaning:</b> {n['meaning']} &nbsp; | &nbsp; <b>Style:</b> {n['origin']} ({n['gender']})</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"🤍 Save '{n['name']}' to Garden"):
            if not any(saved['name'] == n['name'] for saved in st.session_state.baby_names):
                st.session_state.baby_names.append(n)
                st.success("Saved!")

    st.write("---")
    st.markdown("#### Your Name Garden")
    if st.session_state.baby_names:
        for saved in st.session_state.baby_names:
            st.markdown(f"<div class='name-card'><b>{saved['name']}</b> ({saved['gender']}) — <i>{saved['meaning']}</i></div>", unsafe_allow_html=True)
    else:
        st.info("Your garden is empty. Generate and save names above!")

# ----------------------------------------------------
# TAB 7: PRENATAL MILESTONES
# ----------------------------------------------------
with tabs[6]:
    st.subheader("🩺 Checkups Roadmap")
    for appt in APPOINTMENTS_DATA:
        passed = tl["weeks"] >= appt["week"]
        status, color = ("Completed", "#6E8271") if passed else (f"Upcoming (~Wk {appt['week']})", "#A89B8F")
        st.markdown(f"""
        <div class='main-card' style='border-left: 5px solid {color};'>
            <div style='display:flex; justify-content:space-between;'>
                <b>Week {appt['week']}: {appt['title']}</b> <span style='color:{color}; font-size:0.85em;'>{status}</span>
            </div>
            <p style='color:#756559; margin-top:5px;'>{appt['focus']}</p>
        </div>
        """, unsafe_allow_html=True)
