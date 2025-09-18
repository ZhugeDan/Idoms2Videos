"""
测试Streamlit应用
"""
import streamlit as st

st.set_page_config(
    page_title="测试应用",
    page_icon="🧪",
    layout="wide"
)

st.title("🧪 测试应用")
st.write("如果您能看到这个页面，说明Streamlit工作正常！")

st.success("✅ Streamlit应用运行正常")
st.info("现在可以运行完整的成语故事生成器了")

