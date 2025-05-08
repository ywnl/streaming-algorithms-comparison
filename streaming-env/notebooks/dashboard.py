import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Streaming Algo Dashboard", layout="wide")

# --- Load Data ---
benchmark_df = pd.read_csv("../results/benchmark_multi_dist.csv")
real_df = pd.read_csv("../results/sales_approx.csv")

# Sidebar Filters
st.sidebar.title("🔎 Filter Options")
view = st.sidebar.selectbox("Dataset View", ["Synthetic", "Real-World"])

# --- Title ---
st.title("Streaming Frequency Estimation Algorithms Dashboard")

if view == "Synthetic":
    stream_lengths = benchmark_df["StreamLength"].unique()
    selected_length = st.sidebar.selectbox(
        "Select Stream Length(s)",
        options=stream_lengths
    )
    selected_alg = st.sidebar.multiselect( "Select Algorithm", benchmark_df["Algorithm"].unique(), default = benchmark_df["Algorithm"].unique())
    dist = st.sidebar.multiselect("Select Distributions", benchmark_df["Distribution"].unique(), default=["uniform"])
    memory_range = st.sidebar.slider("Memory Size", int(benchmark_df["MemorySize"].min()), int(benchmark_df["MemorySize"].max()), (20, 100))

    filtered = benchmark_df[
        (benchmark_df["Distribution"].isin(dist)) &
        (benchmark_df["MemorySize"].between(*memory_range)) &
        (benchmark_df["StreamLength"] == selected_length) &
        (benchmark_df["Algorithm"].isin(selected_alg))
    ]

    tab1, tab2, tab3 = st.tabs(["Mean Absolute Error", "F1@10 Score", "Runtime"])
    
    with tab1:
        fig = px.line(filtered, x="MemorySize", y="MeanAbsError", color="Algorithm", line_dash="Distribution", markers=True)
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        fig = px.line(filtered, x="MemorySize", y="F1@10", color="Algorithm", line_dash="Distribution", markers=True)
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        fig = px.line(filtered, x="MemorySize", y="Runtime", color="Algorithm", line_dash="Distribution", markers=True)
        st.plotly_chart(fig, use_container_width=True)

# --- Real View ---
else:
    st.subheader("Real-World Dataset (Amazon Sales)")
    # memory_range = st.sidebar.slider("Memory Size", int(benchmark_df["MemorySize"].min()), int(benchmark_df["MemorySize"].max()), (20, 100))
    metric = st.selectbox("Metric", ["MeanAbsError", "MeanRelError", "F1@10", "Runtime"])
    if metric == "Runtime":
        memory_range = st.sidebar.slider("Memory Size", int(real_df["MemorySize"].min()), int(real_df["MemorySize"].max()), (20, 100))
        filtered = real_df[
            real_df["MemorySize"].between(*memory_range)
        ]
        fig = px.line(filtered, x="MemorySize", y="Runtime", color="Algorithm", markers=True)
        st.plotly_chart(fig, use_container_width=True)        
        
    else:
        # memory_size = st.sidebar.selectbox("Memory Size", real_df["MemorySize"].unique())
        # filtered = real_df[
        #     (real_df["MemorySize"]== memory_size)
        # ]
        # fig = px.bar(filtered, x="Algorithm", y=metric,title=f"{metric} by Algorithm")
        fig = px.histogram(real_df, x="Algorithm", y=metric,color='MemorySize', barmode='group', title=f"{metric} by Algorithm")
        fig.update_layout(yaxis_tickformat=".2f")
        st.plotly_chart(fig, use_container_width=True)
