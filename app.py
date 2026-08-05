import streamlit as st
import smtplib
import sqlite3
import re
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="AZiN | عِزِين - حلول الذكاء الاصطناعي للمتاجر",
    page_icon="🟢",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ---------------------------------------------------------
# 2. تهيئة قاعدة البيانات المحلية للنسخ الاحتياطي (SQLite3)
# ---------------------------------------------------------
def init_db():
    try:
        conn = sqlite3.connect("orders.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                service_type TEXT,
                created_at TEXT
            )
        """)
        conn.commit()
        conn.close()
    except Exception as e:
        print("خطأ في إنشاء قاعدة البيانات:", e)


def save_order_to_db(name, phone, service_type):
    try:
        conn = sqlite3.connect("orders.db")
        cursor = conn.cursor()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            INSERT INTO orders (name, phone, service_type, created_at)
            VALUES (?, ?, ?, ?)
        """, (name, phone, service_type, now))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print("خطأ في حفظ قاعدة البيانات:", e)
        return False


init_db()


# ---------------------------------------------------------
# 3. دالة إرسال البريد المباشر عبر smtplib
# ---------------------------------------------------------
def send_direct_email(name, phone, service_type):
    sender_email = "azoz24zezoo@gmail.com"
    receiver_email = "azoz24zezoo@gmail.com"

    # جلب كلمة المرور بأمان دون إيقاف التطبيق في حال عدم وجودها
    sender_password = st.secrets.get("GMAIL_APP_PASSWORD", "")

    if not sender_password:
        print("خطأ: لم يتم ضبط GMAIL_APP_PASSWORD في secrets.toml")
        return False

    subject = f"🚀 طلب خدمة جديد في AZiN من: {name}"
    body = f"""
    تم استلام طلب خدمة جديد عبر المنصة:
    -----------------------------------
    👤 اسم العميل: {name}
    📱 رقم الجوال: {phone}
    🛠️ نوع الخدمة المطلوبة: {service_type if service_type else 'غير محدد'}
    ⏰ التاريخ والوقت: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    -----------------------------------
    """

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print("خطأ أثناء إرسال البريد:", e)
        return False


# ---------------------------------------------------------
# 4. تخصيص التصميم والألوان CSS
# ---------------------------------------------------------
custom_css = """
<style>
    /* محاذاة الصفحة العامة */
    .stApp {
        background-color: #0B0F17;
        color: #F8FAFC;
        direction: rtl;
        text-align: right;
    }

    h1, h2, h3, h4, p, span, div {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    .stApp h2 {
        text-align: right !important;
        color: #FFFFFF !important;
        margin-top: 20px;
        margin-bottom: 20px;
    }

    h1, h3 { color: #FFFFFF !important; }

    .highlight-green {
        color: #10B981;
        font-weight: bold;
    }

    /* بطاقات القوالب والخدمات العامة */
    .custom-card-long {
        background-color: #161F30;
        border: 1px solid #2A384C;
        border-radius: 14px;
        padding: 24px;
        margin-bottom: 20px;
        transition: all 0.3s ease;
        text-align: right;
        direction: rtl;
    }
    .custom-card-long:hover {
        border-color: #10B981;
        transform: translateX(-4px);
    }

    /* بطاقة الرابط التفاعلي القابلة للضغط بكاملها */
    .clickable-card {
        display: block;
        text-decoration: none !important;
        background-color: #161F30;
        border: 1px solid #2A384C;
        border-radius: 14px;
        padding: 24px;
        margin-bottom: 20px;
        transition: all 0.3s ease;
        text-align: right;
        direction: rtl;
        cursor: pointer;
    }
    .clickable-card:hover {
        border-color: #10B981;
        background-color: #1C273D;
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(16, 185, 129, 0.15);
    }

    /* أزرار وحقول الإدخال */
    .stTextInput label, .stSelectbox label, .stTextArea label {
        color: #FFFFFF !important;
        text-align: right !important;
        display: block;
        direction: rtl;
    }

    .stButton>button {
        background-color: #10B981 !important;
        color: #FFFFFF !important;
        font-weight: bold !important;
        font-size: 16px !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 12px 28px !important;
        width: 100% !important;
        transition: background-color 0.3s !important;
    }
    .stButton>button:hover {
        background-color: #059669 !important;
        color: #FFFFFF !important;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ---------------------------------------------------------
# 5. الهيدر العلوي
# ---------------------------------------------------------
col_left, col_header, col_right = st.columns([1, 2, 1])

with col_header:
    try:
        st.image("logo.png", use_container_width=True)
    except Exception:
        st.markdown("<h1 style='text-align: center;'>🟢 AZiN | عِزِين</h1>", unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; margin-top: 15px; margin-bottom: 40px;">
    <h1 style="font-size: 2.7rem; line-height: 1.3; margin-bottom: 16px;">
        مبيعات متجرك أكثر ذكاءً مع <span class="highlight-green">عِزِين (AZiN)</span>
    </h1>
    <p style="font-size: 1.25rem; color: #94A3B8; max-width: 800px; margin: 0 auto; line-height: 1.6;">
        عِزِين — حلول ذكية متفرقة، لتجربة تجارية متكاملة.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ---------------------------------------------------------
# 6. قسم خدمات المنصة
# ---------------------------------------------------------
st.markdown("## ⚡ خدمات المنصة")

st.markdown("""
<div class="custom-card-long">
    <h3 style="color: #10B981 !important;">🤖 عزين بوت (Azin Bot)</h3>
    <p style="color: #94A3B8; font-size: 1.1rem; line-height: 1.6;">
        مساعد مبيعات ذكي مخصص لمتجرك يقترح المنتجات للعميل بناءً على احتياجه الخاص، ويجيب على الاستفسارات والتفاصيل المعقدة فوراً لرفع معدل التحويل والمبيعات على مدار الساعة.
    </p>
</div>

<div class="custom-card-long">
    <h3>🔗 التناغم والربط مع المنصات (Seamless Integration)</h3>
    <p style="color: #94A3B8; font-size: 1.1rem; line-height: 1.6;">
        ربط مباشر ومستقر مع المنصات الرئيسية للتجارة الإلكترونية (سلة، زد، وشوبيفاي) لمزامنة المخزون، المنتجات، والطلبات تلقائياً وبأعلى سرعة ودقة.
    </p>
</div>

<div class="custom-card-long">
    <h3>📊 الأتمتة وتحليلات السلوك (Smart Analytics)</h3>
    <p style="color: #94A3B8; font-size: 1.1rem; line-height: 1.6;">
        تحليل دقيق لأسئلة العملاء وتفاعلاتهم مع البوت للتعرف على أكثر المنتجات طلباً وأبرز مخاوف الشراء، مما يعطيك تقارير ذكية لتطوير حملاتك التسويقية وزيادة الأرباح.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ---------------------------------------------------------
# 7. قسم النماذج والمشاريع التجريبية المتاحة الان
# ---------------------------------------------------------
st.markdown("## 🧪 النماذج والمشاريع التجريبية المتاحة الان")

st.markdown("""
<div style="direction: rtl; text-align: right; margin-bottom: 25px;">
    <p style="color: #F8FAFC; font-size: 1.15rem; line-height: 1.7; margin-bottom: 8px;">
        ✨ <b>اضغط على القالب لتجربة النموذج التجريبي ومعاينة آلية العمل فوراً بكفاءة واقعية.</b>
    </p>
    <p style="color: #94A3B8; font-size: 1.05rem; line-height: 1.6; margin: 0;">
        نضع بين يديك نماذج حية ومصممة بدقة لتستكشف بنفسك كيف يمكن للذكاء الاصطناعي تحويل تواصلك مع العملاء إلى تجربة بيع تفاعلية وسريعة.
    </p>
</div>
""", unsafe_allow_html=True)

# 📌 رابط مشروع "مساعد العود الملكي"
chatbot_url = "https://chatbot-5zxjmiukqtpo3ymydayza3.streamlit.app/"

st.markdown(f"""
<a href="{chatbot_url}" target="_blank" class="clickable-card">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
        <h3 style="margin: 0; color: #FFFFFF !important;">👑 نموذج تجريبي: Azin Bot - مساعد العود الملكي (Royal Oud Assistant)</h3>
        <span style="background-color: #064E3B; color: #34D399; padding: 6px 14px; border-radius: 20px; font-size: 0.85rem; font-weight: bold;">
            🔗 اضغط هنا لتجربة النموذج الأن 🟢
        </span>
    </div>
    <p style="color: #94A3B8; font-size: 1.05rem; line-height: 1.6; margin-top: 14px; margin-bottom: 5px;">
        نموذج أولي تطبيقي لمساعد مبيعات ذكي مخصص لمتاجر العود والعطور الفاخرة. يساعد الزائر في اختيار نوع العود المناسب لمناسبته، توضيح درجات الثبات والفوحان، والإجابة عن استفسارات المنتجات فوراً.
    </p>
</a>
""", unsafe_allow_html=True)

st.markdown("---")

# ---------------------------------------------------------
# 8. قسم طلب الخدمة والتواصل مع العميل
# ---------------------------------------------------------
st.markdown("## 🚀 احجز استشارة أو اطلب خدمتك الآن")
st.markdown("""
<p style="color: #CBD5E1; font-size: 1.1rem; text-align: right; line-height: 1.6;">
أدخل بياناتك وسيقوم فريق <b>AZiN</b> بالتواصل معك لمناقشة احتياجات متجرك وبناء الحل المناسب لك، أو يمكنك التواصل معنا بشكل مباشر عبر الرقم الموضح أسفل الصفحة.
</p>
""", unsafe_allow_html=True)

with st.form("contact_form", clear_on_submit=True):
    name = st.text_input("الاسم الكريم")
    phone = st.text_input("رقم الجوال")
    service_type = st.text_input("نوع الخدمة المطلوبة")

    submit = st.form_submit_button("إرسال الطلب 🟢")
    if submit:
        # التثبت من إدخال الاسم ورقم الهاتف بطريقة صحيحة
        clean_phone = re.sub(r'\s+', '', phone)
        if name.strip() and clean_phone:
            save_order_to_db(name.strip(), clean_phone, service_type.strip())
            sent = send_direct_email(name.strip(), clean_phone, service_type.strip())
            if sent:
                st.success(f"تم استلام طلبك بنجاح أستاذ {name.strip()}! سيتواصل معك فريق **AZiN** في أقرب وقت.")
            else:
                st.warning(f"تم حفظ طلبك بنجاح أستاذ {name.strip()}! وسيتواصل معك فريق **AZiN** قريباً.")
        else:
            st.warning("يرجى كتابة الاسم ورقم التواصل لتمكين فريقنا من التواصل معك.")

st.markdown("---")

# ---------------------------------------------------------
# 9. قسم النبذة
# ---------------------------------------------------------
st.markdown("## 📍 نبذة عن عِزِين (AZiN)")

st.markdown("""
<div class="custom-card-long">
    <h3 style="color: #10B981 !important;">🌐 رؤية المنظومة</h3>
    <p style="color: #CBD5E1; font-size: 1.05rem; line-height: 1.7;">
        منصة <b>AZiN (عِزِين)</b> هي منظومة تقنية متخصصة في ابتكار وتطوير حلول الذكاء الاصطناعي للمتاجر الإلكترونية. نهدف إلى سد الفجوة بين التقنيات المتقدمة واحتياجات التاجر اليومية، عبر دمج أدوات الاستجابة الذكية وأتمتة البيانات في منصة موحدة ترفع المبيعات وتحسن تجربة العميل.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="custom-card-long" style="background-color: #0F172A; border-color: #10B981;">
    <h3 style="color: #10B981 !important;">👨‍💻 عن المؤسس والمطور </h3>
    <h4 style="color: #FFFFFF; margin-top: -5px; margin-bottom: 12px;">عبدالعزيز ياسين العسيري | AI Specialist & Developer</h4>
    <p style="color: #CBD5E1; font-size: 1.05rem; line-height: 1.7;">
        خريج **بكالوريوس الذكاء الاصطناعي** من جامعة جدة بمرتبة الشرف الثانية. ممتلك لخبرة عملية في تطوير نماذج تعلّم الآلة (Machine Learning)، أتمتة البيانات، وبناء المنظومات الذكية التفاعلية.
    </p>
    <ul style="color: #94A3B8; font-size: 1rem; line-height: 1.8; margin-right: 20px;">
        <li><b>الخبرة الصناعية:</b> أخصائي ذكاء اصطناعي (تمهير) في شركة سابك (SABIC)، عملت على تطوير نماذج التنبؤ وتحليل البيانات لدعم اتخاذ القرار.</li>
        <li><b>أبرز المشاريع التقنية:</b> تطوير محرك **شات بوت تفاعلي ذكي** للمتاجر والعملاء مع ربطه بقواعد بيانات متقدمة (SQLite3 & Streamlit)، تصميم أنظمة كشف الشذوذ (Anomaly Detection)، وتطوير روبوتات أمنية وتفاعلية مستندة للرؤية الحاسوبية.</li>
        <li><b>المهارات والتقنيات:</b> Python, SQL, Streamlit, SQLite3, TensorFlow, OpenCV, RapidMiner, and Machine Learning.</li>
    </ul>
    <hr style="border-color: #1E293B; margin: 20px 0;">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
        <div>
            <p style="margin: 0; color: #94A3B8;">📱 رقم الاتصال المباشر:</p>
            <p style="margin: 0; color: #10B981; font-size: 1.1rem; font-weight: 700; direction: ltr; text-align: right;">+966 597 788 974</p>
        </div>
        <div>
            <p style="margin: 0; color: #94A3B8;">🌐 البريد الإلكتروني الرسمي:</p>
            <p style="margin: 0; color: #FFFFFF; font-weight: 500;">alasiri.ab24@gmail.com</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(
    "<br><div style='text-align: center; color: #64748B;'>© 2026 AZiN.ai — جميع الحقوق محفوظة لـ عِزِين (Aziz Intelligence)</div><br>",
    unsafe_allow_html=True)
