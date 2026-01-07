import streamlit as st
import google.generativeai as genai
from PIL import Image

# =============================
# KONFIGURASI API GEMINI
# =============================
API_KEY = "AIzaSyD52TQPGxf-AEVahIe2J-WFyGPYXg9FI7Y"
genai.configure(api_key=API_KEY)

# MODEL TERBARU (SUPPORT TEKS + GAMBAR)
model = genai.GenerativeModel(
    model_name="models/gemini-2.0-flash"
)

# =============================
# UI STREAMLIT
# =============================
st.set_page_config(
    page_title="AI Teknik Industri",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 AI Asisten Teknik Industri")
st.write(
    "Asisten AI untuk membantu mata kuliah Teknik Industri.\n\n"
    "📌 Bisa menjawab pertanyaan teori\n"
    "📌 Bisa menganalisis gambar (diagram, grafik, soal, layout, dll)"
)

# =============================
# INPUT TEKS
# =============================
prompt = st.text_area(
    "Masukkan pertanyaan / perintah",
    placeholder="Contoh: Analisis diagram alir pada gambar ini dan jelaskan pemborosan"
)

# =============================
# INPUT GAMBAR
# =============================
uploaded_image = st.file_uploader(
    "Upload gambar (opsional)",
    type=["jpg", "jpeg", "png"]
)

# =============================
# PROSES AI
# =============================
if st.button("🔍 Proses"):
    if not prompt:
        st.warning("Masukkan pertanyaan atau perintah terlebih dahulu.")
    else:
        with st.spinner("AI sedang menganalisis..."):
            try:
                # JIKA ADA GAMBAR
                if uploaded_image is not None:
                    image = Image.open(uploaded_image)

                    response = model.generate_content(
                        [prompt, image]
                    )

                    st.image(
                        image,
                        caption="Gambar yang dianalisis",
                        use_container_width=True
                    )

                    st.success("Hasil Analisis AI:")
                    st.write(response.text)

                # JIKA HANYA TEKS
                else:
                    response = model.generate_content(prompt)

                    st.success("Jawaban AI:")
                    st.write(response.text)

            except Exception as e:
                st.error("Terjadi kesalahan:")
                st.code(str(e))

# =============================
# FOOTER
# =============================
st.markdown("---")
st.caption("© AI Teknik Industri | Powered by Gemini 1.5 & Python")
