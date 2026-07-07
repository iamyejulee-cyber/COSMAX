import random
from urllib.parse import quote

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

HISTORY_SAMPLE = [
    {"dow": "수", "date": "7/2", "emoji": "🍣", "menu": "일식", "restaurant": "스시로 강남점", "today": False},
    {"dow": "목", "date": "7/3", "emoji": "🍢", "menu": "분식", "restaurant": "엽떡 판교점", "today": False},
    {"dow": "금", "date": "7/4", "emoji": "🥡", "menu": "중식", "restaurant": "홍콩반점 0410", "today": False},
    {"dow": "월", "date": "7/6", "emoji": "🍝", "menu": "양식", "restaurant": "올리브가든 파스타", "today": False},
    {"dow": "화", "date": "7/7", "emoji": "🍚", "menu": "한식", "restaurant": "놀부부대찌개", "today": True},
]

RESTAURANT_DB = [
    {"name": "이모네 백반", "category": "한식", "info": "판교역 도보 3분 · ⭐4.7", "desc": "집밥 감성 가득한 정성 한 상, 판교 직장인 인생 백반집", "tags": ["#한식", "#혼밥가능"], "catchtable": False},
    {"name": "곱창전골명가", "category": "한식", "info": "삼평동 도보 7분 · ⭐4.4", "desc": "얼큰한 곱창전골로 스트레스까지 싹 날려버리는 곳", "tags": ["#한식", "#회식맛집"], "catchtable": False},
    {"name": "스시안", "category": "일식", "info": "판교역 도보 4분 · ⭐4.6", "desc": "매일 공수하는 신선한 재료로 만드는 정통 스시 오마카세", "tags": ["#일식", "#오마카세"], "catchtable": True},
    {"name": "라멘공방", "category": "일식", "info": "정자역 도보 6분 · ⭐4.3", "desc": "진한 돈코츠 육수가 일품인 숨은 라멘 맛집", "tags": ["#일식", "#혼밥가능"], "catchtable": False},
    {"name": "파스타공장", "category": "양식", "info": "판교테크노밸리 도보 5분 · ⭐4.5", "desc": "매일 뽑는 생면으로 만드는 든든한 오늘의 파스타", "tags": ["#양식", "#데이트코스"], "catchtable": True},
    {"name": "그릴하우스", "category": "양식", "info": "알파돔시티 도보 8분 · ⭐4.1", "desc": "육즙 가득 스테이크로 즐기는 특별한 점심 한 끼", "tags": ["#양식", "#분위기맛집"], "catchtable": True},
    {"name": "홍콩반점0410 판교점", "category": "중식", "info": "판교역 도보 6분 · ⭐4.2", "desc": "짜장면부터 탕수육까지, 실패 없는 국민 중식당", "tags": ["#중식", "#가성비"], "catchtable": False},
    {"name": "마라공방", "category": "중식", "info": "정자동 도보 5분 · ⭐4.4", "desc": "매콤함 마니아들의 성지, 커스텀 마라탕 전문점", "tags": ["#중식", "#매운맛"], "catchtable": False},
    {"name": "엽기떡볶이 판교점", "category": "분식", "info": "판교역 도보 3분 · ⭐4.3", "desc": "화끈한 매운맛으로 점심 스트레스 날려주는 분식집", "tags": ["#분식", "#매운맛"], "catchtable": False},
    {"name": "샐러디 판교점", "category": "샐러드", "info": "판교테크노밸리 도보 4분 · ⭐4.0", "desc": "가볍지만 든든하게, 커스텀 샐러드로 건강 챙기는 한 끼", "tags": ["#샐러드", "#다이어트"], "catchtable": False},
]

HISTORY_COMMENT_BANK = {
    1: [
        lambda m: f"이번 주 {m} 1번째~ 아직 여유만만이잖아 😎",
        lambda m: f"{m} 첫 등장! 산뜻하게 시작해보자고 ✨",
    ],
    2: [
        lambda m: f"{m} 벌써 2번째?! 이 정도면 인싸 메뉴 인정 👀",
        lambda m: f"{m} 2번째 등판~ 은근 자주 나온다? 🤭",
    ],
}
HISTORY_COMMENT_DEFAULT = [
    lambda m, c: f"{m} 이번 주만 {c}번째... 우리 팀 완전 {m} 부먹단 아니야? 🫠",
    lambda m, c: f"또 {m}?! 이쯤되면 {m} 명예사원 각 🏅",
    lambda m, c: f"{m} {c}연벙 중... 이제 그만 다른 것도 만나볼 때 아니야? 👉👈",
    lambda m, c: f"{m} 무한루프 각인데 팀 취향 확고한 듯 💅",
    lambda m, c: f"{m} {c}번째, 슬슬 물릴 때 되지 않았어? 😵‍💫",
]


def build_history_comment(top_menu: str, top_count: int) -> str:
    bank = HISTORY_COMMENT_BANK.get(top_count)
    if bank:
        return random.choice(bank)(top_menu)
    return random.choice(HISTORY_COMMENT_DEFAULT)(top_menu, top_count)


def build_map_links(name: str):
    query = quote(f"{name} 판교")
    return {
        "kakao": f"https://map.kakao.com/?q={query}",
        "naver": f"https://map.naver.com/p/search/{query}",
        "catchtable": f"https://app.catchtable.co.kr/ct/search/total?keyword={quote(name)}",
    }


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

st.divider()
st.subheader("📅 우리팀 최근 점심 기록")
st.caption("지난 일주일, 우리 뭐 먹었더라")
history_cols = st.columns(len(HISTORY_SAMPLE))
for col, day in zip(history_cols, HISTORY_SAMPLE):
    with col:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.caption(f"{day['dow']} · {day['date']}" + (" · 오늘" if day["today"] else ""))
        st.markdown(f"<div style='font-size:28px;'>{day['emoji']}</div>", unsafe_allow_html=True)
        st.write(f"**{day['menu']}**")
        st.caption(f"📍{day['restaurant']}")
        st.markdown('</div>', unsafe_allow_html=True)

if "history_comment" not in st.session_state:
    menu_counts = {}
    for day in HISTORY_SAMPLE:
        menu_counts[day["menu"]] = menu_counts.get(day["menu"], 0) + 1
    top_menu, top_count = sorted(menu_counts.items(), key=lambda item: item[1], reverse=True)[0]
    st.session_state.history_comment = build_history_comment(top_menu, top_count)
st.info(st.session_state.history_comment)

st.subheader("🍽️ 판교 맛집 카드")
typed_categories = {
    classify_menu(member["menuText"])
    for member in st.session_state.team_members
    if member["menuText"].strip() and classify_menu(member["menuText"]) != ETC_CATEGORY["key"]
}
if typed_categories:
    resto_list = [r for r in RESTAURANT_DB if r["category"] in typed_categories]
    st.caption(f"지금 적어주신 메뉴({', '.join(sorted(typed_categories))}) 기준으로 골라봤어요")
else:
    resto_list = RESTAURANT_DB
    st.caption("카테고리별로 골라둔 판교 인근 맛집이에요 (메뉴를 적으면 맞춤 추천으로 바뀌어요)")

if not resto_list:
    resto_list = RESTAURANT_DB

resto_cols = st.columns(2)
for idx, resto in enumerate(resto_list):
    with resto_cols[idx % 2]:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown(f"**{resto['name']}**")
        st.caption(resto["info"])
        st.write(resto["desc"])
        st.write(" ".join(resto["tags"]))
        links = build_map_links(resto["name"])
        link_md = f"[🟡 카카오맵]({links['kakao']}) · [🟢 네이버맵]({links['naver']})"
        if resto["catchtable"]:
            link_md += f" · [🔥 실시간 웨이팅 확인하기!]({links['catchtable']})"
        st.markdown(link_md)
        st.markdown('</div>', unsafe_allow_html=True)
