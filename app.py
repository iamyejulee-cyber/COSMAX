import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

st.set_page_config(
    page_title="오늘뭐먹지 (OneMenu)",
    page_icon="🍽️",
    layout="wide",
)

# Streamlit 기본 여백/패딩을 최대한 줄여서 index.html이 앱처럼 보이게 함
st.markdown(
    """
    <style>
        .block-container {
            padding-top: 0rem;
            padding-bottom: 0rem;
            padding-left: 0rem;
            padding-right: 0rem;
            max-width: 100% !important;
        }
        header[data-testid="stHeader"] {
            background: transparent;
        }
        iframe {
            border: none;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

HTML_PATH = Path(__file__).parent / "index.html"
html_content = HTML_PATH.read_text(encoding="utf-8")

# index.html은 자체 완결형 정적 SPA(HTML/CSS/JS, 백엔드 호출 없음)이므로
# iframe 컴포넌트에 그대로 임베드한다.
components.html(html_content, height=2600, scrolling=True)
