import streamlit as st
import requests
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 应用配置
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api/v1")

st.set_page_config(
    page_title="古诗词RAG系统",
    page_icon="📜",
    layout="wide"
)

st.title("📜 古诗词RAG检索系统")

# 侧边栏
st.sidebar.header("系统功能")
app_mode = st.sidebar.selectbox(
    "选择功能",
    ["诗词检索", "诗人查询", "主题搜索", "情感搜索", "知识图谱", "情感分析"]
)

if app_mode == "诗词检索":
    st.header("🔍 诗词检索")
    
    # 查询输入
    query = st.text_input("请输入您要查询的诗词关键词、诗句或问题：")
    
    # 参数设置
    col1, col2 = st.columns(2)
    with col1:
        top_k = st.slider("返回结果数量", 1, 20, 5)
    with col2:
        use_rag = st.checkbox("启用RAG生成", value=True)
    
    if st.button("搜索") and query:
        with st.spinner("正在搜索中..."):
            try:
                # 调用后端API
                response = requests.post(
                    f"{API_BASE_URL}/query",
                    json={
                        "query": query,
                        "top_k": top_k,
                        "use_rag": use_rag
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # 显示生成的答案
                    if data.get("generated_answer"):
                        st.subheader("🤖 AI回答")
                        st.write(data["generated_answer"])
                    
                    # 显示检索结果
                    st.subheader("📚 检索结果")
                    for result in data.get("results", []):
                        poem = result["poem"]
                        with st.expander(f"{poem['title']} - {poem['author']}"):
                            st.write(f"**朝代**: {poem['dynasty']}")
                            st.write(f"**内容**: \n{poem['content']}")
                            if poem.get("translation"):
                                st.write(f"**译文**: \n{poem['translation']}")
                            if poem.get("annotation"):
                                st.write(f"**注释**: \n{poem['annotation']}")
                            st.write(f"**相似度**: {result['similarity_score']:.4f}")
                            st.write(f"**来源**: {result['source']}")
                    
                    # 显示情感分析
                    if data.get("sentiment_analysis"):
                        st.subheader("❤️ 情感分析")
                        sentiment = data["sentiment_analysis"]
                        st.write(f"情感倾向: {sentiment.get('sentiment')}")
                        st.write(f"积极概率: {sentiment.get('positive_prob'):.4f}")
                
                else:
                    st.error(f"请求失败: {response.status_code}")
                    
            except Exception as e:
                st.error(f"请求出错: {str(e)}")

elif app_mode == "诗人查询":
    st.header("👨‍🎨 诗人查询")
    poet_name = st.text_input("请输入诗人姓名：")
    
    if st.button("查询") and poet_name:
        with st.spinner("正在查询中..."):
            try:
                response = requests.get(f"{API_BASE_URL}/poets/{poet_name}")
                
                if response.status_code == 200:
                    data = response.json()
                    st.subheader(f"👤 {data.get('name', poet_name)}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**朝代**: {data.get('dynasty', '未知')}")
                        st.write(f"**生卒年**: {data.get('lifetime', '未知')}")
                    with col2:
                        st.write(f"**风格**: {data.get('style', '未知')}")
                        st.write(f"**代表作品数**: {data.get('work_count', 0)}")
                    
                    if data.get("bio"):
                        st.subheader("📝 生平简介")
                        st.write(data["bio"])
                        
                    if data.get("works"):
                        st.subheader("📚 代表作品")
                        for work in data["works"]:
                            st.write(f"- {work}")
                else:
                    st.error("未找到相关诗人信息")
            except Exception as e:
                st.error(f"查询出错: {str(e)}")

elif app_mode == "知识图谱":
    st.header("🕸️ 知识图谱")
    
    # 查询输入
    query = st.text_input("请输入要查询的诗人、诗词或主题：")
    
    if st.button("生成知识图谱") and query:
        with st.spinner("正在生成知识图谱..."):
            try:
                # 这里应该调用后端的知识图谱接口
                st.info("知识图谱将在此显示")
                st.warning("此功能需要后端实现支持")
                
                # 示例图谱数据
                import networkx as nx
                import matplotlib.pyplot as plt
                
                # 创建示例图
                G = nx.Graph()
                G.add_node("李白", type="诗人", color="red")
                G.add_node("杜甫", type="诗人", color="red")
                G.add_node("静夜思", type="诗词", color="blue")
                G.add_node("唐代", type="朝代", color="green")
                
                G.add_edge("李白", "静夜思", relation="创作")
                G.add_edge("李白", "唐代", relation="朝代")
                G.add_edge("杜甫", "唐代", relation="朝代")
                
                # 绘制图谱
                fig, ax = plt.subplots(figsize=(10, 6))
                pos = nx.spring_layout(G)
                
                # 绘制节点
                node_colors = [G.nodes[node].get("color", "lightblue") for node in G.nodes()]
                nx.draw(G, pos, with_labels=True, node_color=node_colors, 
                       node_size=1500, font_size=10, font_weight="bold", ax=ax)
                
                # 绘制边标签
                edge_labels = nx.get_edge_attributes(G, 'relation')
                nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=8)
                
                st.pyplot(fig)
                
            except Exception as e:
                st.error(f"生成知识图谱出错: {str(e)}")

elif app_mode == "主题搜索":
    st.header("🔍 主题搜索")
    theme = st.text_input("请输入要搜索的主题（如：思乡、春天、哲理等）：")
    limit = st.slider("返回结果数量", 1, 50, 10)
    
    if st.button("搜索") and theme:
        with st.spinner("正在搜索中..."):
            try:
                response = requests.get(f"{API_BASE_URL}/themes/{theme}?limit={limit}")
                
                if response.status_code == 200:
                    poems = response.json()
                    st.subheader(f"主题 '{theme}' 相关诗词")
                    
                    for poem in poems:
                        with st.expander(f"{poem['title']} - {poem['author']}"):
                            st.write(f"**朝代**: {poem['dynasty']}")
                            st.write(f"**内容**: \n{poem['content']}")
                            if poem.get('translation'):
                                st.write(f"**译文**: \n{poem['translation']}")
                else:
                    st.error("搜索失败")
            except Exception as e:
                st.error(f"搜索出错: {str(e)}")

elif app_mode == "情感搜索":
    st.header("❤️ 情感搜索")
    emotion = st.text_input("请输入要搜索的情感（如：思念、愉悦、豪迈等）：")
    limit = st.slider("返回结果数量", 1, 50, 10)
    
    if st.button("搜索") and emotion:
        with st.spinner("正在搜索中..."):
            try:
                response = requests.get(f"{API_BASE_URL}/emotions/{emotion}?limit={limit}")
                
                if response.status_code == 200:
                    poems = response.json()
                    st.subheader(f"表达 '{emotion}' 情感的诗词")
                    
                    for poem in poems:
                        with st.expander(f"{poem['title']} - {poem['author']}"):
                            st.write(f"**朝代**: {poem['dynasty']}")
                            st.write(f"**内容**: \n{poem['content']}")
                            if poem.get('translation'):
                                st.write(f"**译文**: \n{poem['translation']}")
                else:
                    st.error("搜索失败")
            except Exception as e:
                st.error(f"搜索出错: {str(e)}")

elif app_mode == "情感分析":
    st.header("❤️ 情感分析")
    text = st.text_area("请输入要分析的诗词文本：")
    
    if st.button("分析") and text:
        with st.spinner("正在分析中..."):
            try:
                # 调用后端情感分析接口
                response = requests.post(
                    f"{API_BASE_URL}/sentiment",
                    json={"text": text}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    st.write(f"**情感倾向**: {data.get('sentiment', '未知')}")
                    st.write(f"**积极概率**: {data.get('positive_prob', 0.0):.4f}")
                    st.write(f"**消极概率**: {data.get('negative_prob', 0.0):.4f}")
                    
                    # 显示情感可视化
                    import matplotlib.pyplot as plt
                    import numpy as np
                    
                    # 创建情感分布图
                    emotions = ['积极', '消极']
                    probabilities = [data.get('positive_prob', 0.0), data.get('negative_prob', 0.0)]
                    
                    fig, ax = plt.subplots(figsize=(8, 4))
                    bars = ax.bar(emotions, probabilities, color=['green', 'red'])
                    ax.set_ylabel('概率')
                    ax.set_title('情感分析结果')
                    
                    # 在柱状图上显示数值
                    for bar, prob in zip(bars, probabilities):
                        height = bar.get_height()
                        ax.text(bar.get_x() + bar.get_width()/2., height,
                               f'{prob:.3f}',
                               ha='center', va='bottom')
                    
                    st.pyplot(fig)
                else:
                    st.error("情感分析失败")
            except Exception as e:
                st.error(f"分析出错: {str(e)}")

# 页脚
st.markdown("---")
st.markdown("📜 古诗词RAG系统 | 传承中华文化，品味诗词之美")