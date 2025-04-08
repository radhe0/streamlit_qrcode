import streamlit as st
import qrcode
from PIL import Image
import io  # Required for handling image data in memory

def generate_qr_code_image(data_to_encode):
    """
    Generates a QR code image object for the given data.

    Args:
        data_to_encode (str): The string data (text, number, URL, etc.) to encode.

    Returns:
        PIL.Image.Image: The QR code image object, or None if data is empty.
    """
    if not data_to_encode:
        return None

    try:
        # Configure QR code instance
        qr = qrcode.QRCode(
            version=None,  # Auto-detect size
            error_correction=qrcode.constants.ERROR_CORRECT_L, # L = low (7%), M, Q, H = high (30%)
            box_size=10,
            border=4,
        )
        qr.add_data(data_to_encode)
        qr.make(fit=True)

        # Create image
        img = qr.make_image(fill_color="black", back_color="white")
        return img

    except Exception as e:
        st.error(f"An error occurred during QR code generation: {e}")
        return None

# --- Streamlit App Layout ---

st.set_page_config(page_title="QR Code Generator", layout="centered")

st.title("🔗 Simple QR Code Generator")
st.write("Enter text, a URL, a number, or any data below to generate a QR code.")

# --- Input Area ---
input_data = st.text_area(
    "Enter Data to Encode:",
    height=100,
    placeholder="e.g., https://www.streamlit.io or Your Secret Message"
)

# --- Generate Button and Display Logic ---
if st.button("Generate QR Code", type="primary"):
    if input_data:
        # Add a spinner for user feedback
        with st.spinner('Generating QR Code...'):
            qr_image_pil = generate_qr_code_image(input_data) # Get the PIL image object

        if qr_image_pil: # Check if generation was successful
            st.success("✅ QR Code Generated Successfully!")

            # --- Convert PIL image to bytes ---
            # This is needed for both st.image and st.download_button
            buf = io.BytesIO()
            qr_image_pil.save(buf, format="PNG") # Save PIL image to buffer as PNG
            byte_im = buf.getvalue()             # Get the bytes from the buffer

            # --- Display the image using the generated bytes ---
            st.image(
                byte_im, # Pass the raw bytes
                caption="Generated QR Code",
                use_column_width=True,
                output_format='PNG' # Explicitly tell streamlit it's PNG bytes
            )

            # --- Download Functionality (uses the same bytes) ---
            st.download_button(
                label="Download QR Code (.png)",
                data=byte_im,
                file_name="generated_qr_code.png",
                mime="image/png"
            )
        # Error handling for generation failure is inside generate_qr_code_image
    else:
        st.warning("⚠️ Please enter some data to generate a QR code.")

st.markdown("---")
st.markdown("Created with [Streamlit](https://streamlit.io) and [qrcode](https://github.com/lincolnloop/python-qrcode).")