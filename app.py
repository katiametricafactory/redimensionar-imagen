import streamlit as st
from PIL import Image
from rembg import remove
import io

# ---------------- CONFIGURACIÓN ----------------
st.set_page_config(
    page_title="Redimensionar Imagen Sin Fondo",
    page_icon="🖼️",
    layout="centered"
)

# ---------------- ESTILOS CSS ----------------
st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}
h1 {
    text-align: center;
}
.stDownloadButton button {
    background-color: #111827;
    color: white;
    border-radius: 8px;
    padding: 0.6em 1.2em;
}
.stDownloadButton button:hover {
    background-color: #374151;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.title("🖼️ Redimensionar imagen")
st.markdown(
    "<p style='text-align:center; color:gray;'>"
    "Sube una imagen y obtén un PNG transparente optimizado (185x75 px)"
    "</p>",
    unsafe_allow_html=True
)

st.divider()

# ---------------- PARÁMETROS ----------------
TARGET_WIDTH = 185
TARGET_HEIGHT = 75

# ---------------- UPLOAD ----------------
uploaded_file = st.file_uploader(
    "Selecciona una imagen",
    type=["png", "jpg", "jpeg", "webp"]
)

if uploaded_file:

    col1, col2 = st.columns(2)

    # Imagen original
    with col1:
        st.subheader("Original")
        original = Image.open(uploaded_file).convert("RGBA")
        st.image(original, use_container_width=True)

    # Procesamiento
    with st.spinner("Procesando imagen..."):

        output = remove(original)

        w, h = output.size
        scale = min(TARGET_WIDTH / w, TARGET_HEIGHT / h)
        new_w = int(w * scale)
        new_h = int(h * scale)

        resized = output.resize((new_w, new_h), Image.Resampling.LANCZOS)

        canvas = Image.new("RGBA", (TARGET_WIDTH, TARGET_HEIGHT), (255, 255, 255, 0))

        offset_x = (TARGET_WIDTH - new_w) // 2
        offset_y = (TARGET_HEIGHT - new_h) // 2

        canvas.paste(resized, (offset_x, offset_y), resized)

    # Imagen final
    with col2:
        st.subheader("Resultado")
        st.image(canvas, use_container_width=True)

    st.divider()

    # Descargar
    buf = io.BytesIO()
    canvas.save(buf, format="PNG")
    byte_im = buf.getvalue()

    st.download_button(
        "⬇ Descargar PNG",
        byte_im,
        file_name="imagen_sin_fondo.png",
        mime="image/png",
        use_container_width=True
    )

    st.success("Imagen lista para descargar")


