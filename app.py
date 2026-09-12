import streamlit as st
import subprocess
import os
import tempfile
import json

# 1. إعدادات الصفحة والتصميم الداكن
st.set_page_config(
    page_title="LEO STORE | TikTok Optimizer & Checker",
    page_icon="🎬",
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
""", unsafe_style_text=True)

st.markdown("""
    <div class="main-header">
        <h1>🎬 LEO STORE</h1>
        <p style="color: #94a3b8; margin: 0;">المنصة المتكاملة لمعالجة وتحليل فيديوهات TikTok بأعلى جودة ودقة</p>
    </div>
""", unsafe_style_text=True)

tab1, tab2 = st.tabs(["🎬 TikTok Video Optimizer", "🔍 TikTok Checker & Downloader"])

# Tab 1: Optimizer
with tab1:
    st.subheader("⚡ معالجة الفيديو ومنع ضغط الجودة")
    st.info("سيتكفل السيرفر بضبط ترميز الفيديو إلى H.264، وتثبيت الإطارات عند 60 FPS، والحفاظ على أبعاد الفيديو الأصلية بالكامل.")
    
    uploaded_file = st.file_uploader("ارفع الفيديو (MP4, MOV, MKV)", type=["mp4", "mov", "mkv"])

    if uploaded_file is not None:
        if st.button("🚀 بدء المعالجة والتحسين"):
            with st.spinner("جاري معالجة الفيديو بترميز FFmpeg..."):
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_in:
                    tmp_in.write(uploaded_file.read())
                    input_path = tmp_in.name

                output_path = input_path + "_processed.mp4"

                ffmpeg_command = [
                    'ffmpeg', '-y', '-i', input_path,
                    '-vf', "scale=trunc(iw/2)*2:trunc(ih/2)*2",
                    '-c:v', 'libx264',
                    '-pix_fmt', 'yuv420p',
                    '-preset', 'slow',
                    '-crf', '18',
                    '-r', '60',
                    '-c:a', 'aac',
                    '-b:a', '192k',
                    output_path
                ]

                try:
                    subprocess.run(ffmpeg_command, check=True)
                    st.success("✨ تمت معالجة الفيديو بنجاح!")
                    
                    with open(output_path, "rb") as file:
                        st.download_button(
                            label="📥 تحميل الفيديو المعالج",
                            data=file,
                            file_name=f"LEO_STORE_60fps_{uploaded_file.name}",
                            mime="video/mp4"
                        )
                except Exception as e:
                    st.error(f"حدث خطأ أثناء معالجة الفيديو: {e}")
                finally:
                    if os.path.exists(input_path): os.remove(input_path)
                    if os.path.exists(output_path): os.remove(output_path)

# Tab 2: Checker
with tab2:
    st.subheader("🔍 فحص وتحليل الفيديوهات المرفوعة على TikTok")
    tiktok_url = st.text_input("ضع رابط فيديو TikTok هنا:")

    if tiktok_url:
        if st.button("📊 فحص وقراءة بيانات الفيديو"):
            with st.spinner("جاري استخراج الخصائص والبيانات التقنية للمقطع..."):
                try:
                    cmd = ['yt-dlp', '--dump-json', '--no-playlist', tiktok_url]
                    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                    data = json.loads(result.stdout)

                    views = data.get('view_count', 0)
                    likes = data.get('like_count', 0)
                    comments = data.get('comment_count', 0)
                    reposts = data.get('repost_count', 0)
                    upload_date = data.get('upload_date', 'N/A')
                    width = data.get('width', 0)
                    height = data.get('height', 0)
                    fps = data.get('fps', 0)
                    vcodec = data.get('vcodec', 'N/A')
                    tbr = data.get('tbr', 0)
                    filesize = data.get('filesize', 0) or data.get('filesize_approx', 0)
                    filesize_mb = round(filesize / (1024 * 1024), 2) if filesize else "غير معروف"

                    st.markdown(f"""
                        <div class="telegram-card">
                            <div style="border-bottom: 1px dashed #24303f; padding-bottom: 8px; margin-bottom: 12px;">
                                📹 <b>VIDEO • ANALYTICS</b> 
                                <span class="badge-green">{width}x{height}</span> 
                                <span class="badge-blue">{fps} FPS</span>
                            </div>
                            <p><b>العنوان:</b> {data.get('title', 'No Title')}</p>
                            <p><b>تاريخ الرفع:</b> {upload_date}</p>
                            <hr style="border: 0.5px solid #24303f;">
                            <p>📈 <b>الإحصائيات:</b></p>
                            <ul>
                                <li>المشاهدات: {views:,}</li>
                                <li>الاعجابات: {likes:,}</li>
                                <li>التعليقات: {comments:,}</li>
                                <li>المشاركات: {reposts:,}</li>
                            </ul>
                            <hr style="border: 0.5px solid #24303f;">
                            <p>⚙️ <b>الترميز والجودة الحقيقية:</b></p>
                            <ul>
                                <li><b>الأبعاد الأصلية:</b> {width}x{height}</li>
                                <li><b>معدل الإطارات:</b> {fps} FPS</li>
                                <li><b>نوع الكوديك:</b> {vcodec}</li>
                                <li><b>معدل البت (Bitrate):</b> ~{round(tbr/1000, 2) if tbr else 'N/A'} Mbps</li>
                                <li><b>حجم الملف:</b> {filesize_mb} MB</li>
                            </ul>
                        </div>
                    """, unsafe_style_text=True)

                    video_download_url = data.get('url')
                    if video_download_url:
                        st.write("---")
                        st.download_button(
                            label="📥 تحميل الفيديو HD بدون علامة مائية",
                            data=subprocess.run(['curl', '-s', video_download_url], capture_output=True).content,
                            file_name=f"TikTok_{data.get('id')}_HD.mp4",
                            mime="video/mp4"
                        )

                except Exception as e:
                    st.error(f"تعذر قراءة البيانات: {e}")

st.markdown("""
    <div class="footer">
        جميع الحقوق محفوظة © LEO STORE
    </div>
""", unsafe_style_text=True)