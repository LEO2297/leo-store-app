import streamlit as st
import subprocess
import os
import tempfile

st.set_page_config(
    page_title="LEO STORE | أداة تيك توك الاحترافية",
    page_icon="⚡",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
html, body, [class*="css"] {
    font-family: 'Tajawal', sans-serif;
    direction: rtl;
    text-align: right;
}
.stApp { background-color: #0f172a; color: #f8fafc; }
.main-header {
    text-align: center;
    padding: 20px;
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
    border-radius: 12px;
    border: 1px solid #334155;
    margin-bottom: 25px;
}
.main-header h1 { color: #38bdf8; font-weight: 700; margin-bottom: 5px; }
.telegram-card {
    background-color: #18222d;
    border: 1px solid #24303f;
    border-radius: 10px;
    padding: 20px;
    color: #e1e9f0;
    font-family: monospace;
    margin-top: 15px;
}
.badge-blue { background-color: #0284c7; color: white; padding: 2px 8px; border-radius: 4px; font-size: 0.8em; }
.badge-green { background-color: #10b981; color: white; padding: 2px 8px; border-radius: 4px; font-size: 0.8em; }
.footer { text-align: center; padding: 15px; margin-top: 50px; border-top: 1px solid #334155; color: #94a3b8; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>⚡ LEO STORE - أداة تحسين وفحص فيديوهات تيك توك</h1>
    <p>منصة احترافية لمعالجة الفيديوهات بأعلى جودة (60fps / CRF 18) وفحص الروابط</p>
</div>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🎬 معالجة وتحسين الفيديو (60fps)", "🔗 فحص وتحليل روابط TikTok"])

with tab1:
    st.subheader("رفع واختبار الفيديو")
    uploaded_file = st.file_uploader("اختر فيديو للمعالجة (MP4, MOV, MKV)", type=["mp4", "mov", "mkv"])
    
    if uploaded_file is not None:
        st.video(uploaded_file)
        if st.button("🚀 بدء المعالجة والتحسين", type="primary"):
            with st.spinner("جاري المعالجة بأعلى جودة عبر FFmpeg..."):
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_in:
                        tmp_in.write(uploaded_file.read())
                        in_path = tmp_in.name
                    
                    out_path = in_path + "_out.mp4"
                    
                    cmd = [
                        "ffmpeg", "-y", "-i", in_path,
                        "-c:v", "libx264", "-crf", "18", "-preset", "slow",
                        "-r", "60", "-c:a", "aac", "-b:a", "192k",
                        out_path
                    ]
                    
                    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    
                    if res.returncode == 0:
                        st.success("✨ تم تحسين الفيديو بنجاح!")
                        with open(out_path, "rb") as file:
                            st.download_button(
                                label="📥 تحميل الفيديو المعدل (60fps)",
                                data=file,
                                file_name=f"LEO_STORE_{uploaded_file.name}",
                                mime="video/mp4"
                            )
                    else:
                        st.error("حدث خطأ أثناء معالجة الفيديو بواسطة FFmpeg.")
                        st.code(res.stderr)
                        
                    if os.path.exists(in_path): os.remove(in_path)
                    if os.path.exists(out_path): os.remove(out_path)
                except Exception as e:
                    st.error(f"حدث خطأ غير متوقع: {str(e)}")

with tab2:
    st.subheader("تحليل وفحص روابط الفيديوهات (yt-dlp)")
    video_url = st.text_input("ضع رابط فيديو تيك توك هنا:", placeholder="https://www.tiktok.com/@username/video/123456789")
    
    if st.button("🔍 فحص الرابط وجلب التفاصيل"):
        if video_url:
            with st.spinner("جاري فحص الرابط..."):
                try:
                    cmd = ["yt-dlp", "-j", video_url]
                    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    if res.returncode == 0:
                        import json
                        data = json.loads(res.stdout)
                        st.success("تم العثور على معلومات الفيديو بنجاح!")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**العنوان:** {data.get('title', 'غير محدد')}")
                            st.write(f"**صاحب الحساب:** {data.get('uploader', 'غير محدد')}")
                        with col2:
                            st.write(f"**عدد المشاهدات:** {data.get('view_count', 'غير محدد')}")
                            st.write(f"**عدد الإعجابات:** {data.get('like_count', 'غير محدد')}")
                    else:
                        st.error("تعذر جلب معلومات الرابط. تأكد من صحة الرابط.")
                except Exception as e:
                    st.error(f"حدث خطأ: {str(e)}")
        else:
            st.warning("يرجى إدخال رابط أولاً.")

st.markdown("""
<div class="footer">
    جميع الحقوق محفوظة © LEO STORE 2026
</div>
""", unsafe_allow_html=True)
