import os
import streamlit as st
from streamlit_option_menu import option_menu
import base64


def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()


# =========================
# KONFIGURASI HALAMAN
# =========================
st.set_page_config(
    page_title="ꦲꦤꦕꦫꦏ Character App",
    page_icon="Apps/images/icon.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================
# DATA AKSARA JAWA
# =========================
aksara_jawa_map = {
    "ha": "ꦲ", "na": "ꦤ", "ca": "ꦕ", "ra": "ꦫ", "ka": "ꦏ",
    "da": "ꦢ", "ta": "ꦠ", "sa": "ꦱ", "wa": "ꦮ", "la": "ꦭ",
    "pa": "ꦥ", "dha": "ꦝ", "ja": "ꦗ", "ya": "ꦪ", "nya": "ꦚ",
    "ma": "ꦩ", "ga": "ꦒ", "ba": "ꦧ", "tha": "ꦛ", "nga": "ꦔ"
}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
AKSARA_JAWA_DIR = os.path.join(BASE_DIR, "Dataset")


# =========================
# FUNGSI AMBIL GAMBAR
# =========================
def get_sample_images(base_dir, char_key, max_images=6):
    folder_path = os.path.join(base_dir, char_key)

    if not os.path.exists(folder_path):
        return []

    valid_ext = (".png", ".jpg", ".jpeg", ".webp", ".bmp")
    files = [
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if f.lower().endswith(valid_ext)
    ]

    files.sort()
    return files[:max_images]


# =========================
# POPUP SAMPLE
# =========================
@st.dialog("Sampel Karakter Hanacaraka", width="large")
def show_sample_popup(title, char_idn, selected_char, base_dir):
    st.markdown(
        f"""
        <div class='popup-char-info'>
            <h2>{selected_char} — {char_idn}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    sample_images = get_sample_images(base_dir, char_idn, max_images=8)

    if sample_images:
        cols = st.columns(4)
        for i, img_path in enumerate(sample_images):
            with cols[i % 4]:
                st.image(img_path, use_container_width=True, caption=f"Contoh {i+1}")
    else:
        st.warning(
            f"Gambar sampel untuk karakter '{char_idn}' belum ditemukan di folder: {base_dir}/{char_idn}"
        )


# =========================
# TAMPILKAN KARAKTER
# =========================
def show_character_samples(title, data_map, base_dir, key_prefix):
    st.markdown(
        f"""
        <div class='section-card'>
            <h2>{title}</h2>
            <p>
                Klik salah satu karakter di bawah ini untuk melihat contoh gambar
                dari dataset Aksara Jawa yang digunakan dalam aplikasi.
            </p>
            <p>
                ꦑ꧀ꦭꦶꦏ꧀ ꦱꦭꦃ ꦱꦠꦸ ꦏꦫꦏ꧀ꦠꦺꦂ ꦢꦶ ꦧꦮꦃ ꦆꦤꦶ ꦈꦤ꧀ꦠꦸꦏ꧀ ꦩꦺꦭꦶꦲꦠ꧀ ꦕꦺꦴꦤ꧀ꦠꦺꦴꦃ ꦒꦩ꧀ꦧꦂ ꦢꦫꦶ 
                ꦢꦠꦱꦺꦠ꧀ ꦄꦏ꧀ꦱꦫ ꦙꦮ ꦪꦤ꧀ꦒ꧀ ꦢꦶꦒꦸꦤꦏꦤ꧀ ꦢꦭꦩ꧀ ꦄꦥ꧀ꦭꦶꦏꦱꦶ꧉​
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)

    items = list(data_map.items())
    cols_per_row = 5

    for i in range(0, len(items), cols_per_row):
        row_items = items[i:i + cols_per_row]
        cols = st.columns(cols_per_row)

        for j, (roman, jawa_char) in enumerate(row_items):
            label = f"{jawa_char}\n{roman}"
            if cols[j].button(label, key=f"{key_prefix}_{roman}", use_container_width=True):
                show_sample_popup(title, roman, jawa_char, base_dir)


# =========================
# HEADER UTAMA
# =========================
st.markdown(
    """
    <div class='navbar-header'>
        <div class='navbar-title'>ꦲꦤꦕꦫꦏ Character App</div>
        <div class='navbar-subtitle'>
            Aplikasi cerdas untuk mengenali dan memprediksi karakter Aksara Jawa menggunakan arsitektur ResNet50.
            <br>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================
# NAVBAR STICKY
# =========================
st.markdown("<div class='sticky-nav-wrap'>", unsafe_allow_html=True)
page = option_menu(
    menu_title=None,
    options=["Dashboard", "Data", "Predict", "Canvas"],
    icons=["house", "table",  "camera", "pencil"],
    default_index=1,
    orientation="horizontal",
    styles={
        "container": {
            "padding": "10px !important",
            "background-color": "transparent",
        },
        "icon": {
            "color": "#ffffff",
            "font-size": "20px",
        },
        "nav-link": {
            "font-size": "15px",
            "font-weight": "600",
            "text-align": "center",
            "margin": "0px 6px",
            "padding": "12px 18px",
            "border-radius": "14px",
            "color": "#FFFFFF",
        },
        "nav-link-selected": {
            "background": "linear-gradient(145deg,  #7a4a2b 35%, #9c6030 60%, #c9813a 90%)",
            "color": "white",
            "box-shadow": "0 10px 24px rgba(37, 99, 235, 0.20)",
        },
    },
)
st.markdown("<div class='nav-divider'></div></div>", unsafe_allow_html=True)

# =========================
# HALAMAN KONTEN
# =========================
if page == "Dashboard":
    st.switch_page("dashboard.py")

elif page == "Data":
    show_character_samples(
        "Data Karakter Hancaraka",
        aksara_jawa_map,
        AKSARA_JAWA_DIR,
        "aksara_jawa"
    )

elif page == "Predict":
    st.switch_page("pages/prediksi.py")

elif page == "Canvas":
    st.switch_page("pages/canvas.py")


# =========================
# CSS CUSTOM
# =========================
gunungan = get_base64_image("Apps/images/background.png")

st.markdown(f"""
<style>
.stApp {{
    background: linear-gradient(135deg, #fdf7ef 0%, #f8ead7 50%, #f3dfc4 100%);
}}

.stApp::before {{
    content: "";
    position: absolute;
    width: 100%;
    height: 100%;
    background-image: url("data:image/png;base64,{gunungan}");
    background-repeat: no-repeat;
    background-size: cover;
    background-position: center;
    opacity: 0.25;
}}
</style>
""", unsafe_allow_html=True)

st.markdown(
    """
    <style>
    section[data-testid="stSidebar"],
    [data-testid="stSidebar"],
    [data-testid="collapsedControl"] {
        display: none !important;
    }

    .main .block-container {
        padding-top: 0.7rem;
        padding-bottom: 2rem;
        padding-left: 1.2rem;
        padding-right: 1.2rem;
        max-width: 96% !important;
        position: relative;
        z-index: 1;
    }

    .element-container, .stMarkdown {
        width: 100% !important;
    }

    .navbar-header {
        background:
            linear-gradient(90deg, #5a3822 0%, #7a4a2b 25%, #9c6030 55%, #c9813a 78%, #e3a15d 100%);
        padding: 34px 34px 26px 34px;
        border-radius: 24px;
        box-shadow: 0 12px 30px rgba(92, 59, 30, 0.22);
        margin-bottom: 14px;
        width: 100%;
        border: 1px solid rgba(255, 236, 210, 0.35);
        position: relative;
        overflow: hidden;
        isolation: isolate;
    }

    .navbar-header::before {
        content: "ꦭꦼꦱ꧀ꦠꦫꦶꦏꦤ꧀ ꦧꦸꦢꦪ ꦤꦸꦱꦤ꧀ꦠꦫ";
        position: absolute;
        top: 10px;
        right: 24px;
        font-size: 1.7rem;
        color: rgba(255, 248, 220, 0.50);
        font-weight: 700;
        letter-spacing: 2px;
    }

    .navbar-title {
        color: #fffaf0;
        font-size: 3.7rem;
        font-weight: 900;
        margin-bottom: 8px;
        letter-spacing: 0.3px;
        line-height: 1.15;
        text-shadow: 0 2px 8px rgba(60, 35, 15, 0.15);
    }

    .navbar-subtitle {
        color: #fff4dc;
        font-size: 1.06rem;
        line-height: 1.8;
        max-width: 1100px;
    }

    .sticky-nav-wrap {
        position: sticky;
        top: 0;
        z-index: 9999;
        padding-top: 12px;
        padding-bottom: 12px;
        margin-bottom: 10px;
        width: 100%;
    }

    .nav-divider {
        width: 100%;
        height: 3px;
        background: linear-gradient(90deg, #6b4226, #b16b2f, #d8944b, #f0bb79);
        margin-top: 10px;
        margin-bottom: 18px;
        border-radius: 999px;
        box-shadow: 0 2px 8px rgba(145, 90, 38, 0.10);
    }

    .section-card {
        background: rgba(255, 252, 248, 0.96);
        border-radius: 24px;
        padding: 20px;
        box-shadow: 0 8px 24px rgba(92, 59, 30, 0.08);
        border: 1.5px solid #d6a06a;
        backdrop-filter: blur(2px);
    }

    .section-card h2 {
        margin-top: 0;
        color: #5b3a29;
        font-size: 2rem;
        font-weight: 800;
    }

    .section-card p {
        color: #4b3a2f;
        font-size: 1.15rem;
        line-height: 1.9;
        margin-bottom: 0;
    }

    .feature-box {
        background: linear-gradient(180deg, #fffaf5 0%, #fdf0e3 100%);
        border: 1px solid #e7c9a9;
        border-radius: 18px;
        padding: 20px;
        min-height: 150px;
        height: 100%;
        box-shadow: 0 6px 18px rgba(201, 122, 43, 0.08);
    }

    .feature-box h4 {
        margin-top: 0;
        margin-bottom: 10px;
        color: #7c4a21;
        font-size: 1.12rem;
    }

    .feature-box p {
        margin-bottom: 0;
        color: #5f4b3a;
        font-size: 0.98rem;
        line-height: 1.7;
    }

    /* TOMBOL KARAKTER */
    div.stButton > button {
        background: #ffffff !important;
        color: #7c4a21 !important;
        border: 2px solid #c9813a !important;
        border-radius: 16px !important;
        font-size: 1.2rem !important;
        font-weight: 800 !important;
        min-height: 78px !important;
        white-space: pre-line !important;
        line-height: 1.45 !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 10px rgba(201, 129, 58, 0.08) !important;
    }

    div.stButton > button:hover {
        background: #fff4e8 !important;
        color: #5b3a29 !important;
        border-color: #9c6030 !important;
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(156, 96, 48, 0.16) !important;
    }

    div.stButton > button:focus:not(:active) {
        border-color: #7a4a2b !important;
        color: #7a4a2b !important;
        box-shadow: 0 0 0 0.15rem rgba(201, 129, 58, 0.15) !important;
    }

    /* DIALOG */
    div[data-testid="stDialog"] h2 {
        color: #7a4a2b !important;
        font-weight: 900 !important;
    }

    div[data-testid="stDialog"] button {
        font-size: 50px;
        color: #ffffff !important;
        font-weight: 900 !important;
    }

    div[data-testid="stDialog"] button:hover {
        background: #7a4a2b !important;
        border-radius: 8px !important;
        color: #ffffff !important;
    }

    .popup-char-info {
        background: #ffffff;
        border: 2px solid #c9813a;
        border-radius: 18px;
        padding: 5px 20px;
        margin-bottom: 18px;
        box-shadow: 0 6px 16px rgba(201, 129, 58, 0.10);
    }

    .popup-char-info h2 {
        margin: 0 0 8px 0;
        color: #7a4a2b;
        font-size: 3rem;
        font-weight: 900;
        line-height: 1.2;
    }

    .popup-char-info p {
        margin: 0;
        color: #ffffff;
        font-size: 1.08rem;
        font-weight: 700;
        line-height: 1.6;
    }

    [data-testid="stImage"] img {
        border-radius: 14px !important;
        background: #ffffff;
        padding: 6px;
        border: 2px solid #d6a06a;
    }

    [data-testid="stCaptionContainer"] {
        text-align: center;
        color: #ffffff !important;
        font-weight: 700;
        font-size: 0.95rem;
    }

    .stAlert, .stWarning, .stInfo {
        border-radius: 16px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)
