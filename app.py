import streamlit as st

from pose_detector import PoseDetector
from posture_analysis import analyze_posture
from reccomendations import get_recommendations
from utils import uploaded_file_to_rgb_image


st.set_page_config(
    page_title="PostureAI",
    page_icon="🧍",
    layout="wide",
)


def run_posture_scan(rgb_image):
    col_original, col_annotated = st.columns(2)

    with col_original:
        st.subheader("Original")
        st.image(rgb_image, use_container_width=True)

    detector = PoseDetector()
    try:
        landmarks, annotated_image = detector.detect(rgb_image)
    finally:
        detector.close()

    with col_annotated:
        st.subheader("Pose detection")
        st.image(annotated_image, use_container_width=True)

    if landmarks is None:
        st.warning(
            "No pose detected. Try a clearer photo with your full body visible "
            "and good lighting."
        )
        return

    findings = analyze_posture(landmarks)

    st.subheader("Analysis results")

    if not findings:
        st.success(
            "No major posture issues detected with the current thresholds. "
            "Keep up good alignment, or try a different angle for a second opinion."
        )
    else:
        for finding in findings:
            with st.expander(finding["issue"], expanded=True):
                st.write(finding["detail"])
                exercises = get_recommendations(finding["recommendation_key"])
                st.markdown("**Suggested exercises:**")
                for exercise in exercises:
                    st.markdown(f"- {exercise}")


st.title("PostureAI")
st.markdown(
    "Upload a **full-body or upper-body photo**, or use your camera to scan posture "
    "and get exercise suggestions."
)

scan_mode = st.radio(
    "Choose scan type",
    ["Upload image", "Camera scan"],
    horizontal=True,
)

if scan_mode == "Upload image":
    uploaded_file = st.file_uploader(
        "Choose an image",
        type=["jpg", "jpeg", "png", "webp"],
    )

    if uploaded_file is not None:
        try:
            rgb_image = uploaded_file_to_rgb_image(uploaded_file)
        except ValueError as exc:
            st.error(str(exc))
            st.stop()

        run_posture_scan(rgb_image)
    else:
        st.info("Upload an image to begin posture analysis.")

elif scan_mode == "Camera scan":
    camera_photo = st.camera_input("Take a posture photo")

    if camera_photo is not None:
        try:
            rgb_image = uploaded_file_to_rgb_image(camera_photo)
        except ValueError as exc:
            st.error(str(exc))
            st.stop()

        run_posture_scan(rgb_image)
    else:
        st.info("Use your camera to take a posture photo.")