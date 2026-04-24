import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
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
    default_index=0,
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
    st.markdown(
        """
        <div class='section-card'>
            <h2>ꦱꦸꦒꦼꦁ ꦫꦮꦸꦃ</h2>
            <br>
            <p>
                Aksara Jawa merupakan salah satu warisan budaya nusantara yang memiliki nilai historis,
                filosofis, dan estetika yang tinggi. Dengan adanya aplikasi ini, diharapkan proses pembelajaran,
                pelestarian, dan pengenalan aksara tradisional Jawa dapat dilakukan secara lebih modern,
                interaktif, dan mudah diakses.
            </p>
            <p>
                ꦄꦏ꧀ꦱꦫ ꦙꦮ ꦩꦺꦫꦸꦥꦏꦤ꧀ ꦱꦭꦃ ꦱꦠꦸ ꦮꦫꦶꦱꦤ꧀ ꦧꦸꦢꦪ ꦤꦸꦱꦤ꧀ꦠꦫ ꦪꦤ꧀ꦒ꧀ ꦩꦺꦩꦶꦭꦶꦏꦶ ꦤꦶꦭꦻ ꦲꦶꦱ꧀ꦠꦺꦴꦫꦶꦱ꧀꧈​ 
                ꦥ꦳ꦶꦭꦺꦴꦱꦺꦴꦥ꦳ꦶꦱ꧀꧈​ ꦢꦤ꧀ ꦌꦱ꧀ꦠꦺꦠꦶꦏ ꦪꦤ꧀ꦒ꧀ ꦠꦶꦤ꧀ꦒ꧀ꦒꦶ꧉​ ꦣꦺꦤ꧀ꦒꦤ꧀ ꦄꦢꦤ꧀ꦪ ꦄꦥ꧀ꦭꦶꦏꦱꦶ ꦆꦤꦶ꧈​ ꦢꦶꦲꦫꦥ꧀ꦏꦤ꧀ ꦥ꧀ꦫꦺꦴꦱꦺꦱ꧀ ꦥꦺꦩ꧀ꦧꦺꦭꦗꦫꦤ꧀꧈​ ꦥꦺꦭꦺꦱ꧀ꦠꦫꦶꦪꦤ꧀꧈​ 
                ꦢꦤ꧀ ꦥꦺꦤ꧀ꦒꦺꦤꦭꦤ꧀ ꦄꦏ꧀ꦱꦫ ꦠ꧀ꦫꦢꦶꦱꦶꦪꦺꦴꦤꦭ꧀ ꦙꦮ ꦢꦥꦠ꧀ ꦢꦶꦭꦏꦸꦏꦤ꧀ ꦱꦺꦕꦫ ꦭꦺꦧꦶꦃ ꦩꦺꦴꦢꦺꦂꦤ꧀꧈​ ꦆꦤ꧀ꦠꦺꦫꦏ꧀ꦠꦶꦥ꦳꧀꧈​ ꦢꦤ꧀ ꦩꦸꦢꦃ ꦢꦶꦪꦏ꧀ꦱꦺꦱ꧀꧉​
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    
    # =========================
    # RINGKASAN DATASET
    # =========================
    col1, col2, col3, col4 = st.columns(4)

    with col2:
        components.html(
            """
            <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap" rel="stylesheet">

            <div class='feature-box summary-box'>
                <h4>Total Gambar</h4>
                <div class='summary-number' id='counter1'>0</div>
            </div>
            <style>
                body {
                    font-family: 'Poppins', sans-serif;
                    margin: 0;
                    font-weight: 700;
                }
                .summary-box {
                    background: linear-gradient(180deg, #fffaf5 0%, #fdf0e3 100%);
                    border: 1.5px solid #d6a06a;
                    border-radius: 22px;
                    padding: 28px 20px;
                    text-align: center;
                    box-shadow: 0 6px 18px rgba(201, 122, 43, 0.08);
                }

                .summary-box h4 {
                    margin: 0 0 10px 0;
                    color: #7c4a21;
                    font-size: 1.1rem;
                    font-weight: 700;
                }

                .summary-number {
                    font-size: 2.4rem;
                    font-weight: 900;
                    color: #9c6030;
                    line-height: 1.2;
                }
            </style>

            <script>
                let current1 = 0;
                const target1 = 10000;
                const duration1 = 1000;
                const stepTime1 = 20;
                const increment1 = Math.ceil(target1 / (duration1 / stepTime1));

                const counter1 = document.getElementById("counter1");

                const timer1 = setInterval(() => {
                    current1 += increment1;
                    if (current1 >= target1) {
                        current1 = target1;
                        counter1.innerHTML = current1.toLocaleString('id-ID') + "+";
                        clearInterval(timer1);
                    } else {
                        counter1.innerHTML = current1.toLocaleString('id-ID');
                    }
                }, stepTime1);
            </script>
            """,
        )

    with col3:
        components.html(
            """
            <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap" rel="stylesheet">
            
            <div class='feature-box summary-box'>
                <h4>Jumlah Karakter</h4>
                <div class='summary-number' id='counter2'>0</div>
            </div>

            <style>
                body {
                        font-family: 'Poppins', sans-serif;
                        margin: 0;
                        font-weight: 700;
                    }
                
                .summary-box {
                    background: linear-gradient(180deg, #fffaf5 0%, #fdf0e3 100%);
                    border: 1.5px solid #d6a06a;
                    border-radius: 22px;
                    padding: 28px 20px;
                    text-align: center;
                    box-shadow: 0 6px 18px rgba(201, 122, 43, 0.08);
                }

                .summary-box h4 {
                    margin: 0 0 10px 0;
                    color: #7c4a21;
                    font-size: 1.1rem;
                    font-weight: 700;
                }

                .summary-number {
                    font-size: 2.4rem;
                    font-weight: 900;
                    color: #9c6030;
                    line-height: 1.2;
                }
            </style>

            <script>
                let current2 = 0;
                const target2 = 20;
                const duration2 = 2000;
                const stepTime2 = 60;
                const increment2 = 1;

                const counter2 = document.getElementById("counter2");

                const timer2 = setInterval(() => {
                    current2 += increment2;
                    if (current2 >= target2) {
                        current2 = target2;
                        counter2.innerHTML = current2 + " Karakter";
                        clearInterval(timer2);
                    } else {
                        counter2.innerHTML = current2;
                    }
                }, stepTime2);
            </script>
            """,
        )

    st.markdown("<div class='nav-divider'></div></div>", unsafe_allow_html=True)
    
    # =========================
    # TEKNOLOGI PADA DASHBOARD
    # =========================
    tech1, tech2, tech3 = st.columns(3)

    st.markdown(
        """
        <div class='tech-intro'>
            <h3>Teknologi Yang Digunakan</h3>
            <p>
                Aplikasi ini dikembangkan menggunakan berbagai teknologi modern untuk memproses gambar, 
                melatih model pembelajaran mendalam, dan mengenali pola karakter aksara Jawa dengan 
                lebih mudah dan interaktif.
            </p>
            <p>
                ꦄꦥ꧀ꦭꦶꦏꦱꦶ ꦆꦤꦶ ꦢꦶꦏꦺꦩ꧀ꦧꦤ꧀ꦒ꧀ꦏꦤ꧀ ꦩꦺꦤ꧀ꦒ꧀ꦒꦸꦤꦏꦤ꧀ ꦧꦺꦂꦧꦒꦻ ꦠꦺꦏ꧀ꦤꦺꦴꦭꦺꦴꦒꦶ ꦩꦺꦴꦢꦺꦂꦤ꧀ ꦈꦤ꧀ꦠꦸꦏ꧀ ꦩꦺꦩ꧀ꦥ꧀ꦫꦺꦴꦱꦺꦱ꧀ ꦒꦩ꧀ꦧꦂ꧈​ 
                ꦩꦺꦭꦠꦶꦃ ꦩꦺꦴꦢꦺꦭ꧀ ꦥꦺꦩ꧀ꦧꦺꦭꦗꦫꦤ꧀ ꦩꦺꦤ꧀ꦢꦭꦩ꧀꧈​ ꦢꦤ꧀ ꦩꦺꦤ꧀ꦒꦺꦤꦭꦶ ꦥꦺꦴꦭ ꦏꦫꦏ꧀ꦠꦺꦂ ꦄꦏ꧀ꦱꦫ ꦙꦮ ꦢꦺꦤ꧀ꦒꦤ꧀ 
                ꦭꦺꦧꦶꦃ ꦩꦸꦢꦃ ꦢꦤ꧀ ꦆꦤ꧀ꦠꦺꦫꦏ꧀ꦠꦶꦥ꦳꧀꧉​
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    tech_col1, tech_col2, tech_col3 = st.columns(3)

    with tech_col1:
        st.markdown(
            """
            <div class='tech-card numpy'>
                <img src='https://upload.wikimedia.org/wikipedia/commons/3/31/NumPy_logo_2020.svg' class='tech-logo'>
                <h4>NumPy</h4>
                <p>
                    Digunakan untuk mengolah data numerik, array, dan matriks
                    sebagai dasar pemrosesan citra karakter.
                </p>
                <br>
                <p>
                    ꦟꦸꦩ꧀ꦦ꧀ꦪ꧀ ꦢꦶꦥꦸꦤ꧀ꦒꦶꦤꦏꦏꦺꦤ꧀ ꦏꦤ꧀ꦒ꧀ꦒꦺ ꦤ꧀ꦒꦺꦴꦭꦃ ꦢꦠ ꦄꦤ꧀ꦒ꧀ꦏ꧈​ ꦄꦂꦫꦪ꧀꧈​ ꦱꦲ ꦩꦠ꧀ꦫꦶꦏ꧀ꦱ꧀ ꦆꦤ꧀ꦒ꧀ꦏꦤ꧀ꦒ꧀ ꦢꦢꦺꦴꦱ꧀ ꦢ꧀ꦲꦱꦂ ꦥꦤ꧀ꦒꦺꦴꦭꦲꦤ꧀ ꦕꦶꦠ꧀ꦫ ꦄꦏ꧀ꦱꦫ꧉​
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class='tech-card opencv'>
                <img src='https://upload.wikimedia.org/wikipedia/commons/3/32/OpenCV_Logo_with_text_svg_version.svg' class='tech-logo'>
                <h4>OpenCV</h4>
                <p>
                    OpenCV dimanfaatkan untuk membaca, memproses, dan memanipulasi gambar
                    karakter agar siap digunakan.
                </p>
                <br>
                <p>
                    ꦎꦥꦺꦤ꧀ꦖ꧀ꦮ꦳꧀ ꦢꦶꦩꦤ꧀ꦥ꦳ꦴꦠ꧀ꦏꦤ꧀ ꦈꦤ꧀ꦠꦸꦏ꧀ ꦩꦺꦩ꧀ꦧꦕ꧈​ ꦩꦺꦩ꧀ꦥ꧀ꦫꦺꦴꦱꦺꦱ꧀꧈​ ꦢꦤ꧀ ꦩꦺꦩꦤꦶꦥꦸꦭꦱꦶ ꦒꦩ꧀ꦧꦂ ꦏꦫꦏ꧀ꦠꦺꦂ ꦄꦒꦂ ꦱꦶꦪꦥ꧀ ꦢꦶꦒꦸꦤꦏꦤ꧀꧉​
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with tech_col2:
        st.markdown(
            """
            <div class='tech-card tensorflow'>
                <img src='https://upload.wikimedia.org/wikipedia/commons/2/2d/Tensorflow_logo.svg' class='tech-logo'>
                <h4>TensorFlow</h4>
                <p>
                    TensorFlow digunakan sebagai framework utama untuk membangun
                    dan melatih model deep learning.
                </p>
                <br>
                <p>
                    ꦡꦺꦤ꧀ꦱꦺꦴꦂꦦ꦳ꦭꦺꦴꦮ꧀ ꦢꦶꦥꦸꦤ꧀ꦒꦶꦤꦏꦏꦺꦤ꧀ ꦢꦢꦺꦴꦱ꧀ ꦏꦺꦫꦤ꧀ꦒ꧀ꦏ ꦈꦠꦩ ꦏꦤ꧀ꦒ꧀ꦒꦺ ꦢꦩꦺꦭ꧀ ꦱꦲ ꦤ꧀ꦒ꧀ꦭꦠꦶꦃ ꦩꦺꦴꦢꦺꦭ꧀ ꦢꦺꦲꦺꦥ꧀ ꦭꦺꦪꦂꦤꦶꦤ꧀ꦒ꧀꧉​
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class='tech-card keras'>
                <img src='https://upload.wikimedia.org/wikipedia/commons/a/ae/Keras_logo.svg' class='tech-logo'>
                <h4>Keras</h4>
                <p>
                    Keras membantu dalam menyusun arsitektur jaringan saraf
                    agar lebih mudah dan efisien.
                </p>
                <br>
                <p>
                    ꦑꦺꦫꦱ꧀ ꦩꦶꦒꦸꦤꦤꦶ ꦏꦤ꧀ꦒ꧀ꦒꦺ ꦤ꧀ꦪꦸꦱꦸꦤ꧀ ꦄꦂꦱꦶꦠꦺꦏ꧀ꦠꦸꦂ ꦗꦫꦶꦤ꧀ꦒꦤ꧀ ꦱꦫꦥ꦳꧀ ꦱꦸꦥꦢꦺꦴꦱ꧀ ꦭꦤ꧀ꦒ꧀ꦏꦸꦤ꧀ꦒ꧀ ꦒꦩ꧀ꦥꦤ꧀ꦒ꧀ ꦭꦤ꧀ ꦌꦥ꦳ꦶꦱꦶꦪꦺꦤ꧀꧉​
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with tech_col3:
        st.markdown(
            """
            <div class='tech-card cnn'>
                <img src='https://cdn-icons-png.flaticon.com/256/6461/6461928.png' class='tech-logo'>
                <h4>CNN</h4>
                <p>
                    CNN digunakan untuk mengenali pola visual pada citra
                    karakter Aksara Jawa secara otomatis.
                </p>
                <br>
                <p>
                    ꦖ꧀ꦟ꧀ꦟ꧀ ꦢꦶꦥꦸꦤ꧀ꦒꦶꦤꦏꦏꦺꦤ꧀ ꦏꦤ꧀ꦒ꧀ꦒꦺ ꦤ꧀ꦒꦺꦤꦭꦶ ꦥꦺꦴꦭ ꦮ꦳ꦶꦱꦸꦮꦭ꧀ 
                    ꦮꦺꦴꦤ꧀ꦠꦺꦤ꧀ ꦆꦤ꧀ꦒ꧀ ꦕꦶꦠ꧀ꦫ ꦏꦫꦏ꧀ꦠꦺꦂ ꦄꦏ꧀ꦱꦫ ꦙꦮ ꦏꦤ꧀ꦠ꧀ꦲꦶ ꦎꦠꦺꦴꦩꦠꦶꦱ꧀꧉​
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class='tech-card resnet'>
                <img src='https://img.icons8.com/color/96/artificial-intelligence.png' class='tech-logo'>
                <h4>ResNet</h4>
                <p>
                    Asitektur untuk meningkatkan performa model
                    dengan pendekatan residual learning.
                </p>
                <br>
                <p>
                    ꦄꦱꦶꦠꦺꦏ꧀ꦠꦸꦂ ꦈꦤ꧀ꦠꦸꦏ꧀ ꦩꦺꦤꦶꦤ꧀ꦒ꧀ꦏꦠ꧀ꦏꦤ꧀ ꦥꦺꦂꦥ꦳ꦺꦴꦂꦩ ꦩꦺꦴꦢꦺꦭ꧀ ꦢꦺꦤ꧀ꦒꦤ꧀ ꦥꦺꦤ꧀ꦢꦺꦏꦠꦤ꧀ ꦫꦺꦱꦶꦢꦸꦮꦭ꧀ ꦭꦺꦪꦂꦤꦶꦤ꧀ꦒ꧀꧉​
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

elif page == "Data":
    st.switch_page('pages/data.py')

elif page == "Predict":
    st.switch_page('pages/prediksi.py')

elif page == "Canvas":
    st.switch_page('pages/canvas.py')


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
        padding: 30px;
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

    .stInfo {
        border-radius: 16px;
    }
    
    .tech-box {
        margin-bottom: 16px;
        min-height: 165px;
    }
    .tech-intro {
        background: linear-gradient(180deg, #fff8f1 0%, #fdf0e3 100%);
        border: 1.5px solid #d6a06a;
        border-radius: 22px;
        padding: 22px 24px;
        margin-bottom: 24px;
        box-shadow: 0 8px 20px rgba(156, 96, 48, 0.08);
    }

    .tech-intro h3 {
        margin: 0 0 8px 0;
        color: #7a4a2b;
        font-size: 1.5rem;
        font-weight: 800;
    }

    .tech-intro p {
        margin: 0;
        color: #5f4b3a;
        font-size: 1rem;
        line-height: 1.8;
    }

    .tech-card {
        background: linear-gradient(180deg, #fffaf5 0%, #fdf0e3 100%);
        border-radius: 22px;
        padding: 24px;
        margin-bottom: 22px;
        min-height: 320px;
        text-align: center;
        box-shadow: 0 10px 24px rgba(201, 122, 43, 0.10);
        transition: all 0.3s ease;
        border: 1px solid #e7c9a9;
    }

    .tech-card:hover {
        transform: translateY(-4px);
    }

    .tech-logo {
        width: 90px;
        height: 90px;
        object-fit: contain;
        margin-bottom: 14px;
    }

    .tech-card h4 {
        margin-top: 0;
        margin-bottom: 10px;
        color: #7c4a21;
        font-size: 1.18rem;
        font-weight: 800;
    }

    .tech-card p {
        margin-bottom: 0;
        color: #5f4b3a;
        font-size: 0.97rem;
        line-height: 1.75;
    }

    .tech-card.numpy {
        border: 2px solid #d6a06a;
    }

    .tech-card.opencv {
        border: 2px solid #c9813a;
    }

    .tech-card.tensorflow {
        border: 2px solid #d88a3d;
    }

    .tech-card.keras {
        border: 2px solid #b16b2f;
    }

    .tech-card.cnn {
        border: 2px solid #9c6030;
    }

    .tech-card.resnet {
        border: 2px solid #7a4a2b;
    }

    .tech-card.numpy:hover {
        box-shadow: 0 10px 25px rgba(214, 160, 106, 0.35);
    }

    .tech-card.opencv:hover {
        box-shadow: 0 10px 25px rgba(201, 129, 58, 0.35);
    }

    .tech-card.tensorflow:hover {
        box-shadow: 0 10px 25px rgba(216, 138, 61, 0.35);
    }

    .tech-card.keras:hover {
        box-shadow: 0 10px 25px rgba(177, 107, 47, 0.35);
    }

    .tech-card.cnn:hover {
        box-shadow: 0 10px 25px rgba(156, 96, 48, 0.35);
    }

    .tech-card.resnet:hover {
        box-shadow: 0 10px 25px rgba(122, 74, 43, 0.35);
    }
    </style>
    """,
    unsafe_allow_html=True
)

