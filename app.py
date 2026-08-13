import streamlit as st
2
import plotly.express as px
3
 
4
from config import DEFAULTS
5
 
6
from debt import debt_schedule
7
from underwriting import build_cashflows
8
from valuation import add_exit_to_cashflows, valuation_summary
9
from metrics import kpi_summary
10
from risk import risk_score, risk_category
11
from portfolio import portfolio_summary
12
from montecarlo import run_monte_carlo, monte_carlo_summary
13
 
14
# =====================================================
15
# CONFIGURATION
16
# =====================================================
17
 
18
st.set_page_config(
19
page_title="Real Estate Investment Platform",
20
page_icon="🏢",
21
layout="wide"
22
)
23
 
24
st.title("🏢 Real Estate Investment Platform")
25
 
26
# =====================================================
27
# SIDEBAR
28
# =====================================================
29
 
30
st.sidebar.header("Hypothèses")
31
 
32
purchase_price = st.sidebar.number_input(
33
"Prix acquisition",
34
value=float(DEFAULTS["purchase_price"])
35
)
36
 
37
acquisition_fee_rate = (
38
st.sidebar.number_input(
39
"Frais acquisition (%)",
40
value=float(DEFAULTS["acquisition_fee_rate"] * 100)
41
) / 100
42
)
43
 
44
capex = st.sidebar.number_input(
45
"Travaux",
46
value=float(DEFAULTS["capex"])
47
)
48
 
49
gross_rent_y1 = st.sidebar.number_input(
50
"Loyer brut Année 1",
51
value=float(DEFAULTS["gross_rent_y1"])
52
)
53
 
54
rent_growth = (
55
st.sidebar.number_input(
56
"Croissance loyers (%)",
57
value=float(DEFAULTS["rent_growth"] * 100)
58
) / 100
59
)
60
 
61
vacancy_rate = (
62
st.sidebar.number_input(
63
"Vacance (%)",
64
value=float(DEFAULTS["vacancy_rate"] * 100)
65
) / 100
66
)
67
 
68
expense_rate = (
69
st.sidebar.number_input(
70
"Charges (%)",
71
value=float(DEFAULTS["expense_rate"] * 100)
72
) / 100
73
)
74
 
75
# =====================================================
76
# FINANCEMENT
77
# =====================================================
78
 
79
st.sidebar.header("Dette")
80
 
81
ltv = (
82
st.sidebar.number_input(
83
"LTV (%)",
84
value=float(DEFAULTS["ltv"] * 100)
85
) / 100
86
)
87
 
88
debt_rate = (
89
st.sidebar.number_input(
90
"Taux dette (%)",
91
value=float(DEFAULTS["debt_rate"] * 100)
92
) / 100
93
)
94
 
95
debt_term = int(
96
st.sidebar.number_input(
97
"Durée dette",
98
value=int(DEFAULTS["debt_term"])
99
)
100
)
101
 
102
# =====================================================
103
# SORTIE
104
# =====================================================
105
 
106
st.sidebar.header("Sortie")
107
 
108
holding_period = int(
109
st.sidebar.number_input(
110
"Horizon",
111
value=int(DEFAULTS["holding_period"])
112
)
113
)
114
 
115
exit_cap_rate = (
116
st.sidebar.number_input(
117
"Exit Cap Rate (%)",
118
value=float(DEFAULTS["exit_cap_rate"] * 100)
119
) / 100
120
)
121
 
122
sale_cost_rate = (
123
st.sidebar.number_input(
124
"Frais cession (%)",
125
value=float(DEFAULTS["sale_cost_rate"] * 100)
126
) / 100
127
)
128
 
129
discount_rate = (
130
st.sidebar.number_input(
131
"Taux actualisation (%)",
132
value=float(DEFAULTS["discount_rate"] * 100)
133
) / 100
134
)
135
 
136
# =====================================================
137
# CHARGES DETAILLEES
138
# =====================================================
139
 
140
taxe_fonciere = float(DEFAULTS["taxe_fonciere"])
141
assurance = float(DEFAULTS["assurance"])
142
maintenance = float(DEFAULTS["maintenance"])
143
gestion_locative = float(DEFAULTS["gestion_locative"])
144
inflation = float(DEFAULTS["inflation_rate"])
145
 
146
# =====================================================
147
# INVESTISSEMENT
148
# =====================================================
149
 
150
acquisition_fees = (
151
purchase_price * acquisition_fee_rate
152
)
153
 
154
total_investment = (
155
purchase_price +
156
acquisition_fees +
157
capex
158
)
159
 
160
loan_amount = (
161
total_investment * ltv
162
)
163
 
164
equity_investment = (
165
total_investment -
166
loan_amount
167
)
168
 
169
# =====================================================
170
# DETTE
171
# =====================================================
172
 
173
debt_df = debt_schedule(
174
loan_amount=loan_amount,
175
interest_rate=debt_rate,
176
term=debt_term
177
)
178
 
179
annual_debt_service = float(
180
debt_df.iloc[0]["Annuity"]
181
)
182
 
183
# =====================================================
184
# CASH FLOWS
185
# =====================================================
186
 
187
cashflows_df = build_cashflows(
188
rent_y1=gross_rent_y1,
189
growth=rent_growth,
190
vacancy=vacancy_rate,
191
expense_rate=expense_rate,
192
debt_service=annual_debt_service,
193
holding_period=holding_period,
194
taxe_fonciere=taxe_fonciere,
195
assurance=assurance,
196
maintenance=maintenance,
197
gestion_locative=gestion_locative,
198
inflation=inflation
199
)
200
 
201
cashflows_df = add_exit_to_cashflows(
202
cashflows_df,
203
debt_df,
204
exit_cap_rate,
205
sale_cost_rate
206
)
207
 
208
# =====================================================
209
# KPI
210
# =====================================================
211
 
212
kpis = kpi_summary(
213
equity_investment=equity_investment,
214
loan_amount=loan_amount,
215
total_investment=total_investment,
216
discount_rate=discount_rate,
217
cashflows_df=cashflows_df
218
)
219
 
220
# =====================================================
221
# RISQUE
222
# =====================================================
223
 
224
risk = risk_score(
225
vacancy_rate,
226
ltv,
227
debt_rate
228
)
229
 
230
# =====================================================
231
# TABLEAU DE BORD
232
# =====================================================
233
 
234
st.subheader("📊 KPI")
235
 
236
col1, col2, col3, col4 = st.columns(4)
237
 
238
col1.metric(
239
"IRR",
240
f"{kpis['IRR']} %"
241
)
242
 
243
col2.metric(
244
"NPV",
245
f"{kpis['NPV']:,.0f}"
246
)
247
 
248
col3.metric(
249
"DSCR",
250
f"{kpis['DSCR']}"
251
)
252
 
253
col4.metric(
254
"Equity Multiple",
255
f"{kpis['Equity Multiple']}x"
256
)
257
 
258
# =====================================================
259
# ONGLETS
260
# =====================================================
261
 
262
tab1, tab2, tab3, tab4, tab5 = st.tabs(
263
[
264
"Cash-Flows",
265
"Dette
