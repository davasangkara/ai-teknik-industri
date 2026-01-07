import streamlit as st
import requests

# =============================
# KONFIGURASI API DEEPSEEK
# =============================
DEEPSEEK_API_KEY = "sk-b5bf59f93912456595d4f2885a2c8b56"

API_URL = "https://api.deepseek.com/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
    "Content-Type": "application/json"
}

# =============================
# UI STREAMLIT
# =============================
st.set_page_config(
    page_title="AI Teknik Industri",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 AI Asisten Teknik Industri (DeepSeek)")
st.write(
    "Asisten AI berbasis DeepSeek untuk membantu mata kuliah Teknik Industri.\n\n"
    "📌 Mendukung tanya jawab akademik\n"
    "📌 Analisis soal & konsep\n"
    "📌 *Catatan: Gambar belum bisa dianalisis langsung*"
)

# =============================
# INPUT TEKS
# =============================
prompt = st.text_area(
    "Masukkan pertanyaan / perintah",
    placeholder="Contoh: Jelaskan metode work sampling dan contohnya"
)

# =============================
# INPUT GAMBAR (OPSIONAL)
# =============================
uploaded_image = st.file_uploader(
    "Upload gambar (opsional)",
    type=["jpg", "jpeg", "png"]
)

if uploaded_image:
    st.info(
        "⚠️ DeepSeek belum mendukung analisis gambar.\n"
        "Silakan jelaskan isi gambar di kolom pertanyaan."
    )

# =============================
# PROSES AI
# =============================
if st.button("🔍 Proses"):
    if not prompt:
        st.warning("Masukkan pertanyaan terlebih dahulu.")
    else:
        with st.spinner("AI sedang berpikir..."):
            try:
                payload = {
                    "model": "deepseek-chat",
                    "messages": [
                        {
                            "role": "system",
                            "content": (
                                "Kamu adalah asisten akademik khusus mata kuliah Teknik Industri. "
                                "Jawaban harus jelas, sistematis, dan mudah dipahami mahasiswa."
                            )
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "temperature": 0.4
                }

                response = requests.post(
                    API_URL,
                    headers=HEADERS,
                    json=payload,
                    timeout=60
                )

                if response.status_code == 200:
                    result = response.json()
                    answer = result["choices"][0]["message"]["content"]

                    st.success("Jawaban AI:")
                    st.write(answer)
                else:
                    st.error("Gagal memanggil DeepSeek API")
                    st.code(response.text)

            except Exception as e:
                st.error("Terjadi kesalahan:")
                st.code(str(e))

# =============================
# FOOTER
# =============================
st.markdown("---")
st.caption("© AI Teknik Industri | Powered by DeepSeek & Python")
