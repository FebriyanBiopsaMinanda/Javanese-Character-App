import os
import random
import numpy as np
import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import tensorflow as tf
from tensorflow.keras.applications.resnet50 import preprocess_input
import base64
from pathlib import Path

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
# KONFIGURASI FILE
# =========================
PATH_BASE = Path(__file__).resolve().parent.parent.parent
MODEL_PATH =  PATH_BASE / "resnet50_aksara_jawa.h5"
CLASS_NAMES_PATH =  PATH_BASE / "class_names.npy"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATASET_DIR = os.path.join(BASE_DIR, "Dataset")
IMG_SIZE = (224, 224)

# =========================
# MAPPING AKSARA
# =========================
aksara_map = {
    "ha": "ꦲ", "na": "ꦤ", "ca": "ꦕ", "ra": "ꦫ", "ka": "ꦏ",
    "da": "ꦢ", "ta": "ꦠ", "sa": "ꦱ", "wa": "ꦮ", "la": "ꦭ",
    "pa": "ꦥ", "dha": "ꦝ", "ja": "ꦗ", "ya": "ꦪ", "nya": "ꦚ",
    "ma": "ꦩ", "ga": "ꦒ", "ba": "ꦧ", "tha": "ꦛ", "nga": "ꦔ"
}

# =========================
# LOAD MODEL
# =========================
@st.cache_resource
def load_resnet_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model tidak ditemukan: {MODEL_PATH}")

    return tf.keras.models.load_model(MODEL_PATH)


# =========================
# LOAD CLASS NAMES
# =========================
@st.cache_data
def load_class_names():
    if not os.path.exists(CLASS_NAMES_PATH):
        raise FileNotFoundError(f"File class_names tidak ditemukan: {CLASS_NAMES_PATH}")

    class_names = np.load(CLASS_NAMES_PATH, allow_pickle=True)

    if len(class_names) == 0:
        raise ValueError("class_names.npy kosong.")

    return class_names


# =========================
# PREPROCESS GAMBAR
# =========================
def preprocess_image(uploaded_image):
    image = Image.open(uploaded_image).convert("RGB")
    preview = image.copy()

    image = image.resize(IMG_SIZE)
    image_array = tf.keras.utils.img_to_array(image)
    image_array = np.expand_dims(image_array, axis=0)
    image_array = preprocess_input(image_array)

    return preview, image_array


# =========================
# AMBIL CONTOH DATASET
# =========================
def get_sample_images(predicted_class, max_samples=5):
    folder_path = os.path.join(DATASET_DIR, str(predicted_class))

    if not os.path.exists(folder_path):
        return []

    images = [
        os.path.join(folder_path, file)
        for file in os.listdir(folder_path)
        if file.lower().endswith((".png", ".jpg", ".jpeg"))
    ]

    if len(images) == 0:
        return []

    return random.sample(images, min(max_samples, len(images)))


# =========================
# POPUP HASIL PREDIKSI
# =========================
@st.dialog("Hasil Prediksi Gambar", width="large")
def show_prediction_popup(uploaded_file, predicted_class, confidence):
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        image = Image.open(uploaded_file)
        st.image(image, use_container_width=True)
    
    aksara = aksara_map.get(str(predicted_class).lower(), "-")

    with col2:
        st.markdown(
            f"""
            <div class='popup-result-box'>
                <h3>Hasil (ꦲꦱꦶꦭ꧀) : {predicted_class}</h3>
                <p>Karakter (ꦏꦫꦏ꧀ꦠꦺꦂ) : <b>{aksara}</b></p>
                <p>Persentase (ꦥꦺꦂꦱꦺꦤ꧀ꦠꦱꦺ) : <b>{confidence:.2f}%</b></p>
            </div>
            """,
            unsafe_allow_html=True
        )

        sample_images = get_sample_images(predicted_class)

        if sample_images:
            st.markdown("<h2 style='color:#7a4a2b;'>Contoh Sample (ꦱꦩ꧀ꦥ꧀ꦭꦺ)</h2>", unsafe_allow_html=True)

            cols = st.columns(5)

            for i, img_path in enumerate(sample_images):
                with cols[i]:
                    st.image(img_path, use_container_width=True)
        else:
            st.info("""Contoh gambar dataset untuk kelas ini tidak ditemukan.
                    \nꦕꦺꦴꦤ꧀ꦠꦺꦴꦃ ꦒꦩ꧀ꦧꦂ ꦢꦠꦱꦺꦠ꧀ ꦲꦸꦤ꧀ꦠꦸꦏ꧀ ꦏꦺꦭꦱ꧀ ꦲꦶꦤꦶ ꦠꦶꦢꦏ꧀ ꦢꦶꦠꦺꦩꦸꦏꦤ꧀꧉​""")


# =========================
# HEADER
# =========================
st.markdown(
    """
    <div class='navbar-header'>
        <div class='navbar-title'>ꦲꦤꦕꦫꦏ Character App</div>
        <div class='navbar-subtitle'>
            Aplikasi cerdas untuk mengenali dan memprediksi karakter Aksara Jawa menggunakan arsitektur ResNet50.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================
# NAVBAR
# =========================
st.markdown("<div class='sticky-nav-wrap'>", unsafe_allow_html=True)

page = option_menu(
    menu_title=None,
    options=["Dashboard", "Data", "Predict", "Canvas"],
    icons=["house", "table", "camera", "pencil"],
    default_index=2,
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
            "background": "linear-gradient(145deg, #7a4a2b 35%, #9c6030 60%, #c9813a 90%)",
            "color": "white",
        },
    },
)

st.markdown("<div class='nav-divider'></div></div>", unsafe_allow_html=True)


# =========================
# CEK MODEL
# =========================
model = None
class_names = None
model_ready = False

try:
    model = load_resnet_model()
    class_names = load_class_names()

    output_model = model.output_shape[-1]

    if output_model != len(class_names):
        st.error(
            f"Jumlah output model ({output_model}) tidak sama dengan jumlah class_names ({len(class_names)})."
        )
    else:
        model_ready = True

except Exception as e:
    st.warning(f"Model belum bisa digunakan: {e}")


# =========================
# HALAMAN KONTEN
# =========================
if page == "Dashboard":
    st.switch_page(".../dashboard.py")

elif page == "Data":
    st.switch_page("pages/data.py")

elif page == "Predict":
    left_col, right_col = st.columns([1.1, 1], gap="large")

    with left_col:
        st.markdown(
            """
            <div class='predict-card'>
                <h3>Upload Gambar ꦲꦤꦕꦫꦏ</h3>
                <p>
                    Pilih satu gambar karakter Aksara Jawa dalam format PNG, JPG, atau JPEG.
                    Setelah gambar berhasil diupload, klik tombol prediksi untuk melihat hasil klasifikasi.
                </p>
                <p>
                    ꦥꦶꦭꦶꦃ ꦱꦠꦸ ꦒꦩ꧀ꦧꦂ ꦏꦫꦏ꧀ꦠꦺꦂ ꦄꦏ꧀ꦱꦫ ꦗꦮ ꦢꦭꦩ꧀ ꦥ꦳ꦺꦴꦂꦩꦠ꧀ ꦥ꧀ꦤ꧀ꦒ꧀꧈​ ꦗ꧀ꦥ꧀ꦒ꧀꧈​ ꦲꦠꦻꦴ ꦗ꧀ꦥꦌꦒ꧀꧉​ ꦱꦺꦠꦺꦭꦃ 
                    ꦒꦩ꧀ꦧꦂ ꦧꦺꦂꦲꦱꦶꦭ꧀ ꦢꦶꦪꦸꦥ꧀ꦭꦺꦴꦮꦢ꧀꧈​ ꦏ꧀ꦭꦶꦏ꧀ ꦠꦺꦴꦩ꧀ꦧꦺꦴꦭ꧀ ꦥ꧀ꦫꦺꦢꦶꦏ꧀ꦱꦶ ꦲꦸꦤ꧀ꦠꦸꦏ꧀ ꦩꦺꦭꦶꦲꦠ꧀ ꦲꦱꦶꦭ꧀ ꦏ꧀ꦭꦱꦶꦥ꦳ꦶꦏꦱꦶ꧉​
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with right_col:
        uploaded_file = st.file_uploader(
            "Upload gambar",
            type=["png", "jpg", "jpeg"],
            label_visibility="collapsed"
        )

        if uploaded_file is None:
            st.info("""Silakan upload satu gambar Aksara Jawa terlebih dahulu.
                    \nꦱꦶꦭꦏꦤ꧀ ꦲꦸꦥ꧀ꦭꦺꦴꦮꦢ꧀ ꦱꦠꦸ ꦒꦩ꧀ꦧꦂ ꦄꦏ꧀ꦱꦫ ꦗꦮ ꦠꦺꦂꦭꦺꦧꦶꦃ ꦢꦲꦸꦭꦸ꧉​""")

        else:
            st.success("""Gambar berhasil diupload. Klik tombol prediksi.
                       \nꦒꦩ꧀ꦧꦂ ꦧꦺꦂꦲꦱꦶꦭ꧀ ꦢꦶꦪꦸꦥ꧀ꦭꦺꦴꦮꦢ꧀꧉​ ꦏ꧀ꦭꦶꦏ꧀ ꦠꦺꦴꦩ꧀ꦧꦺꦴꦭ꧀ ꦥ꧀ꦫꦺꦢꦶꦏ꧀ꦱꦶ꧉​""")

            col1, col2, col3= st.columns(3)
            
            with col3:
                if st.button("Prediksi (ꦥ꧀ꦫꦺꦢꦶꦏ꧀ꦱꦶ)", use_container_width=True):
                    if not model_ready:
                        st.error("""Model belum siap digunakan. Periksa file model dan class_names.npy.
                                \nꦩꦺꦴꦢꦺꦭ꧀ ꦧꦺꦭꦸꦩ꧀ ꦱꦶꦪꦥ꧀ ꦢꦶꦒꦸꦤꦏꦤ꧀꧉​ ꦥꦺꦫꦶꦏ꧀ꦱ ꦥ꦳ꦶꦭꦺ ꦩꦺꦴꦢꦺꦭ꧀ ꦢꦤ꧀ ꦕ꧀ꦭꦱ꧀ꦱ꧀_ꦤꦩꦺꦱ꧀꧉​ꦤ꧀ꦥ꧀ꦪ꧀꧉​""")
                    else:
                        _, image_input = preprocess_image(uploaded_file)

                        prediction = model.predict(image_input, verbose=0)[0]

                        pred_index = int(np.argmax(prediction))
                        predicted_class = class_names[pred_index]
                        confidence = float(np.max(prediction) * 100)

                        show_prediction_popup(
                            uploaded_file,
                            predicted_class,
                            confidence
                        )

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
    }

    .navbar-header {
        background: linear-gradient(90deg, #5a3822 0%, #7a4a2b 25%, #9c6030 55%, #c9813a 78%, #e3a15d 100%);
        padding: 34px 34px 26px 34px;
        border-radius: 24px;
        box-shadow: 0 12px 30px rgba(92, 59, 30, 0.22);
        margin-bottom: 14px;
        width: 100%;
    }

    .navbar-title {
        color: #fffaf0;
        font-size: 3.7rem;
        font-weight: 900;
        margin-bottom: 8px;
        letter-spacing: 0.3px;
        line-height: 1.15;
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
    }

    .predict-card {
        background: rgba(255, 252, 248, 0.96);
        border: 1.5px solid #d6a06a;
        border-radius: 24px;
        padding: 24px;
        box-shadow: 0 8px 24px rgba(92, 59, 30, 0.08);
    }

    .predict-card h3 {
        margin-top: 0;
        color: #5b3a29;
        font-size: 2rem;
        font-weight: 800;
    }

    .predict-card p {
        color: #4b3a2f;
        font-size: 1.1rem;
        line-height: 1.9;
    }

    div[data-testid="stDialog"] h2 {
        font-size: 2.2rem !important;
        text-align: center !important;
        font-weight: 900 !important;
        color: #ffffff !important;
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
    
    div[data-testid="stFileUploader"] {
        background: #ffffff !important;
        border: 1.5px solid #d6a06a !important;
        border-radius: 18px !important;
        padding: 14px !important;
        box-shadow: 0 8px 20px rgba(201, 129, 58, 0.08) !important;
    }

    .stButton > button {
        background: linear-gradient(145deg, #7a4a2b 35%, #9c6030 60%, #c9813a 90%) !important;
        color: white !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 0.9rem 1rem !important;
        font-size: 1.1rem !important;
        font-weight: 800 !important;
        box-shadow: 0 8px 18px rgba(92, 59, 30, 0.18) !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 22px rgba(92, 59, 30, 0.26) !important;
    }

    .popup-result-box {
        background: #ffffff;
        border: 2px solid #c9813a;
        border-radius: 20px;
        padding: 20px 22px;
        box-shadow: 0 8px 20px rgba(201, 129, 58, 0.10);
    }

    .popup-result-box h3 {
        margin: 0 0 12px 0;
        color: #7a4a2b;
        font-size: 1.8rem;
        font-weight: 900;
    }

    .popup-result-box p {
        margin: 6px 0;
        color: #5b3a29;
        font-size: 1.08rem;
        font-weight: 600;
        line-height: 1.7;
    }

    [data-testid="stImage"] img {
        border-radius: 16px !important;
        border: 2px solid #d6a06a;
        background: #ffffff;
        padding: 6px;
    }

    .stInfo,
    .stAlert,
    .stWarning,
    .stSuccess {
        border-radius: 16px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)
