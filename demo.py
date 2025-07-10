import streamlit as st

st.markdown("""
<style>
.hacker-box {
    padding: 0.5rem 0.75rem;
    border-radius: 6px;
    background-color: #f9f9f9;
    border: 1px solid #ccc;
    color: #333;
    font-size: 0.85rem;
    line-height: 1.2;
    margin: 0.5rem 0 1rem 0;
    max-width: 600px;
    font-family: Arial, sans-serif;
}
.hacker-title {
    font-weight: 600;
    margin-bottom: 0.3rem;
    font-size: 1rem;
    color: #222;
}
.value {
    font-family: monospace;
    background-color: #eee;
    padding: 2px 6px;
    border-radius: 3px;
    display: inline-block;
    margin-left: 0.3rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hacker-box">
    <div class="hacker-title">Hacker's View</div>
    Hacker has info about:<br><br>
    <b>Encrypted AES Key:</b><span class="value">013361271020108101015</span><br>
    <b>Value of N (RSA modulus):</b><span class="value">21</span><br>
    <b>Cipher Text:</b><span class="value">0f15322e0e0b465f0e5195d6c9e7c102</span>
</div>
""", unsafe_allow_html=True)


dot = """
digraph {
    rankdir=LR;
    node [shape=box, style=filled, fillcolor=lightgray, fontname=Arial, fontsize=12];
    
    GuessFactor [label="Guess taken: 6", shape=box, fillcolor="#d3d3d3"];
}
"""

st.title("Shor's Algorithm")
st.markdown("**Step 1:** Take a guess a number that shares a factor with 21.")
st.graphviz_chart(dot)

st.markdown("### Step 2: Finding a special multiple 'P' ")

st.write("""
We want to find numbers **p** and **m** such that:

> p × 6 = m × 21 + 1

$6^{p}-1 = m \\times 21$

$(6^{p/2} - 1)(6^{p/2} + 1) = m \\times 21$
""")

