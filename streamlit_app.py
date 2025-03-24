import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# 초기 데이터 설정
if 'users' not in st.session_state:
    st.session_state.users = [
        {'id': 1, 'email': 'test@test.com', 'password': 'test123', 'name': '테스트 사용자'}
    ]

if 'events' not in st.session_state:
    st.session_state.events = []

# 페이지 설정
st.set_page_config(
    page_title="일정 관리 시스템",
    page_icon="📅",
    layout="wide"
)

# 세션 상태 초기화
if 'user_id' not in st.session_state:
    st.session_state.user_id = None

# 로그인 페이지
def login_page():
    st.title("로그인")
    
    email = st.text_input("이메일")
    password = st.text_input("비밀번호", type="password")
    
    if st.button("로그인"):
        # 사용자 확인
        user = next((user for user in st.session_state.users 
                    if user['email'] == email and user['password'] == password), None)
        
        if user:
            st.session_state.user_id = user['id']
            st.success("로그인 성공!")
            st.experimental_rerun()
        else:
            st.error("이메일 또는 비밀번호가 잘못되었습니다.")

# 메인 캘린더 페이지
def calendar_page():
    st.title("일정 관리 시스템")
    
    # 현재 날짜 정보
    today = datetime.now()
    if 'selected_date' not in st.session_state:
        st.session_state.selected_date = today
    
    # 달력 네비게이션
    col1, col2, col3 = st.columns([1,2,1])
    with col1:
        if st.button("◀"):
            st.session_state.selected_date -= timedelta(days=30)
    with col2:
        st.write(f"### {st.session_state.selected_date.strftime('%Y년 %m월')}")
    with col3:
        if st.button("▶"):
            st.session_state.selected_date += timedelta(days=30)
    
    # 현재 월의 일정 가져오기
    month_start = st.session_state.selected_date.replace(day=1)
    month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    
    current_events = [
        event for event in st.session_state.events
        if (st.session_state.user_id == event['user_id'] and
            datetime.strptime(event['start_date'], '%Y-%m-%d').date() <= month_end.date() and
            datetime.strptime(event['end_date'], '%Y-%m-%d').date() >= month_start.date())
    ]
    
    # 일정 추가 버튼
    if st.button("새 일정 추가"):
        st.session_state.adding_event = True
    
    # 일정 추가 폼
    if st.session_state.get('adding_event', False):
        with st.form("event_form"):
            title = st.text_input("제목")
            description = st.text_area("설명")
            start_date = st.date_input("시작일")
            end_date = st.date_input("종료일")
            
            if st.form_submit_button("저장"):
                new_event = {
                    'id': len(st.session_state.events) + 1,
                    'user_id': st.session_state.user_id,
                    'title': title,
                    'description': description,
                    'start_date': start_date.strftime('%Y-%m-%d'),
                    'end_date': end_date.strftime('%Y-%m-%d')
                }
                st.session_state.events.append(new_event)
                st.success("일정이 추가되었습니다!")
                st.session_state.adding_event = False
                st.experimental_rerun()
    
    # 일정 목록 표시
    st.write("### 이번 달 일정")
    for event in current_events:
        with st.expander(f"{event['title']} ({event['start_date']})"):
            st.write(f"설명: {event['description']}")
            st.write(f"기간: {event['start_date']} ~ {event['end_date']}")
            
            if st.button(f"삭제", key=f"del_{event['id']}"):
                st.session_state.events = [e for e in st.session_state.events if e['id'] != event['id']]
                st.success("일정이 삭제되었습니다!")
                st.experimental_rerun()

# 메인 앱 로직
def main():
    if st.session_state.user_id is None:
        login_page()
    else:
        calendar_page()

if __name__ == '__main__':
    main() 