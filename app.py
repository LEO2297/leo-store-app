import streamlit as st
import subprocess
import os
import tempfile
import json
import re

st.set_page_config(
    page_title="LEO STORE | أداة تيك توك الاحترافية",
    page_icon="⚡",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Tajawal', sans-serif;
    direction: rtl;
    text-align: right;
}

/* خلفية المتجر السوداء الداكنة بالكامل */
.stApp {
    background-color: #080c14;
    color: #f1f5f9;
}

/* الهيدر السينمائي الفخم مع صورة هانيبال وإضاءة الجلو */
.hannibal-header {
    position: relative;
    text-align: center;
    padding: 40px 20px;
    background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(5, 7, 11, 0.98) 100%);
    border-radius: 16px;
    border: 1px solid #1e293b;
    box-shadow: 0 0 30px rgba(56, 189, 248, 0.15), inset 0 0 15px rgba(0, 0, 0, 0.5);
    margin-bottom: 30px;
    overflow: hidden;
}

/* تصميم صورة هانيبال الدائرية مع إضاءة الجلو */
.hannibal-avatar {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    object-fit: cover;
    border: 3px solid #38bdf8;
    box-shadow: 0 0 25px #38bdf8, 0 0 50px rgba(56, 189, 248, 0.4);
    margin-bottom: 15px;
    transition: transform 0.3s ease;
}

.hannibal-avatar:hover {
    transform: scale(1.05);
}

.hannibal-header h1 {
    color: #38bdf8;
    font-weight: 900;
    font-size: 2.2rem;
    margin-bottom: 10px;
    text-shadow: 0 0 10px rgba(56, 189, 248, 0.4);
}

.hannibal-header p {
    color: #94a3b8;
    font-size: 1.1rem;
}

/* تنسيق التبوابات (Tabs) بشكل أنيق ومرتب */
.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
    background-color: #0f172a;
    padding: 10px;
    border-radius: 12px;
    border: 1px solid #1e293b;
}

.stTabs [data-baseweb="tab"] {
    background-color: #1e293b;
    border-radius: 8px;
    color: #94a3b8;
    font-weight: 700;
    padding: 10px 20px;
    border: none;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important;
    color: #ffffff !important;
    box-shadow: 0 0 15px rgba(2, 132, 199, 0.5);
}

/* تحسين شكل الأزرار */
.stButton button {
    background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
    color: white;
    font-weight: 700;
    border-radius: 8px;
    border: none;
    box-shadow: 0 0 10px rgba(2, 132, 199, 0.3);
    transition: all 0.3s ease;
}

.stButton button:hover {
    background: linear-gradient(135deg, #0369a1 0%, #075985 100%);
    box-shadow: 0 0 20px rgba(2, 132, 199, 0.6);
}

/* الفوتر */
.footer {
    text-align: center;
    padding: 20px;
    margin-top: 60px;
    border-top: 1px solid #1e293b;
    color: #64748b;
    font-size: 0.9rem;
}
</style>
""", unsafe_allow_html=True)

# الهيدر السينمائي المطور مع صورتك الخاصة وإضاءة الجلو
st.markdown("""
<div class="hannibal-header">
    <img src="https://raw.githubusercontent.com/LEO2297/leo-store-app/main/IMG_0787.jpeg" class="hannibal-avatar" alt="LEO STORE Hannibal">
    <h1>⚡ LEO STORE</h1>
    <p>منصة احترافية لتحسين دقة وفريمات الفيديوهات وفحص تفاصيل الروابط بإضاءة سينمائية</p>
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
    st.subheader("تحليل وفحص روابط الفيديوهات")
    video_url = st.text_input("ضع رابط فيديو تيك توك هنا:", placeholder="https://www.tiktok.com/@username/video/123456789")
    
    if st.button("🔍 فحص الرابط وجلب التفاصيل"):
        if video_url:
            with st.spinner("جاري جلب تفاصيل الفيديو وقراءة الفريمات الدقيقة..."):
                try:
                    cmd = ["yt-dlp", "-j", video_url]
                    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    
                    if res.returncode == 0:
                        data = json.loads(res.stdout)
                        st.success("تم العثور على معلومات الفيديو بنجاح!")
                        
                        fps_real = "غير محدد"
                        
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_vid:
                            tmp_path = tmp_vid.name
                        
                        dl_cmd = [
                            "yt-dlp",
                            "--download-sections", "*00:00:00-00:00:01",
                            "-o", tmp_path,
                            "--force-overwrites",
                            video_url
                        ]
                        
                        subprocess.run(dl_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=20)
                        
                        if os.path.exists(tmp_path) and os.path.getsize(tmp_path) > 0:
                            ff_cmd = ["ffmpeg", "-i", tmp_path, "-f", "null", "-"]
                            ff_res = subprocess.run(ff_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                            
                            match = re.search(r'(\d+(?:\.\d+)?)\s*fps', ff_res.stderr)
                            if match:
                                fps_val = float(match.group(1))
                                fps_real = f"{round(fps_val)} FPS"
                            
                            os.remove(tmp_path)

                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**العنوان:** {data.get('title', 'غير محدد')}")
                            st.write(f"**صاحب الحساب:** {data.get('uploader', 'غير محدد')}")
                            st.write(f"**الدقة والجودة:** {data.get('width', '?')}x{data.get('height', '?')}")
                        with col2:
                            st.write(f"**عدد المشاهدات:** {data.get('view_count', 'غير محدد')}")
                            st.write(f"**عدد الإعجابات:** {data.get('like_count', 'غير محدد')}")
                            st.write(f"**معدل الفريمات الحقيقي:** {fps_real}")
                    else:
                        st.error("تعذر جلب معلومات الرابط. تأكد من صحة الرابط.")
                except Exception as e:
                    st.error(f"حدث خطأ أثناء الفحص: {str(e)}")
        else:
            st.warning("يرجى إدخال رابط أولاً.")

st.markdown("""
<div class="footer">
    جميع الحقوق محفوظة © LEO STORE 2026
</div>
""", unsafe_allow_html=True)
