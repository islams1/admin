import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------------
# 1. إعدادات الصفحة
# ---------------------------------------------------------
st.set_page_config(layout="wide", page_title="إدارة التدريب المروري", page_icon="🎓")

# ---------------------------------------------------------
# 2. التنسيق (CSS)
# ---------------------------------------------------------
st.markdown("""
    <style>
    .stApp {
        direction: rtl; 
        text-align: right; 
        background-color: #0B1B32; 
        color: white !important; 
    }
    h1, h2, h3, h4, h5, h6, p, span, div, label, th, td {
        color: white !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    section[data-testid="stSidebar"] {
        background-color: #061121; 
        border-left: 1px solid #D4AF37; 
    }
    div[data-testid="stMetricValue"] { 
        color: #D4AF37 !important; 
    }
    div[data-testid="stMetricLabel"] {
        color: #eeeeee !important;
        font-size: 14px !important;
    }
    div[data-testid="stDataFrame"] { 
        background-color: #152D4F;
        border: 1px solid #333;
    }
    div[data-baseweb="select"] > div {
        background-color: #152D4F !important;
        color: white !important;
        border-color: #D4AF37 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. القائمة الجانبية
# ---------------------------------------------------------
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/Seal_of_the_Ministry_of_Interior_of_Egypt.png/600px-Seal_of_the_Ministry_of_Interior_of_Egypt.png", width=100)
    st.markdown("<h2 style='text-align: center; color: #D4AF37 !important;'>أكاديمية المرور</h2>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center;'>نظام إدارة التدريب (LMS)</h4>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.header("🚓 بحث مروري")
    trainee_id = st.text_input("رقم الهوية / كود المتدرب", placeholder="بحث...")
    
    st.subheader("📌 تصفية الدورات")
    course_type = st.selectbox("نوع الدورة", ["الكل", "تأهيل سلوكي (مخالفات)", "قيادة مبتدئين", "قيادة مهنية", "سلامة الطرق"])
    year_filter = st.selectbox("العام التدريبي", ["2024", "2023", "2022"])
    
    st.markdown("---")
    st.info("💡 يتم تحديث نسب الحضور والغياب تلقائياً كل 24 ساعة.")

# ---------------------------------------------------------
# 4. المحتوى الرئيسي
# ---------------------------------------------------------
st.title("🎓 لوحة متابعة العملية التدريبية")

tab1, tab2 = st.tabs(["📊 الموقف التدريبي العام", "👨‍🎓 ملف المتدرب (الدورات والشهادات)"])

# =========================================================
# التبويب الأول: الموقف التدريبي العام
# =========================================================
with tab1:
    # --- 1. المؤشرات الخمسة (KPIs) ---
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("إجمالي المسجلين", "15,420", "120+")
    col2.metric("الدورات المحجوزة", "3,250", "45+")
    col3.metric("إجمالي المخالفات المرصودة", "450", "12+", delta_color="inverse")
    col4.metric("نسبة حجز الدورات للمخالفين", "60%", "5%+")
    col5.metric("نسبة إنجاز الدورات للمخالفين", "85%", "2%+")

    st.markdown("---")

    # --- 2. الإضافة الجديدة (توزيع المسجلين + المسارات الأكثر حجزاً) ---
    row_new_1, row_new_2 = st.columns([1, 1])

    with row_new_1:
        st.subheader("🚗 إجمالي المسجلين (قيادة vs مركبات)")
        data_types = pd.DataFrame({
            'التصنيف': ['رخص قيادة (أفراد/مهني)', 'رخص مركبات (فحص/بيئة)'],
            'العدد': [10420, 5000]
        })
        fig_pie = px.pie(data_types, values='العدد', names='التصنيف', hole=0.5,
                         color_discrete_sequence=['#D4AF37', '#1F4E79'])
        fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'),
                              legend=dict(orientation="h", y=-0.1))
        st.plotly_chart(fig_pie, use_container_width=True)

    with row_new_2:
        st.subheader("📈 المسارات التدريبية الأكثر حجزاً")
        data_tracks = pd.DataFrame({
            'المسار': ['تأهيل سلوكي (إزالة مخالفات)', 'رخصة خاصة (مبتدئ)', 'رخصة درجة ثالثة', 'قيادة دراجة نارية', 'سلامة مركبات'],
            'الحجوزات': [3200, 2800, 1500, 1200, 900]
        })
        fig_bar = px.bar(data_tracks, x='الحجوزات', y='المسار', orientation='h', text='الحجوزات',
                         color='الحجوزات', color_continuous_scale=['#1F4E79', '#D4AF37'])
        fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white'),
                              yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("---")

    # --- 3. Drill-down Charts (توزيع المخالفات وتوزيع الحجوزات) ---
    data_mock = pd.DataFrame({
        'المحافظة': ['القاهرة', 'القاهرة', 'القاهرة', 'الجيزة', 'الجيزة', 'الإسكندرية', 'الإسكندرية', 'القليوبية', 'القليوبية'],
        'المديرية': ['مدينة نصر', 'مصر الجديدة', 'المعادي', 'الدقي', 'أكتوبر', 'شرق', 'المنتزه', 'شبرا', 'بنها'],
        'المخالفات': [500, 300, 200, 400, 350, 250, 200, 150, 100],
        'الحجوزات': [350, 200, 150, 300, 250, 150, 100, 80, 60]
    })

    row_drill_1, row_drill_2 = st.columns(2)
    
    with row_drill_1:
        st.subheader("📍 توزيع إجمالي المخالفات حسب المنطقة")
        selected_gov_viol = st.selectbox("اختر المحافظة (المخالفات):", ["الكل"] + list(data_mock['المحافظة'].unique()), key="gov_viol_select")
        if selected_gov_viol == "الكل":
            df_grouped_v = data_mock.groupby('المحافظة')['المخالفات'].sum().reset_index()
            fig_viol = px.bar(df_grouped_v, x='المحافظة', y='المخالفات', text='المخالفات', 
                              color='المخالفات', color_continuous_scale=['#152D4F', '#FF4B4B'])
        else:
            df_filtered_v = data_mock[data_mock['المحافظة'] == selected_gov_viol]
            fig_viol = px.bar(df_filtered_v, x='المديرية', y='المخالفات', text='المخالفات', 
                              title=f"تفاصيل مديريات {selected_gov_viol}",
                              color='المخالفات', color_continuous_scale=['#152D4F', '#FF4B4B'])
        fig_viol.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
        st.plotly_chart(fig_viol, use_container_width=True)

    with row_drill_2:
        st.subheader("🎓 توزيع حاجزي الدورات حسب المنطقة")
        selected_gov_course = st.selectbox("اختر المحافظة (الحجوزات):", ["الكل"] + list(data_mock['المحافظة'].unique()), key="gov_course_select")
        if selected_gov_course == "الكل":
            df_grouped_c = data_mock.groupby('المحافظة')['الحجوزات'].sum().reset_index()
            fig_course = px.bar(df_grouped_c, x='المحافظة', y='الحجوزات', text='الحجوزات',
                                color='الحجوزات', color_continuous_scale=['#1F4E79', '#D4AF37'])
        else:
            df_filtered_c = data_mock[data_mock['المحافظة'] == selected_gov_course]
            fig_course = px.bar(df_filtered_c, x='المديرية', y='الحجوزات', text='الحجوزات', 
                                title=f"حجوزات مديريات {selected_gov_course}",
                                color='الحجوزات', color_continuous_scale=['#1F4E79', '#D4AF37'])
        fig_course.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
        st.plotly_chart(fig_course, use_container_width=True)

    st.markdown("---")

    # =========================================================
    # 🔴 الإضافة المطلوبة: تحليل نوعية المخالفات جغرافياً 🔴
    # =========================================================
    st.subheader("🚦 تفاصيل أنواع المخالفات وتوزيعها الجغرافي")
    
    # 1. تجهيز بيانات تجريبية تحتوي على المنطقة ونوع المخالفة والعدد
    df_violation_types = pd.DataFrame({
        'المنطقة': ['القاهرة', 'القاهرة', 'القاهرة', 'القاهرة', 
                   'الجيزة', 'الجيزة', 'الجيزة', 
                   'الإسكندرية', 'الإسكندرية', 'الإسكندرية'],
        'نوع المخالفة': ['تجاوز سرعة', 'كسر إشارة', 'طمس لوحات', 'موقف عشوائي',
                        'تجاوز سرعة', 'سير عكس الاتجاه', 'موقف عشوائي',
                        'تجاوز سرعة', 'قيادة برعونة', 'كسر إشارة'],
        'العدد': [450, 320, 150, 200, 
                 380, 120, 210, 
                 290, 100, 180]
    })

    # 2. إنشاء الرسم البياني
    # نستخدم Bar Chart مع خاصية Color لتوضيح نوع المخالفة داخل كل منطقة
    fig_v_types = px.bar(
        df_violation_types, 
        x="المنطقة", 
        y="العدد", 
        color="نوع المخالفة",  # هذا ما يقسم العمود حسب نوع المخالفة
        barmode='group',       # اجعلها 'stack' لتكديسها فوق بعض، أو 'group' لتكون بجانب بعض
        text_auto=True,
        title="توزيع أعداد المخالفات حسب النوع والمنطقة",
        color_discrete_sequence=px.colors.qualitative.Pastel # ألوان هادئة ومتنوعة
    )

    # 3. تنسيق الرسم ليتناسب مع الخلفية الداكنة
    fig_v_types.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)', 
        font=dict(color='white'),
        legend=dict(orientation="h", y=1.1, title=None), # مفتاح الرسم بالأعلى
        xaxis=dict(gridcolor='#203A60'),
        yaxis=dict(gridcolor='#203A60')
    )

    st.plotly_chart(fig_v_types, use_container_width=True)
    st.markdown("---")
    # =========================================================

    # --- 5. مخطط الأداء الزمني ---
    st.subheader("📈 معدلات الأداء والمخالفات الشهرية")
    
    chart_data = pd.DataFrame({
        'الشهر': ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو'],
        'عدد_المخالفات': [90, 95, 100, 110, 105, 115],
        'حجز_الدورات': [60, 70, 75, 85, 90, 100]
    })
    
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=chart_data['الشهر'], y=chart_data['عدد_المخالفات'], mode='lines+markers', name='عدد المخالفات', 
                              line=dict(dash='dash', color='#FF4B4B', width=3)))
    fig3.add_trace(go.Scatter(x=chart_data['الشهر'], y=chart_data['حجز_الدورات'], mode='lines+markers', name='الحاجزين للدورات', 
                              line=dict(color='#D4AF37', width=4)))
    
    fig3.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white'), 
                       xaxis=dict(gridcolor='#203A60'), yaxis=dict(gridcolor='#203A60'), legend=dict(orientation="h", y=1.1))
    st.plotly_chart(fig3, use_container_width=True)

# =========================================================
# التبويب الثاني: ملف المتدرب 
# =========================================================
with tab2:
    st.markdown("### 📂 السجل التدريبي للمواطن")
    
    if trainee_id:
        col_profile_img, col_profile_data = st.columns([1, 5])
        with col_profile_img:
            st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=130)
        with col_profile_data:
            st.markdown(f"## المتدرب: محمد أحمد محمود")
            st.markdown(f"**رقم الملف:** {trainee_id} | **الفئة:** سائق رخصة خاصة")
            st.caption("تاريخ آخر دخول للمنصة: منذ ساعتين")
            m1, m2, m3 = st.columns(3)
            m1.info("معدل الحضور: 95%")
            m2.success("المعدل التراكمي: 88% (جيد جداً)")
            m3.warning("ملاحظات المدرب: يحتاج تركيز في الركن")

        st.markdown("---")

        st.subheader("📚 الدورات المسجلة ونسب الإنجاز")
        courses_data = pd.DataFrame([
            {"اسم الدورة": "إعادة تأهيل سلوكي (إلزامية)", "تاريخ البدء": "2024-03-01", "المحاضر": "لواء/ حسين مصطفى", "التقدم": 100, "الدرجة": 95, "الحالة": "تمت", "الشهادة": True},
            {"اسم الدورة": "ميكانيكا الطوارئ", "تاريخ البدء": "2024-03-10", "المحاضر": "م/ علي حسن", "التقدم": 60, "الدرجة": 0, "الحالة": "جارية", "الشهادة": False},
            {"اسم الدورة": "الإسعافات الأولية للطرق", "تاريخ البدء": "2024-04-05", "المحاضر": "د/ سارة مجدي", "التقدم": 10, "الدرجة": 0, "الحالة": "جارية", "الشهادة": False},
            {"اسم الدورة": "اختبار الإشارات", "تاريخ البدء": "2024-01-15", "المحاضر": "نظام آلي", "التقدم": 100, "الدرجة": 45, "الحالة": "راسب", "الشهادة": False}
        ])
        column_config = {
            "اسم الدورة": st.column_config.TextColumn("اسم البرنامج التدريبي", width="medium"),
            "التقدم": st.column_config.ProgressColumn("نسبة الإنجاز", format="%d%%", min_value=0, max_value=100),
            "الدرجة": st.column_config.NumberColumn("الدرجة النهائية", format="%d / 100"),
            "الشهادة": st.column_config.CheckboxColumn("إصدار الشهادة", disabled=True),
        }
        st.data_editor(courses_data, column_config=column_config, use_container_width=True, hide_index=True, disabled=True)

        st.markdown("---")
        
        col_violations, col_schedule = st.columns([1, 1])
        
        with col_violations:
            st.subheader("⚠️ المخالفات الموجبة للتدريب")
            violations_linked = pd.DataFrame({
                'المخالفة': ['تجاوز السرعة المقررة', 'تجاوز السرعة المقررة'],
                'تاريخ المخالفة': ['2024-02-28', '2024-02-28'],
                'الدورة المطلوبة': ['إعادة تأهيل سلوكي', 'إعادة تأهيل سلوكي'],
                'حالة الدورة': ['مكتملة', 'مكتملة'],
                'سداد الغرامة': ['تم السداد', 'تم السداد']
            })
            
            def color_payment(val):
                color = '#00cc66' if val == 'تم السداد' else '#ff4b4b'
                return f'color: {color}; font-weight: bold;'
            
            st.dataframe(
                violations_linked.style.map(color_payment, subset=['سداد الغرامة']),
                use_container_width=True,
                height=200
            )

        with col_schedule:
            st.subheader("📅 جدول المحاضرات القادمة")
            schedule_data = pd.DataFrame({
                'اليوم': ['الأحد', 'الثلاثاء'],
                'التاريخ': ['2024-05-12', '2024-05-14'],
                'المحاضرة': ['ورشة ميكانيكا عملي', 'الإسعافات الأولية (تطبيق)'],
                'القاعة': ['ورشة رقم 3', 'قاعة 5 - الدور الثاني'],
                'الوقت': ['10:00 ص', '12:30 م']
            })
            st.table(schedule_data)

        st.markdown("### 🎖️ الشهادات المتاحة للتحميل")
        completed_courses = courses_data[(courses_data['التقدم'] == 100) & (courses_data['الدرجة'] >= 50)]
        
        if not completed_courses.empty:
            cols = st.columns(len(completed_courses))
            for index, (i, row) in enumerate(completed_courses.iterrows()):
                with cols[index if index < len(cols) else 0]:
                    st.success(f"دورة: {row['اسم الدورة']}")
                    st.download_button(
                        label=f"📥 تحميل شهادة ({row['اسم الدورة']})",
                        data=f"Certificate for {row['اسم الدورة']}",
                        file_name=f"Certificate_{row['اسم الدورة']}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
        else:
            st.warning("لا توجد شهادات متاحة للتحميل حالياً.")

    else:
        st.info("👈 قم بالبحث عن متدرب في القائمة الجانبية لعرض ملفه التعليمي.")
