import datetime
import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="우리반 수행평가 알리미", page_icon="📚", layout="centered"
)

# 🎨 위기감용 깜빡이는 애니메이션 CSS 스타일 주입
st.markdown(
    """
    <style>
    @keyframes urgent-flash {
        0% { background-color: rgba(239, 68, 68, 0.05); border-color: #ef4444; box-shadow: 0 0 0px rgba(239, 68, 68, 0); }
        50% { background-color: rgba(239, 68, 68, 0.25); border-color: #dc2626; box-shadow: 0 0 15px rgba(239, 68, 68, 0.6); }
        100% { background-color: rgba(239, 68, 68, 0.05); border-color: #ef4444; box-shadow: 0 0 0px rgba(239, 68, 68, 0); }
    }

    @keyframes warning-flash {
        0% { background-color: rgba(245, 158, 11, 0.05); border-color: #f59e0b; }
        50% { background-color: rgba(245, 158, 11, 0.2); border-color: #d97706; box-shadow: 0 0 10px rgba(245, 158, 11, 0.4); }
        100% { background-color: rgba(245, 158, 11, 0.05); border-color: #f59e0b; }
    }

    .card-dday {
        animation: urgent-flash 0.7s infinite ease-in-out;
        border: 2px solid #ef4444;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        background: white;
    }

    .card-warning {
        animation: warning-flash 1.5s infinite ease-in-out;
        border: 2px solid #f59e0b;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        background: white;
    }

    .card-normal {
        border: 1px solid #e2e8f0;
        border-left: 5px solid #4f46e5;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        background: white;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# 제목 및 소개
st.title("📚 우리반 수행평가 알리미")
st.write("마감일이 다가올수록 카드가 번쩍거립니다! 빨리 서두르세요 🏃‍♂️💨")
st.divider()

# 세션 스테이트(데이터 저장용) 초기화
if "tasks" not in st.session_state:
    # 테스트를 위해 오늘 날짜 기준 임의 설정 (오늘, 2일 뒤, 10일 뒤)
    today = datetime.date.today()
    st.session_state.tasks = [
        {
            "subject": "국어",
            "title": "한 책 읽고 독후감 쓰기",
            "date": today,  # 오늘 마감 (빨리 번쩍!)
            "desc": "지정한 도서 중 한 권을 읽고 줄거리 및 감상문 제출",
        },
        {
            "subject": "역사",
            "title": "근현대사 인물 조사 보고서",
            "date": today + datetime.timedelta(days=2),  # 2일 뒤 마감 (주의)
            "desc": "모둠별로 조사한 인물에 대한 PPT 제작 및 발표",
        },
        {
            "subject": "수학",
            "title": "수학 익힘책 풀이 검사",
            "date": today + datetime.timedelta(days=10),  # 여유 있음
            "desc": "교과서 및 익힘책 120~125쪽 풀이 완료하기",
        },
    ]

# 📌 등록된 수행평가 목록 보여주기
st.subheader("📌 다가오는 수행평가 목록")

if not st.session_state.tasks:
    st.info("등록된 수행평가가 없습니다.")
else:
    # 날짜순 정렬
    sorted_tasks = sorted(st.session_state.tasks, key=lambda x: x["date"])
    today = datetime.date.today()

    for task in sorted_tasks:
        delta = (task["date"] - today).days

        # 남은 일자에 따른 D-day 뱃지 및 애니메이션 클래스 설정
        if delta < 0:
            dday_text = f"🚨 마감 지남 ({abs(delta)}일 지남)"
            card_class = "card-dday"
        elif delta == 0:
            dday_text = "🔥 D-Day (오늘 마감!)"
            card_class = "card-dday"
        elif delta <= 3:
            dday_text = f"⏰ D-{delta} (임박!)"
            card_class = "card-warning"
        else:
            dday_text = f"⏳ D-{delta}"
            card_class = "card-normal"

        # HTML로 카드 렌더링 (깜빡임 효과 적용)
        card_html = f"""
        <div class="{card_class}">
            <div style="font-size: 0.85rem; font-weight: bold; color: #4f46e5; text-transform: uppercase; margin-bottom: 5px;">{task['subject']}</div>
            <div style="font-size: 1.2rem; font-weight: 600; margin-bottom: 5px;">{task['title']}</div>
            <div style="font-size: 0.9rem; color: #64748b; margin-bottom: 10px; font-weight: bold;">📅 마감일: {task['date']} &nbsp;|&nbsp; {dday_text}</div>
            <div style="font-size: 0.95rem; color: #475569;">{task['desc']}</div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)

# ➕ 새로운 수행평가 추가 폼
st.divider()
st.subheader("➕ 새로운 수행평가 추가하기")

with st.form("task_form", clear_on_submit=True):
    subject = st.text_input("과목명", placeholder="예: 수학, 영어")
    title = st.text_input("수행평가 제목/내용", placeholder="예: 단원평가 및 문제풀이")
    date = st.date_input("마감일자")
    desc = st.text_area(
        "상세 설명", placeholder="예: 교과서 50~60쪽 풀이 후 제출"
    )

    submitted = st.form_submit_button("등록하기")
    if submitted:
        if subject and title and date:
            st.session_state.tasks.append(
                {"subject": subject, "title": title, "date": date, "desc": desc}
            )
            st.success("수행평가가 성공적으로 추가되었습니다!")
            st.rerun()
        else:
            st.warning("과목명과 제목은 필수 입력입니다!")
