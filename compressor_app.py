from PIL import Image
import cv2
import streamlit as st
import os

# Function to inject CSS
def inject_css(css_file):
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Function for image compression.
def compress_image(input_path: str, output_path: str, quality: int):
    image = Image.open(input_path)
    image.save(output_path, "JPEG", quality=quality)


# Function for video compression.
def compress_video(input_path: str, output_path: str, quality: int):
    video = cv2.VideoCapture(input_path)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    fps = video.get(cv2.CAP_PROP_FPS)
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    while True:
        ret, frame = video.read()
        if not ret:
            break
        out.write(frame)
    
    video.release()
    out.release()

# Integrating these functionalities into a Streamlit app.
def main():

    # Set page config
    st.set_page_config(page_title="Compressify", page_icon="📦", layout="centered")
    # Inject CSS
    inject_css("styles.css")
    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Compressify</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Your Ultimate Image and Video Compression Tool</h3>", unsafe_allow_html=True)


    option = st.selectbox("Choose what to compress", ("Image", "Video"))

    if option == "Image":
        image_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])
        if image_file is not None:
            quality = st.slider("Select Quality", 10, 100, 70)
            temp_file = "temp_image.jpg"
            with open(temp_file, "wb") as f:
                f.write(image_file.getbuffer())
            
            compress_image(temp_file, "compressed_image.jpg", quality)
            st.success("Image compressed successfully!")
            st.download_button("Download Compressed Image", open("compressed_image.jpg", "rb"), "compressed_image.jpg")

    elif option == "Video":
        video_file = st.file_uploader("Upload a Video", type=["mp4", "avi", "mov"])
        if video_file is not None:
            quality = st.slider("Select Quality", 10, 100, 70)
            temp_file = "temp_video.mp4"
            with open(temp_file, "wb") as f:
                f.write(video_file.getbuffer())
            
            compress_video(temp_file, "compressed_video.mp4", quality)
            st.success("Video compressed successfully!")
            st.download_button("Download Compressed Video", open("compressed_video.mp4", "rb"), "compressed_video.mp4")

if __name__ == "__main__":
    main()