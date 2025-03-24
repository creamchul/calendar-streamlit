import streamlit as st
from datetime import datetime, timedelta

# 페이지 설정
st.set_page_config(
    page_title="일정 관리 시스템",
    page_icon="📅",
    layout="wide"
)

# CSS 스타일 추가
st.markdown("""
<style>
    .stButton > button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
    }
    .main-header {
        text-align: center;
        padding: 1em;
        background-color: #f0f2f6;
        border-radius: 10px;
        margin-bottom: 2em;
    }
    .event-card {
        padding: 1em;
        background-color: white;
        border-radius: 5px;
        border: 1px solid #e6e6e6;
        margin-bottom: 1em;
    }
    .progress-container {
        margin-top: 1em;
        padding: 0.5em;
        background-color: #f8f9fa;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# 초기 데이터 설정
if 'users' not in st.session_state:
    st.session_state.users = [
        {'id': 1, 'email': 'test@test.com', 'password': 'test123', 'name': '테스트 사용자'}
    ]

if 'events' not in st.session_state:
    st.session_state.events = []

if 'user_id' not in st.session_state:
    st.session_state.user_id = None

def login_page():
    st.markdown('<div class="main-header"><h1>📅 일정 관리 시스템</h1></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
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

def calendar_page():
    # 헤더 영역
    col1, col2, col3 = st.columns([2,6,2])
    with col2:
        st.markdown('<div class="main-header"><h1>📅 일정 관리 시스템</h1></div>', unsafe_allow_html=True)
    with col3:
        st.button("로그아웃", key="logout", on_click=lambda: setattr(st.session_state, 'user_id', None))
    
    # 현재 날짜 정보
    today = datetime.now()
    if 'selected_date' not in st.session_state:
        st.session_state.selected_date = today
    
    # 달력 네비게이션
    col1, col2, col3 = st.columns([1,3,1])
    with col1:
        if st.button("◀ 이전 달"):
            st.session_state.selected_date -= timedelta(days=30)
    with col2:
        st.markdown(f"<h2 style='text-align: center;'>{st.session_state.selected_date.strftime('%Y년 %m월')}</h2>", unsafe_allow_html=True)
    with col3:
        if st.button("다음 달 ▶"):
            st.session_state.selected_date += timedelta(days=30)
    
    # 일정 관리 영역
    col1, col2 = st.columns([2,3])
    
    # 왼쪽 컬럼: 일정 추가
    with col1:
        st.markdown("### 새 일정 추가")
        with st.form("event_form"):
            title = st.text_input("제목")
            description = st.text_area("설명")
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input("시작일")
            with col2:
                end_date = st.date_input("종료일")
            progress = st.slider("진행률", 0, 100, 0, 5, format="%d%%")
            
            if st.form_submit_button("일정 추가", use_container_width=True):
                new_event = {
                    'id': len(st.session_state.events) + 1,
                    'user_id': st.session_state.user_id,
                    'title': title,
                    'description': description,
                    'start_date': start_date.strftime('%Y-%m-%d'),
                    'end_date': end_date.strftime('%Y-%m-%d'),
                    'progress': progress
                }
                st.session_state.events.append(new_event)
                st.success("일정이 추가되었습니다!")
                st.experimental_rerun()
    
    # 오른쪽 컬럼: 일정 목록
    with col2:
        st.markdown("### 이번 달 일정")
        month_start = st.session_state.selected_date.replace(day=1)
        month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        current_events = [
            event for event in st.session_state.events
            if (st.session_state.user_id == event['user_id'] and
                datetime.strptime(event['start_date'], '%Y-%m-%d').date() <= month_end.date() and
                datetime.strptime(event['end_date'], '%Y-%m-%d').date() >= month_start.date())
        ]
        
        if not current_events:
            st.info("이번 달 일정이 없습니다.")
        
        for event in current_events:
            with st.container():
                st.markdown(f"""
                <div class="event-card">
                    <h4>{event['title']}</h4>
                    <p><small>🗓 {event['start_date']} ~ {event['end_date']}</small></p>
                    <p>{event['description']}</p>
                    <div class="progress-container">
                        <p><strong>진행률:</strong> {event['progress']}%</p>
                        <div style="width:100%; height:20px; background-color:#e9ecef; border-radius:5px;">
                            <div style="width:{event['progress']}%; height:100%; background-color:#007bff; border-radius:5px;"></div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns([3,1])
                with col2:
                    if st.button("삭제", key=f"del_{event['id']}"):
                        st.session_state.events = [e for e in st.session_state.events if e['id'] != event['id']]
                        st.success("일정이 삭제되었습니다!")
                        st.experimental_rerun()
                with col1:
                    new_progress = st.slider("진행률 수정", 
                                          0, 100, event['progress'], 5,
                                          format="%d%%",
                                          key=f"progress_{event['id']}")
                    if new_progress != event['progress']:
                        for e in st.session_state.events:
                            if e['id'] == event['id']:
                                e['progress'] = new_progress
                                break
                        st.experimental_rerun()

def main():
    if st.session_state.user_id is None:
        login_page()
    else:
        calendar_page()

if __name__ == '__main__':
    main() 