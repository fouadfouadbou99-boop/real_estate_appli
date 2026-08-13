Python
1
import streamlit as st
2
import pandas as pd
3
import plotly.express as px
4
 
5
from config import DEFAULTS
6
from debt import debt_schedule
7
from underwriting import build_cashflows
8
from portfolio import portfolio_summary
9
from risk import (
10
risk_score,
11
risk_category
12
)
13
 
14
st.set_page_config(
15
page_title="Real Estate Platform",
16
layout="wide"
17
)
18
 
19
st.title(
20
"🏢 Real Estate Investment Platform"
21
)
22
 
23
purchase_price = st.sidebar.number_input(
24
"Prix acquisition",
25
value=DEFAULTS["purchase_price"]
26
)
27
 
28
ltv = st.sidebar.slider(
29
"LTV",
30
0.0,
31
1.0,
32
DEFAULTS["ltv"]
33
)
34
 
35
loan_amount = purchase_price * ltv
36
 
37
debt_df = debt_schedule(
38
loan_amount,
39
DEFAULTS["debt_rate"],
40
DEFAULTS["debt_term"]
41
)
42
 
43
annuity = debt_df.iloc[0]["Annuity"]
44
 
45
cashflow_df = build_cashflows(
46
DEFAULTS["gross_rent_y1"],
47
DEFAULTS["rent_growth"],
48
DEFAULTS["vacancy_rate"],
49
DEFAULTS["expense_rate"],
50
annuity,
51
DEFAULTS["holding_period"]
52
)
53
 
54
score = risk_score(
55
DEFAULTS["vacancy_rate"],
56
ltv,
57
DEFAULTS["debt_rate"]
58
)
59
 
60
col1, col2, col3 = st.columns(3)
61
 
62
col1.metric(
63
"Risk Score",
64
score
65
)
66
 
67
col2.metric(
68
"Risk Category",
69
risk_category(score)
70
)
71
 
72
col3.metric(
73
"Loan Amount",
74
f"{loan_amount:,.0f}"
75
)
76
 
77
st.subheader(
78
"Cash Flows"
79
)
80
 
81
fig = px.bar(
82
cashflow_df,
83
x="Year",
84
y="CF Equity"
85
)
86
 
87
st.plotly_chart(
88
fig,
89
use_container_width=True
90
)
91
 
92
st.subheader(
93
"Debt Schedule"
94
)
95
 
96
st.dataframe(
97
debt_df,
98
use_container_width=True
99
)
100
 
101
st.subheader(
102
"Portfolio"
103
)
104
 
105
st.dataframe(
106
portfolio_summary(),
107
use_container_width=True
108
)
