import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Child Processing Pipeline Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.main {
    padding-top: 1rem;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1500px;
}

/* Main title */
.dashboard-title {
    font-size: 42px;
    font-weight: 700;
    margin-bottom: 5px;
}

.dashboard-subtitle {
    font-size: 17px;
    opacity: 0.75;
    margin-bottom: 25px;
}

/* KPI cards */
.kpi-card {
    padding: 20px;
    border-radius: 14px;
    border: 1px solid rgba(128,128,128,0.25);
    background: rgba(128,128,128,0.06);
    min-height: 125px;
}

.kpi-label {
    font-size: 14px;
    opacity: 0.7;
    margin-bottom: 8px;
}

.kpi-value {
    font-size: 30px;
    font-weight: 700;
}

/* Section headers */
.section-title {
    font-size: 25px;
    font-weight: 650;
    margin-top: 25px;
    margin-bottom: 10px;
}

/* Insight cards */
.insight-card {
    padding: 18px;
    border-radius: 12px;
    border: 1px solid rgba(128,128,128,0.25);
    background: rgba(128,128,128,0.05);
    margin-bottom: 10px;
}

.insight-title {
    font-size: 17px;
    font-weight: 650;
}

.insight-text {
    font-size: 14px;
    opacity: 0.85;
}

/* Footer */
.footer {
    text-align: center;
    opacity: 0.6;
    font-size: 13px;
    padding-top: 25px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    data = pd.read_csv("cleaned_dataset.csv")

    data["Date"] = pd.to_datetime(data["Date"])

    data = data.sort_values("Date").reset_index(drop=True)

    return data


df = load_data()


# ============================================================
# COLUMN NAMES
# ============================================================

APP = "Children apprehended and placed in CBP custody*"
TRANSFER = "Children transferred out of CBP custody"
DISCHARGE = "Children discharged from HHS Care"
CBP_CUSTODY = "Children in CBP custody"
HHS_CARE = "Children in HHS Care"


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("📊 Dashboard")

    st.markdown("---")

    st.subheader("📅 Analysis Period")

    min_date = df["Date"].min().date()
    max_date = df["Date"].max().date()

    selected_dates = st.date_input(
        "Select date range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    st.markdown("---")

    st.subheader("ℹ️ About")

    st.write(
        """
        This dashboard analyzes the movement of children through
        the CBP and HHS processing pipeline.

        It focuses on:

        • Apprehensions  
        • CBP transfers  
        • HHS discharges  
        • Custody levels  
        • Flow pressure  
        • Operational stability
        """
    )

    st.markdown("---")

    st.caption(
        "Internship Data Analytics Project"
    )


# ============================================================
# DATE FILTER
# ============================================================

if len(selected_dates) != 2:

    st.warning("Please select both a start date and an end date.")

    st.stop()


start_date = pd.to_datetime(selected_dates[0])
end_date = pd.to_datetime(selected_dates[1])

filtered_df = df[
    (df["Date"] >= start_date) &
    (df["Date"] <= end_date)
].copy()


if filtered_df.empty:

    st.error("No data available for the selected period.")

    st.stop()


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="dashboard-title">📊 Child Processing Pipeline Analytics</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="dashboard-subtitle">'
    'CBP → HHS Flow, Capacity & Operational Pressure Dashboard'
    '</div>',
    unsafe_allow_html=True
)

st.info(
    f"📅 **Selected period:** "
    f"{start_date.strftime('%d %B %Y')} → "
    f"{end_date.strftime('%d %B %Y')} "
    f"| **{len(filtered_df):,} daily records**"
)


# ============================================================
# BASIC KPI CALCULATIONS
# ============================================================

total_apprehensions = filtered_df[APP].sum()
total_transfers = filtered_df[TRANSFER].sum()
total_discharges = filtered_df[DISCHARGE].sum()

avg_cbp_custody = filtered_df[CBP_CUSTODY].mean()
avg_hhs_care = filtered_df[HHS_CARE].mean()

max_cbp_custody = filtered_df[CBP_CUSTODY].max()
max_hhs_care = filtered_df[HHS_CARE].max()


# ============================================================
# TOP KPI CARDS
# ============================================================

st.markdown(
    '<div class="section-title">📌 Executive KPIs</div>',
    unsafe_allow_html=True
)

k1, k2, k3, k4, k5 = st.columns(5)


def kpi_card(column, label, value):

    with column:

        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{value}</div>
            </div>
            """,
            unsafe_allow_html=True
        )


kpi_card(
    k1,
    "Total Apprehensions",
    f"{total_apprehensions:,.0f}"
)

kpi_card(
    k2,
    "Total CBP Transfers",
    f"{total_transfers:,.0f}"
)

kpi_card(
    k3,
    "Total HHS Discharges",
    f"{total_discharges:,.0f}"
)

kpi_card(
    k4,
    "Average CBP Custody",
    f"{avg_cbp_custody:,.0f}"
)

kpi_card(
    k5,
    "Average HHS Care",
    f"{avg_hhs_care:,.0f}"
)


# ============================================================
# MONTHLY DATA
# ============================================================

monthly = filtered_df.copy()

monthly["Month"] = (
    monthly["Date"]
    .dt.to_period("M")
    .astype(str)
)

monthly_data = (
    monthly
    .groupby("Month")
    .agg({
        APP: "sum",
        TRANSFER: "sum",
        DISCHARGE: "sum",
        CBP_CUSTODY: "mean",
        HHS_CARE: "mean"
    })
    .reset_index()
)


# ============================================================
# PERFORMANCE RATIOS
# ============================================================

transfer_efficiency = (
    total_transfers / total_apprehensions
    if total_apprehensions != 0
    else 0
)

discharge_effectiveness = (
    total_discharges / total_transfers
    if total_transfers != 0
    else 0
)

pipeline_throughput = (
    total_discharges / total_apprehensions
    if total_apprehensions != 0
    else 0
)


# ============================================================
# PERFORMANCE KPI SECTION
# ============================================================

st.markdown(
    '<div class="section-title">⚙️ Pipeline Performance</div>',
    unsafe_allow_html=True
)

p1, p2, p3 = st.columns(3)

kpi_card(
    p1,
    "Transfer Efficiency Ratio",
    f"{transfer_efficiency:.2f}"
)

kpi_card(
    p2,
    "Discharge Effectiveness",
    f"{discharge_effectiveness:.2f}"
)

kpi_card(
    p3,
    "Pipeline Throughput",
    f"{pipeline_throughput:.2f}"
)

st.caption(
    "Ratios are calculated from aggregate activity during the selected period."
)


# ============================================================
# MONTHLY KPI CALCULATIONS
# ============================================================

monthly_kpi = monthly_data.copy()

monthly_kpi["Transfer Efficiency"] = (
    monthly_kpi[TRANSFER] /
    monthly_kpi[APP].replace(0, np.nan)
)

monthly_kpi["Discharge Effectiveness"] = (
    monthly_kpi[DISCHARGE] /
    monthly_kpi[TRANSFER].replace(0, np.nan)
)

monthly_kpi["Pipeline Throughput"] = (
    monthly_kpi[DISCHARGE] /
    monthly_kpi[APP].replace(0, np.nan)
)


# ============================================================
# MONTHLY PERFORMANCE CHART
# ============================================================

st.markdown(
    '<div class="section-title">📈 Monthly Performance</div>',
    unsafe_allow_html=True
)

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=monthly_kpi["Month"],
        y=monthly_kpi["Transfer Efficiency"],
        mode="lines+markers",
        name="Transfer Efficiency"
    )
)

fig.add_trace(
    go.Scatter(
        x=monthly_kpi["Month"],
        y=monthly_kpi["Discharge Effectiveness"],
        mode="lines+markers",
        name="Discharge Effectiveness"
    )
)

fig.add_trace(
    go.Scatter(
        x=monthly_kpi["Month"],
        y=monthly_kpi["Pipeline Throughput"],
        mode="lines+markers",
        name="Pipeline Throughput"
    )
)

fig.update_layout(
    height=450,
    hovermode="x unified",
    xaxis_title="Month",
    yaxis_title="Ratio",
    legend_title="Metric"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# FLOW ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-title">🔄 Care Pipeline Flow</div>',
    unsafe_allow_html=True
)

flow_fig = go.Figure()

flow_fig.add_trace(
    go.Scatter(
        x=monthly_data["Month"],
        y=monthly_data[APP],
        mode="lines+markers",
        name="Apprehensions"
    )
)

flow_fig.add_trace(
    go.Scatter(
        x=monthly_data["Month"],
        y=monthly_data[TRANSFER],
        mode="lines+markers",
        name="Transfers"
    )
)

flow_fig.add_trace(
    go.Scatter(
        x=monthly_data["Month"],
        y=monthly_data[DISCHARGE],
        mode="lines+markers",
        name="Discharges"
    )
)

flow_fig.update_layout(
    height=500,
    hovermode="x unified",
    xaxis_title="Month",
    yaxis_title="Children",
    legend_title="Pipeline Stage"
)

st.plotly_chart(
    flow_fig,
    use_container_width=True
)


# ============================================================
# CARE POPULATION
# ============================================================

st.markdown(
    '<div class="section-title">👥 Active Care Population</div>',
    unsafe_allow_html=True
)

care_fig = go.Figure()

care_fig.add_trace(
    go.Scatter(
        x=monthly_data["Month"],
        y=monthly_data[CBP_CUSTODY],
        mode="lines+markers",
        name="CBP Custody"
    )
)

care_fig.add_trace(
    go.Scatter(
        x=monthly_data["Month"],
        y=monthly_data[HHS_CARE],
        mode="lines+markers",
        name="HHS Care"
    )
)

care_fig.update_layout(
    height=450,
    hovermode="x unified",
    xaxis_title="Month",
    yaxis_title="Average Children",
    legend_title="Care Population"
)

st.plotly_chart(
    care_fig,
    use_container_width=True
)


# ============================================================
# PRESSURE ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-title">🚨 Pressure & Bottleneck Analysis</div>',
    unsafe_allow_html=True
)

pressure_df = filtered_df.copy()

pressure_df["CBP Backlog Pressure"] = (
    pressure_df[APP] -
    pressure_df[TRANSFER]
)

pressure_df["HHS Backlog Pressure"] = (
    pressure_df[TRANSFER] -
    pressure_df[DISCHARGE]
)

pressure_df["CBP Pressure 7D Avg"] = (
    pressure_df["CBP Backlog Pressure"]
    .rolling(7)
    .mean()
)

pressure_df["HHS Pressure 7D Avg"] = (
    pressure_df["HHS Backlog Pressure"]
    .rolling(7)
    .mean()
)

pressure_df["CBP Bottleneck Alert"] = (
    pressure_df["CBP Pressure 7D Avg"] > 0
)

pressure_df["HHS Bottleneck Alert"] = (
    pressure_df["HHS Pressure 7D Avg"] > 0
)

cbp_bottleneck_days = int(
    pressure_df["CBP Bottleneck Alert"].sum()
)

hhs_bottleneck_days = int(
    pressure_df["HHS Bottleneck Alert"].sum()
)


# ============================================================
# PRESSURE KPIs
# ============================================================

b1, b2, b3, b4 = st.columns(4)

kpi_card(
    b1,
    "CBP Bottleneck Days",
    f"{cbp_bottleneck_days:,}"
)

kpi_card(
    b2,
    "HHS Bottleneck Days",
    f"{hhs_bottleneck_days:,}"
)

kpi_card(
    b3,
    "Peak CBP Custody",
    f"{max_cbp_custody:,.0f}"
)

kpi_card(
    b4,
    "Peak HHS Care",
    f"{max_hhs_care:,.0f}"
)


# ============================================================
# DAILY PRESSURE CHART
# ============================================================

pressure_fig = go.Figure()

pressure_fig.add_trace(
    go.Scatter(
        x=pressure_df["Date"],
        y=pressure_df["CBP Backlog Pressure"],
        mode="lines",
        name="CBP Pressure"
    )
)

pressure_fig.add_trace(
    go.Scatter(
        x=pressure_df["Date"],
        y=pressure_df["HHS Backlog Pressure"],
        mode="lines",
        name="HHS Pressure"
    )

)

pressure_fig.add_hline(
    y=0,
    line_dash="dash"
)

pressure_fig.update_layout(
    height=450,
    hovermode="x unified",
    xaxis_title="Date",
    yaxis_title="Pressure",
    legend_title="Pressure Indicator"
)

st.plotly_chart(
    pressure_fig,
    use_container_width=True
)


# ============================================================
# SUSTAINED PRESSURE
# ============================================================

st.markdown("### 📉 Sustained Pressure — 7-Day Average")

rolling_fig = go.Figure()

rolling_fig.add_trace(
    go.Scatter(
        x=pressure_df["Date"],
        y=pressure_df["CBP Pressure 7D Avg"],
        mode="lines",
        name="CBP 7-Day Pressure"
    )
)

rolling_fig.add_trace(
    go.Scatter(
        x=pressure_df["Date"],
        y=pressure_df["HHS Pressure 7D Avg"],
        mode="lines",
        name="HHS 7-Day Pressure"
    )
)

rolling_fig.add_hline(
    y=0,
    line_dash="dash"
)

rolling_fig.update_layout(
    height=450,
    hovermode="x unified",
    xaxis_title="Date",
    yaxis_title="7-Day Average Pressure"
)

st.plotly_chart(
    rolling_fig,
    use_container_width=True
)


# ============================================================
# DISCHARGE STABILITY
# ============================================================

st.markdown(
    '<div class="section-title">📉 Discharge Stability</div>',
    unsafe_allow_html=True
)

discharge_mean = filtered_df[DISCHARGE].mean()
discharge_std = filtered_df[DISCHARGE].std()
discharge_median = filtered_df[DISCHARGE].median()

discharge_min = filtered_df[DISCHARGE].min()
discharge_max = filtered_df[DISCHARGE].max()

discharge_cv = (
    discharge_std / discharge_mean
    if discharge_mean != 0
    else 0
)

s1, s2, s3, s4 = st.columns(4)

kpi_card(
    s1,
    "Mean Discharges",
    f"{discharge_mean:,.1f}"
)

kpi_card(
    s2,
    "Median Discharges",
    f"{discharge_median:,.1f}"
)

kpi_card(
    s3,
    "Discharge CV",
    f"{discharge_cv * 100:.1f}%"
)

kpi_card(
    s4,
    "Maximum Daily Discharges",
    f"{discharge_max:,.0f}"
)

st.caption(
    "Coefficient of Variation (CV) measures relative variability. "
    "Higher values indicate less stable daily discharge activity."
)


# ============================================================
# EXTREME VALUES
# ============================================================

st.markdown(
    '<div class="section-title">🏆 Operational Extremes</div>',
    unsafe_allow_html=True
)

highest_cbp = filtered_df.loc[
    filtered_df[CBP_CUSTODY].idxmax()
]

lowest_cbp = filtered_df.loc[
    filtered_df[CBP_CUSTODY].idxmin()
]

highest_hhs = filtered_df.loc[
    filtered_df[HHS_CARE].idxmax()
]

lowest_hhs = filtered_df.loc[
    filtered_df[HHS_CARE].idxmin()
]

e1, e2 = st.columns(2)

with e1:

    st.markdown("#### 🏢 CBP Custody")

    st.write(
        f"**Highest:** {highest_cbp[CBP_CUSTODY]:,.0f} "
        f"on {highest_cbp['Date'].strftime('%d %B %Y')}"
    )

    st.write(
        f"**Lowest:** {lowest_cbp[CBP_CUSTODY]:,.0f} "
        f"on {lowest_cbp['Date'].strftime('%d %B %Y')}"
    )

with e2:

    st.markdown("#### 🏠 HHS Care")

    st.write(
        f"**Highest:** {highest_hhs[HHS_CARE]:,.0f} "
        f"on {highest_hhs['Date'].strftime('%d %B %Y')}"
    )

    st.write(
        f"**Lowest:** {lowest_hhs[HHS_CARE]:,.0f} "
        f"on {lowest_hhs['Date'].strftime('%d %B %Y')}"
    )


# ============================================================
# MONTHLY EXTREMES
# ============================================================

st.markdown(
    '<div class="section-title">📅 Monthly Flow Extremes</div>',
    unsafe_allow_html=True
)

extreme_rows = []

metrics = [
    (APP, "Highest Monthly Apprehensions", "max"),
    (APP, "Lowest Monthly Apprehensions", "min"),
    (TRANSFER, "Highest Monthly Transfers", "max"),
    (TRANSFER, "Lowest Monthly Transfers", "min"),
    (DISCHARGE, "Highest Monthly Discharges", "max"),
    (DISCHARGE, "Lowest Monthly Discharges", "min")
]

for column, label, operation in metrics:

    if operation == "max":
        row = monthly_data.loc[
            monthly_data[column].idxmax()
        ]
    else:
        row = monthly_data.loc[
            monthly_data[column].idxmin()
        ]

    extreme_rows.append({
        "Metric": label,
        "Month": row["Month"],
        "Value": row[column]
    })

extreme_data = pd.DataFrame(extreme_rows)

st.dataframe(
    extreme_data,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# AUTOMATIC INSIGHTS
# ============================================================

st.markdown(
    '<div class="section-title">💡 Key Insights</div>',
    unsafe_allow_html=True
)


# Insight 1

if total_transfers > total_apprehensions:

    insight1 = (
        "Aggregate transfers exceeded apprehensions during the "
        "selected period, indicating strong downstream movement "
        "relative to new CBP intake."
    )

else:

    insight1 = (
        "Aggregate apprehensions exceeded transfers during the "
        "selected period, indicating higher CBP inflow relative "
        "to downstream transfers."
    )


# Insight 2

if hhs_bottleneck_days > cbp_bottleneck_days:

    insight2 = (
        f"HHS recorded more potential sustained-pressure days "
        f"({hhs_bottleneck_days}) than CBP ({cbp_bottleneck_days}), "
        "suggesting greater pressure at the HHS transfer-to-discharge stage."
    )

else:

    insight2 = (
        f"CBP recorded more potential sustained-pressure days "
        f"({cbp_bottleneck_days}) than HHS ({hhs_bottleneck_days}), "
        "suggesting greater pressure at the initial intake-to-transfer stage."
    )


# Insight 3

insight3 = (
    f"HHS care reached a maximum of "
    f"{max_hhs_care:,.0f} children during the selected period, "
    "representing the highest observed active care load."
)


# Insight 4

if discharge_cv >= 0.50:

    stability_text = "relatively high variability"

elif discharge_cv >= 0.25:

    stability_text = "moderate variability"

else:

    stability_text = "relatively low variability"

insight4 = (
    f"Daily HHS discharge activity showed {stability_text}, "
    f"with a coefficient of variation of "
    f"{discharge_cv * 100:.1f}%."
)


# Insight 5

last_pressure = pressure_df.iloc[-1]

if (
    abs(last_pressure["CBP Backlog Pressure"]) < 20
    and abs(last_pressure["HHS Backlog Pressure"]) < 20
):

    insight5 = (
        "Near the end of the selected period, daily flow pressure "
        "was close to zero, indicating a relatively balanced "
        "inflow/outflow relationship."
    )

else:

    insight5 = (
        "Near the end of the selected period, flow pressure "
        "remained measurable, indicating that inflow and outflow "
        "were not fully balanced."
    )


insights = [
    ("🔹 Pipeline Flow", insight1),
    ("🔹 Bottleneck Indicator", insight2),
    ("🔹 HHS Care Load", insight3),
    ("🔹 Discharge Stability", insight4),
    ("🔹 Recent Flow Balance", insight5)
]


for title, text in insights:

    st.markdown(
        f"""
        <div class="insight-card">
            <div class="insight-title">{title}</div>
            <div class="insight-text">{text}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# RECOMMENDATIONS
# ============================================================

st.markdown(
    '<div class="section-title">🎯 Recommendations</div>',
    unsafe_allow_html=True
)

recommendations = [
    "Monitor HHS discharge capacity during periods of sustained positive pressure.",
    "Use 7-day pressure indicators as an early-warning monitoring tool.",
    "Track transfer and discharge efficiency on a monthly basis.",
    "Investigate periods with unusually low discharge activity.",
    "Use dashboard pressure alerts to identify emerging operational constraints."
]

for i, recommendation in enumerate(recommendations, 1):

    st.write(
        f"**{i}.** {recommendation}"
    )


# ============================================================
# DETAILED DATA
# ============================================================

st.markdown(
    '<div class="section-title">📋 Detailed Data</div>',
    unsafe_allow_html=True
)

with st.expander("View filtered dataset"):

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

with st.expander("View monthly calculations"):

    st.dataframe(
        monthly_kpi,
        use_container_width=True
    )

with st.expander("View pressure calculations"):

    st.dataframe(
        pressure_df,
        use_container_width=True
    )


# ============================================================
# METHODOLOGY NOTE
# ============================================================

st.markdown("---")

st.markdown("### ℹ️ Methodology")

st.info(
    """
    **CBP Backlog Pressure** = Apprehensions − Transfers

    **HHS Backlog Pressure** = Transfers − Discharges

    A positive 7-day rolling pressure average is treated as a
    potential sustained-pressure indicator.

    These indicators are analytical measures based on aggregate
    daily flow data. They should not be interpreted as confirmed
    case-level processing delays or individual outcomes.
    """
)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        Child Processing Pipeline Analytics |
        Data Analysis & Visualization Internship Project
    </div>
    """,
    unsafe_allow_html=True
)