import streamlit as st
from datetime import datetime, timedelta
import calendar

# 페이지 설정
st.set_page_config(
    page_title="일정 관리 시스템",
    page_icon="📅",
    layout="wide"
)

# CSS 스타일 추가
st.markdown("""
<style>
    /* 전체 테마 색상 */
    :root {
        --primary-color: #7C3AED;
        --secondary-color: #A78BFA;
        --background-color: #F5F3FF;
        --text-color: #1F2937;
        --border-color: #E5E7EB;
    }

    /* 전체 배경 */
    .stApp {
        background-color: var(--background-color);
        max-width: 100%;
        padding: 1rem;
    }

    /* 반응형 컨테이너 */
    @media (max-width: 768px) {
        .stApp {
            padding: 0.5rem;
        }
        
        .main-content {
            flex-direction: column !important;
        }
        
        .calendar-grid {
            grid-template-columns: repeat(7, 1fr) !important;
            gap: 0.25rem !important;
        }
        
        .calendar-day {
            min-height: 60px !important;
            padding: 0.5rem !important;
            font-size: 0.875rem !important;
        }
        
        .event-card {
            margin-bottom: 0.75rem !important;
            padding: 0.75rem !important;
        }
        
        .event-card h4 {
            font-size: 1rem !important;
        }
        
        .event-card p {
            font-size: 0.875rem !important;
        }
    }

    /* 헤더 스타일 */
    .main-header {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        padding: 1.5rem;
        border-radius: 1rem;
        margin-bottom: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    @media (max-width: 768px) {
        .main-header {
            padding: 1rem;
            margin-bottom: 1rem;
        }
        
        .main-header h1 {
            font-size: 1.5rem !important;
        }
    }

    /* 카드 스타일 */
    .card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        margin-bottom: 1rem;
        border: 1px solid var(--border-color);
    }

    @media (max-width: 768px) {
        .card {
            padding: 1rem;
            margin-bottom: 0.75rem;
        }
    }

    /* 버튼 스타일 */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        border: none;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }

    @media (max-width: 768px) {
        .stButton > button {
            padding: 0.4rem 0.8rem;
            font-size: 0.875rem;
        }
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    /* 입력 필드 스타일 */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-radius: 0.5rem;
        border: 1px solid var(--border-color);
        padding: 0.75rem;
    }

    @media (max-width: 768px) {
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {
            padding: 0.5rem;
            font-size: 0.875rem;
        }
    }

    /* 달력 그리드 */
    .calendar-grid {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 0.5rem;
        margin-bottom: 1rem;
    }

    .calendar-day {
        background-color: white;
        padding: 0.75rem;
        border-radius: 0.5rem;
        text-align: center;
        border: 1px solid var(--border-color);
        min-height: 80px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }

    .calendar-day.today {
        background-color: var(--background-color);
        border: 2px solid var(--primary-color);
    }

    .calendar-day.has-events {
        background-color: #EEF2FF;
    }

    /* 이벤트 카드 */
    .event-card {
        background: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        border: 1px solid var(--border-color);
        transition: all 0.3s ease;
    }

    .event-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    /* 진행률 바 */
    .progress-container {
        margin-top: 0.5rem;
        background-color: #F3F4F6;
        border-radius: 0.5rem;
        overflow: hidden;
    }

    .progress-bar {
        height: 0.5rem;
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        transition: width 0.3s ease;
    }

    /* 태그 스타일 */
    .tag {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        font-size: 0.875rem;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
    }

    .tag-high {
        background-color: #FEE2E2;
        color: #DC2626;
    }

    .tag-medium {
        background-color: #FEF3C7;
        color: #D97706;
    }

    .tag-low {
        background-color: #ECFDF5;
        color: #059669;
    }

    /* 슬라이더 스타일 */
    .stSlider > div > div > div {
        background-color: var(--primary-color);
    }

    /* 컬럼 레이아웃 */
    .main-content {
        display: flex;
        gap: 1rem;
        flex-wrap: wrap;
    }

    @media (max-width: 768px) {
        .main-content {
            flex-direction: column;
            gap: 0.75rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# 초기 데이터 설정
if 'users' not in st.session_state:
    st.session_state.users = [
        {'id': 1, 'email': 'test@test.com', 'password': 'test123', 'name': '테스트 사용자'}
    ]

# 이벤트 데이터 초기화 및 마이그레이션
if 'events' not in st.session_state or not isinstance(st.session_state.events, list):
    st.session_state.events = []
else:
    # 기존 이벤트 데이터 마이그레이션
    migrated_events = []
    for event in st.session_state.events:
        if isinstance(event, dict):
            if 'progress' not in event:
                event['progress'] = 0
            migrated_events.append(event)
    st.session_state.events = migrated_events

if 'user_id' not in st.session_state:
    st.session_state.user_id = None

def format_date(date_str):
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    return date_obj.strftime('%Y년 %m월 %d일')

def get_priority_tag(priority):
    if priority == "높음":
        return '<span class="tag tag-high">높음</span>'
    elif priority == "중간":
        return '<span class="tag tag-medium">중간</span>'
    else:
        return '<span class="tag tag-low">낮음</span>'

def login_page():
    st.markdown('<div class="main-header"><h1>📅 일정 관리 시스템</h1></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 로그인")
        with st.form("login_form"):
            email = st.text_input("이메일")
            password = st.text_input("비밀번호", type="password")
            submit = st.form_submit_button("로그인", use_container_width=True)
            
            if submit:
                user = next((user for user in st.session_state.users 
                            if user['email'] == email and user['password'] == password), None)
                
                if user:
                    st.session_state.user_id = user['id']
                    st.success("로그인 성공!")
                    st.experimental_rerun()
                else:
                    st.error("이메일 또는 비밀번호가 잘못되었습니다.")
        st.markdown('</div>', unsafe_allow_html=True)

def calendar_page():
    # 헤더 영역
    st.markdown('<div class="main-header">', unsafe_allow_html=True)
    st.markdown('<h1>📅 일정 관리 시스템</h1>', unsafe_allow_html=True)
    if st.button("로그아웃", key="logout"):
        st.session_state.user_id = None
        st.experimental_rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 메인 컨텐츠
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    # 왼쪽 컬럼: 일정 추가 및 수정
    st.markdown('<div style="flex: 2;">', unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    if 'editing_event' in st.session_state and st.session_state.editing_event:
        st.markdown("### 일정 수정")
        event = st.session_state.editing_event
    else:
        st.markdown("### 새 일정 추가")
        event = None
    
    with st.form("event_form"):
        title = st.text_input("제목", value=event['title'] if event else "")
        description = st.text_area("설명", value=event['description'] if event else "")
        date_cols = st.columns(2)
        with date_cols[0]:
            start_date = st.date_input("시작일", 
                value=datetime.strptime(event['start_date'], '%Y-%m-%d').date() if event else datetime.now())
        with date_cols[1]:
            end_date = st.date_input("종료일",
                value=datetime.strptime(event['end_date'], '%Y-%m-%d').date() if event else datetime.now())
        
        priority = st.selectbox("우선순위", 
            options=["낮음", "중간", "높음"],
            index=["낮음", "중간", "높음"].index(event['priority']) if event and 'priority' in event else 0)
        
        location = st.text_input("장소", value=event['location'] if event and 'location' in event else "")
        participants = st.text_input("참석자 (쉼표로 구분)", 
            value=", ".join(event['participants']) if event and 'participants' in event else "")
        
        progress = st.slider("진행률", 0, 100, 
            value=event['progress'] if event else 0,
            format="%d%%")
        
        if event:
            submit = st.form_submit_button("일정 수정")
        else:
            submit = st.form_submit_button("일정 추가")
        
        if submit:
            if title and description:
                new_event = {
                    'id': event['id'] if event else len(st.session_state.events) + 1,
                    'user_id': st.session_state.user_id,
                    'title': title,
                    'description': description,
                    'start_date': start_date.strftime('%Y-%m-%d'),
                    'end_date': end_date.strftime('%Y-%m-%d'),
                    'priority': priority,
                    'location': location,
                    'participants': [p.strip() for p in participants.split(",")] if participants else [],
                    'progress': progress
                }
                
                if event:
                    st.session_state.events = [new_event if e['id'] == event['id'] else e 
                                            for e in st.session_state.events]
                    st.success("일정이 수정되었습니다!")
                    st.session_state.editing_event = None
                else:
                    st.session_state.events.append(new_event)
                    st.success("일정이 추가되었습니다!")
                
                st.experimental_rerun()
            else:
                st.error("제목과 설명을 입력해주세요.")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 오른쪽 컬럼: 캘린더 뷰
    st.markdown('<div style="flex: 3;">', unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    # 달력 네비게이션
    if 'selected_date' not in st.session_state:
        st.session_state.selected_date = datetime.now()
    
    nav_cols = st.columns([1,3,1])
    with nav_cols[0]:
        if st.button("◀"):
            st.session_state.selected_date -= timedelta(days=30)
            st.experimental_rerun()
    with nav_cols[1]:
        st.markdown(f"<h2 style='text-align: center;'>{st.session_state.selected_date.strftime('%Y년 %m월')}</h2>", 
                   unsafe_allow_html=True)
    with nav_cols[2]:
        if st.button("▶"):
            st.session_state.selected_date += timedelta(days=30)
            st.experimental_rerun()
    
    # 달력 그리드
    month_start = st.session_state.selected_date.replace(day=1)
    month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    
    # 현재 월의 일정
    current_events = [
        event for event in st.session_state.events
        if (st.session_state.user_id == event.get('user_id') and
            datetime.strptime(event.get('start_date', '2099-12-31'), '%Y-%m-%d').date() <= month_end.date() and
            datetime.strptime(event.get('end_date', '2000-01-01'), '%Y-%m-%d').date() >= month_start.date())
    ]
    
    # 달력 그리드 생성
    cal = calendar.monthcalendar(month_start.year, month_start.month)
    st.markdown('<div class="calendar-grid">', unsafe_allow_html=True)
    
    # 요일 헤더
    for day in ["일", "월", "화", "수", "목", "금", "토"]:
        st.markdown(f'<div class="calendar-day"><strong>{day}</strong></div>', unsafe_allow_html=True)
    
    # 날짜 그리드
    for week in cal:
        for day in week:
            if day == 0:
                st.markdown('<div class="calendar-day"></div>', unsafe_allow_html=True)
            else:
                date = month_start.replace(day=day)
                today_class = " today" if date.date() == datetime.now().date() else ""
                has_events = any(datetime.strptime(event['start_date'], '%Y-%m-%d').date() <= date.date() <= 
                               datetime.strptime(event['end_date'], '%Y-%m-%d').date() 
                               for event in current_events)
                has_events_class = " has-events" if has_events else ""
                
                st.markdown(f'<div class="calendar-day{today_class}{has_events_class}">{day}</div>', 
                          unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 일정 목록
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 이번 달 일정")
    
    if not current_events:
        st.info("이번 달 일정이 없습니다.")
    
    for event in current_events:
        st.markdown(f"""
        <div class="event-card">
            <h4>{event['title']}</h4>
            {get_priority_tag(event.get('priority', '낮음'))}
            <p><small>🗓 {format_date(event['start_date'])} ~ {format_date(event['end_date'])}</small></p>
            <p>{event['description']}</p>
            <p>📍 {event.get('location', '장소 미정')}</p>
            <p>👥 {', '.join(event.get('participants', ['참석자 없음']))}</p>
            <div class="progress-container">
                <div class="progress-bar" style="width: {event.get('progress', 0)}%;"></div>
            </div>
            <p><strong>진행률:</strong> {event.get('progress', 0)}%</p>
        </div>
        """, unsafe_allow_html=True)
        
        event_cols = st.columns([1,1,1])
        with event_cols[0]:
            if st.button("수정", key=f"edit_{event['id']}"):
                st.session_state.editing_event = event
                st.experimental_rerun()
        with event_cols[1]:
            if st.button("삭제", key=f"del_{event['id']}"):
                st.session_state.events = [e for e in st.session_state.events if e['id'] != event['id']]
                st.success("일정이 삭제되었습니다!")
                st.experimental_rerun()
        with event_cols[2]:
            new_progress = st.slider("진행률 수정", 
                                  0, 100, event.get('progress', 0), 5,
                                  format="%d%%",
                                  key=f"progress_{event['id']}")
            if new_progress != event.get('progress', 0):
                for e in st.session_state.events:
                    if e['id'] == event['id']:
                        e['progress'] = new_progress
                        break
                st.experimental_rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # main-content 닫기

def main():
    if st.session_state.user_id is None:
        login_page()
    else:
        calendar_page()

if __name__ == '__main__':
    main() 