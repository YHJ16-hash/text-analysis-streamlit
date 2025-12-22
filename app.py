import streamlit as st
import jieba
from collections import Counter
import re
from snownlp import SnowNLP

# 页面基础配置
st.set_page_config(
    page_title="文本分析工具",
    page_icon="📝",
    layout="wide"
)

# 标题与说明
st.title("📝 文本分析Web应用")
st.markdown("### 支持功能：字数统计、词频分析、情感倾向分析")

# 文本输入区域
text_input = st.text_area(
    "请输入需要分析的文本内容",
    height=200,
    placeholder="例如：今天天气很好，我很开心！"
)

# 分析按钮
if st.button("开始分析"):
    if text_input.strip() == "":
        st.warning("请输入文本内容后再分析！")
    else:
        # 1. 基础字数统计
        st.subheader("1. 基础字数统计")
        total_char = len(text_input)  # 总字符数
        total_char_no_space = len(re.sub(r"\s+", "", text_input))  # 去除空格后的字符数
        word_count = len(jieba.lcut(text_input))  # 分词后的词数
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("总字符数", total_char)
        with col2:
            st.metric("去除空格后字符数", total_char_no_space)
        with col3:
            st.metric("分词后词数", word_count)

        # 2. 词频分析（过滤停用词）
        st.subheader("2. 高频词汇分析")
        # 简单停用词列表
        stop_words = ["的", "了", "是", "我", "你", "他", "她", "它", "在", "和", "就", "都", "而", "也", "还", "个", "这", "那"]
        # 分词并过滤
        words = jieba.lcut(text_input)
        words_filtered = [w for w in words if w not in stop_words and len(w) > 1 and not w.isdigit()]
        # 统计前10个高频词
        word_freq = Counter(words_filtered).most_common(10)
        if word_freq:
            st.bar_chart(dict(word_freq))
        else:
            st.info("无有效高频词汇（已过滤停用词/数字/单字）")

        # 3. 情感倾向分析（修复核心错误：调整st.metric参数）
        st.subheader("3. 情感倾向分析")
        s = SnowNLP(text_input)
        sentiment_score = s.sentiments  # 情感得分（0-1，越接近1越积极）
        sentiment_label = "积极" if sentiment_score > 0.6 else "中性" if sentiment_score > 0.4 else "消极"
        
        # 正确写法：st.metric(标签, 主值, 可选的变化值)
        # 把情感标签作为主标题的一部分，避免参数错误
        st.metric(f"情感得分（{sentiment_label}）", round(sentiment_score, 3))

# 侧边栏信息
with st.sidebar:
    st.markdown("### 关于应用")
    st.markdown("这是一个基于Streamlit开发的文本分析工具，支持中文文本的基础分析。")
    st.markdown("技术栈：Python + Streamlit + jieba + snownlp")