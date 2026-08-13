# =====================================================
# REAL ESTATE INVESTMENT PLATFORM
# app.py
# =====================================================

import streamlit as st
import plotly.express as px

from config import DEFAULTS

from debt import debt_schedule
from underwriting import build_cashflows
from valuation import add_exit_to_cashflows, valuation_summary
from metrics import kpi_summary
from risk import risk_score, risk_category
from portfolio import portfolio_summary
from montecarlo import run_monte_carlo, monte_carlo_summary

# =====================================================
# CONFIGURATION PAGE
# =====================================================

st.set_page_config(
    page_title="Real Estate Investment Platform",
    page_icon="🏢",
    layout="wide"
)

st.title("🏢 Real Estate Investment Platform")

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.header("Hypothèses")

purchase_price = st.sidebar.number_input(
    "Prix acquisition",
    value=float(DEFAULTS["purchase_price"])
)

acquisition_fee_rate = st.sidebar.number_input(
    "Frais acquisition (%)",
    value=float(DEFAULTS["acquisition_fee_rate"] * 100)
) / 100

capex = st.sidebar.number_input(
    "Travaux",
    value=float(DEFAULTS["capex"])
)

gross_rent_y1 = st.sidebar.number_input(
    "Loyer brut Année 1",
    value=float(DEFAULTS["gross_rent_y1"])
)

rent_growth = st.sidebar.number_input(
    "Croissance loyers (%)",
    value=float(DEFAULTS["rent_growth"] * 100)
) / 100

vacancy_rate = st.sidebar.number_input(
    "Vacance (%)",
    value=float(DEFAULTS["vacancy_rate"] * 100)
) / 100

expense_rate = st.sidebar.number_input(
    "Charges (%)",
    value=float(DEFAULTS["expense_rate"] * 100)
) / 100

# =====================================================
# DETTE
# =====================================================

st.sidebar.header("Financement")

ltv = st.sidebar.number_input(
    "LTV (%)",
    value=float(DEFAULTS["ltv"] * 100)
) / 100

debt_rate = st.sidebar.number_input(
    "Taux dette (%)",
    value=float(DEFAULTS["debt_rate"] * 100)
) / 100

debt_term = int(
    st.sidebar.number_input(
        "Durée dette",
        value=int(DEFAULTS["debt_term"])
    )
)

# =====================================================
# SORTIE
# =====================================================

st.sidebar.header("Sortie")

holding_period = int(
    st.sidebar.number_input(
        "Horizon",
        value=int(DEFAULTS["holding_period"])
    )
)

exit_cap_rate = st.sidebar.number_input(
    "Exit Cap Rate (%)",
    value=float(DEFAULTS["exit_cap_rate"] * 100)
) / 100

sale_cost_rate = st.sidebar.number_input(
    "Frais cession (%)",
    value=float(DEFAULTS["sale_cost_rate"] * 100)
) / 100

discount_rate = st.sidebar.number_input(
    "Taux actualisation (%)",
    value=float(DEFAULTS["discount_rate"] * 100)
) / 100

# =====================================================
# CHARGES DETAILLEES
# =====================================================

st.sidebar.header("Charges détaillées")

taxe_fonciere = float(DEFAULTS["taxe_fonciere"])
assurance = float(DEFAULTS["assurance"])
maintenance = float(DEFAULTS["maintenance"])
gestion_locative = float(DEFAULTS["gestion_locative"])
inflation = float(DEFAULTS["inflation_rate"])

# =====================================================
# INVESTISSEMENT
# =====================================================

acquisition_fees = (
    purchase_price *
    acquisition_fee_rate
)

total_investment = (
    purchase_price
    + acquisition_fees
    + capex
)

loan_amount = (
    total_investment * ltv
)

equity_investment = (
    total_investment - loan_amount
)

# =====================================================
# DETTE
# =====================================================

debt_df = debt_schedule(
    loan_amount,
    debt_rate,
    debt_term
)

annual_debt_service = (
    debt_df.iloc[0]["Annuity"]
)

# =====================================================
# CASH FLOWS
# =====================================================

cashflows_df = build_cashflows(
    rent_y1=gross_rent_y1,
    growth=rent_growth,
    vacancy=vacancy_rate,
    expense_rate=expense_rate,
    debt_service=annual_debt_service,
    holding_period=holding_period,
    taxe_fonciere=taxe_fonciere,
    assurance=assurance,
    maintenance=maintenance,
    gestion_locative=gestion_locative,
    inflation=inflation
)

cashflows_df = add_exit_to_cashflows(
    cashflows_df,
    debt_df,
    exit_cap_rate,
    sale_cost_rate
)

# =====================================================
# KPI
# =====================================================

kpis = kpi_summary(
    equity_investment=equity_investment,
    loan_amount=loan_amount,
    total_investment=total_investment,
    discount_rate=discount_rate,
    cashflows_df=cashflows_df
)

# =====================================================
# RISQUE
# =====================================================

risk = risk_score(
    vacancy_rate,
    ltv,
    debt_rate
)

# =====================================================
220
# KPI DASHBOARD
221
# =====================================================
222
 
223
st.subheader("KPI")
224
 
225
c1, c2, c3, c4 = st.columns(4)
226
 
227
c1.metric(
228
"IRR",
229
f"{kpis['IRR']} %"
230
)
231
 
232
c2.metric(
233
"NPV",
234
f"{kpis['NPV']:,.0f}"
235
)
236
 
237
c3.metric(
238
"DSCR",
239
f"{kpis['DSCR']}"
240
)
241
 
242
c4.metric(
243
"Equity Multiple",
244
f"{kpis['Equity Multiple']}x"
245
)
246
 
247
# =====================================================
248
# ONGLETS
249
# =====================================================
250
 
251
tab1, tab2, tab3, tab4, tab5 = st.tabs([
252
"Cash-Flows",
253
"Dette",
254
"Valorisation",
255
"Monte Carlo",
256
"Portefeuille"
257
])
258
 
259
# =====================================================
260
# CASH FLOWS
261
# =====================================================
262
 
263
with tab1:
264
 
265
st.dataframe(
266
cashflows_df,
267
use_container_width=True
268
)
269
 
270
fig = px.bar(
271
cashflows_df,
272
x="Year",
273
y="CF Equity",
274
title="Cash Flows Equity"
275
)
276
 
277
st.plotly_chart(
278
fig,
279
use_container_width=True
280
)
281
 
282
# =====================================================
283
# DETTE
284
# =====================================================
285
 
286
with tab2:
287
 
288
st.dataframe(
289
debt_df,
290
use_container_width=True
291
)
292
 
293
# =====================================================
294
# VALORISATION
295
# =====================================================
296
 
297
with tab3:
298
 
299
terminal_noi = float(
300
cashflows_df.iloc[-1]["NOI"]
301
)
302
 
303
remaining_debt = float(
304
debt_df.iloc[-1]["Closing Balance"]
305
)
306
 
307
val = valuation_summary(
308
terminal_noi,
309
exit_cap_rate,
310
sale_cost_rate,
311
remaining_debt
312
)
313
 
314
st.json(val)
315
 
316
# =====================================================
317
# MONTE CARLO
318
# =====================================================
319
 
320
with tab4:
321
 
322
simulations = st.slider(
323
"Nombre simulations",
324
100,
325
5000,
326
1000
327
)
328
 
329
mc_df = run_monte_carlo(
330
simulations=simulations,
331
equity_investment=equity_investment,
332
debt_df=debt_df,
333
base_rent=gross_rent_y1,
334
growth_mean=rent_growth,
335
growth_std=0.01,
336
vacancy_mean=vacancy_rate,
337
vacancy_std=0.02,
338
expense_rate=expense_rate,
339
debt_service=annual_debt_service,
340
holding_period=holding_period,
341
taxe_fonciere=taxe_fonciere,
342
assurance=assurance,
343
maintenance=maintenance,
344
gestion_locative=gestion_locative,
345
inflation=inflation,
346
exit_cap_rate=exit_cap_rate,
347
sale_cost_rate=sale_cost_rate
348
)
349
 
350
st.json(
351
monte_carlo_summary(mc_df)
352
)
353
 
354
fig_mc = px.histogram(
355
mc_df,
356
x="IRR",
357
nbins=30,
358
title="Distribution des TRI"
359
)
360
 
361
st.plotly_chart(
362
fig_mc,
363
use_container_width=True
364
)
365
 
366
# =====================================================
367
# PORTEFEUILLE
368
# =====================================================
369
 
370
with tab5:
371
 
372
portfolio_df = portfolio_summary()
373
 
374
st.dataframe(
375
portfolio_df,
376
use_container_width=True
377
)
378
 
379
# =====================================================
380
# FIN
381
# =====================================================
382
 
383
st.markdown("---")
384
st.caption(
385
"Real Estate Investment Platform - Version 1.0"
386
)
