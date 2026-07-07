import streamlit as st

st.set_page_config(
    page_title="오늘뭐먹지 (OneMenu)",
    page_icon="🍽️",
    layout="wide",
)

st.markdown(
    """
    <style>
        .block-container { padding-top: 1rem; padding-bottom: 1rem; }
        .stButton > button { border-radius: 999px; }
        .section-card {
            background: linear-gradient(135deg, #f8f5ff, #ffffff);
            border: 1px solid #e7dcff;
            border-radius: 18px;
            padding: 1rem;
            margin-bottom: 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


if "team_name" not in st.session_state:
    st.session_state.team_name = "전략마케팅팀"
if "team_members" not in st.session_state:
    st.session_state.team_members = [
        {"name": "이예주", "avatar": "🐰", "menuText": "", "restaurant": "", "done": False},
        {"name": "이영주", "avatar": "🐻", "menuText": "", "restaurant": "", "done": False},
        {"name": "이현주", "avatar": "🐱", "menuText": "", "restaurant": "", "done": False},
        {"name": "정우영", "avatar": "🦊", "menuText": "", "restaurant": "", "done": False},
        {"name": "박서윤", "avatar": "🐼", "menuText": "", "restaurant": "", "done": False},
    ]
if "show_result" not in st.session_state:
    st.session_state.show_result = False
if "result_title" not in st.session_state:
    st.session_state.result_title = ""
if "result_sub" not in st.session_state:
    st.session_state.result_sub = ""


CATEGORIES = [
    {"key": "한식", "emoji": "🍚", "keywords": ["김치찌개", "된장찌개", "비빔밥", "국밥", "불고기", "제육", "순두부", "백반", "한정식", "보쌈", "칼국수", "수제비", "설렁탕", "곰탕", "육개장", "닭갈비", "삼겹살", "냉면", "갈비", "청국장", "추어탕", "한식"]},
    {"key": "일식", "emoji": "🍣", "keywords": ["스시", "초밥", "라멘", "규동", "사시미", "회", "오니기리", "텐동", "카츠동", "우동", "소바", "일식", "돈까스", "가츠"]},
    {"key": "양식", "emoji": "🍝", "keywords": ["파스타", "피자", "스테이크", "리조또", "브런치", "버거", "샌드위치", "오믈렛", "양식", "스파게티"]},
    {"key": "중식", "emoji": "🥡", "keywords": ["짜장면", "짬뽕", "탕수육", "마라탕", "마라샹궈", "중국집", "볶음밥", "딤섬", "중식", "유린기", "깐풍기"]},
    {"key": "분식", "emoji": "🍢", "keywords": ["떡볶이", "김밥", "순대", "튀김", "라면", "분식", "만두", "핫도그"]},
    {"key": "샐러드", "emoji": "🥗", "keywords": ["샐러드", "포케", "샤브", "다이어트", "닭가슴살"]},
]
ETC_CATEGORY = {"key": "기타", "emoji": "🍽️"}


def classify_menu(text: str):
    t = text.strip()
    if not t:
        return None
    for cat in CATEGORIES:
        if any(keyword in t for keyword in cat["keywords"]):
            return cat["key"]
    return ETC_CATEGORY["key"]


def aggregated_categories():
    buckets = {cat["key"]: {"key": cat["key"], "emoji": cat["emoji"], "votes": 0, "members": []} for cat in CATEGORIES}
    etc = {"key": ETC_CATEGORY["key"], "emoji": ETC_CATEGORY["emoji"], "votes": 0, "members": []}
    for member in st.session_state.team_members:
        text = member["menuText"].strip()
        if not text:
            continue
        cat = classify_menu(text)
        entry = {"name": member["name"], "text": text}
        if cat == ETC_CATEGORY["key"]:
            etc["votes"] += 1
            etc["members"].append(entry)
        else:
            buckets[cat]["votes"] += 1
            buckets[cat]["members"].append(entry)
    result = list(buckets.values())
    if etc["votes"] > 0:
        result.append(etc)
    return result


def total_votes():
    return sum(1 for member in st.session_state.team_members if member["menuText"].strip())


st.title("오늘뭐먹지 🍽️")
st.caption("HTML 파일 없이, 앱 하나로 바로 실행되는 팀 점심 메뉴 추천기")

with st.container():
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("팀 설정")
    st.session_state.team_name = st.text_input("팀 이름", value=st.session_state.team_name)
    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button("팀원 추가"):
            st.session_state.team_members.append({"name": "새 팀원", "avatar": "✨", "menuText": "", "restaurant": "", "done": False})
    with col2:
        if st.button("초기화"):
            st.session_state.team_members = [
                {"name": "이예주", "avatar": "🐰", "menuText": "", "restaurant": "", "done": False},
                {"name": "이영주", "avatar": "🐻", "menuText": "", "restaurant": "", "done": False},
                {"name": "이현주", "avatar": "🐱", "menuText": "", "restaurant": "", "done": False},
                {"name": "정우영", "avatar": "🦊", "menuText": "", "restaurant": "", "done": False},
                {"name": "박서윤", "avatar": "🐼", "menuText": "", "restaurant": "", "done": False},
            ]
            st.session_state.team_name = "전략마케팅팀"
            st.session_state.show_result = False
    st.markdown('</div>', unsafe_allow_html=True)

st.subheader(f"{st.session_state.team_name} 팀원별 메뉴 입력")
for idx, member in enumerate(st.session_state.team_members):
    with st.container():
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        col_name, col_menu, col_rest, col_done = st.columns([1, 3, 3, 1])
        with col_name:
            st.write(f"{member['avatar']} {member['name']}")
        with col_menu:
            menu_text = st.text_input(f"menu_{idx}", value=member["menuText"], label_visibility="collapsed")
            st.session_state.team_members[idx]["menuText"] = menu_text
        with col_rest:
            restaurant_text = st.text_input(f"rest_{idx}", value=member["restaurant"], label_visibility="collapsed", placeholder="추천 맛집")
            st.session_state.team_members[idx]["restaurant"] = restaurant_text
        with col_done:
            done = st.checkbox("완료", value=member["done"], key=f"done_{idx}")
            st.session_state.team_members[idx]["done"] = done
        st.markdown('</div>', unsafe_allow_html=True)

col_a, col_b = st.columns([2, 1])
with col_a:
    if st.button("메뉴 모아서 결과 보기"):
        st.session_state.show_result = True
with col_b:
    if st.button("오늘 메뉴 확정"):
        if total_votes() == 0:
            st.warning("아직 입력된 메뉴가 없어요.")
        else:
            sorted_categories = sorted(aggregated_categories(), key=lambda item: item["votes"], reverse=True)
            winner = sorted_categories[0]
            st.session_state.result_title = f"🎉 {winner['emoji']} {winner['key']}"
            st.session_state.result_sub = "최다 득표로 확정!"
            st.session_state.show_result = True

if st.session_state.show_result:
    st.subheader("결과 보기")
    categories = aggregated_categories()
    if total_votes() == 0:
        st.info("메뉴를 입력하면 결과가 표시됩니다.")
    else:
        top_votes = max(item["votes"] for item in categories)
        for item in sorted(categories, key=lambda entry: entry["votes"], reverse=True):
            with st.container():
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.write(f"{item['emoji']} **{item['key']}** — {item['votes']}표")
                st.progress(min(item["votes"] / max(top_votes, 1), 1.0))
                if item["members"]:
                    for member in item["members"]:
                        st.write(f"- {member['name']}: {member['text']}")
                st.markdown('</div>', unsafe_allow_html=True)

        st.success(st.session_state.result_title or "결과가 준비됐어요")
        st.write(st.session_state.result_sub or "위 카테고리를 기준으로 오늘의 메뉴를 골라보세요.")

        if st.session_state.result_title:
            st.write("추천 맛집 참고")
            restaurant_examples = {
                "한식": ["이모네 백반", "곱창전골명가"],
                "일식": ["스시안", "라멘공방"],
                "양식": ["파스타공장", "그릴하우스"],
                "중식": ["홍콩반점0410 판교점", "마라공방"],
                "분식": ["엽기떡볶이 판교점"],
                "샐러드": ["샐러디 판교점"],
            }
            for name in restaurant_examples.get(st.session_state.result_title.split()[1], []):
                st.write(f"- {name}")
