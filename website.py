import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(
    page_title="Energy Calculator",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #FF6B6B;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .stSelectbox > div > div {
        background-color: #f0f2f6;
    }
    
    .energy-summary {
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Main title
st.markdown('<h1 class="main-header">⚡ Energy Consumption Calculator</h1>', unsafe_allow_html=True)

# Sidebar for user info
st.sidebar.header("👤 Personal Info")
name = st.sidebar.text_input("Name", placeholder="Enter your name")
age = st.sidebar.number_input("Age", min_value=1, max_value=120, value=25)
area = st.sidebar.text_input("Area", placeholder="Your area")
city = st.sidebar.text_input("City", placeholder="Your city")

# Main content
col1, col2 = st.columns([1, 1])

with col1:
    st.header("🏠 Home Details")
    bhk = st.selectbox("Number of rooms (BHK)", [1, 2, 3], index=1)
    
    # Base energy calculation
    calc = [2.4, 3.6, 4]
    base_energy = calc[bhk-1]
    
    st.success(f"Base energy consumption: {base_energy} kJ/day")

with col2:
    st.header("📊 Quick Stats")
    if name:
        st.info(f"Hello {name}! 👋")
    if city:
        st.info(f"📍 Location: {area}, {city}")

# Appliances section
st.header("🏠 Appliances & Usage")

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
weekly_energy = {day: base_energy for day in days}

# Fridge section
st.subheader("🧊 Refrigerator")
has_fridge = st.checkbox("I have a refrigerator")
if has_fridge:
    st.write("Which days do you use the fridge?")
    fridge_days = st.multiselect("Fridge usage days", days, default=days)
    for day in fridge_days:
        weekly_energy[day] += 4

# AC section
st.subheader("❄️ Air Conditioner")
has_ac = st.checkbox("I have an AC")
if has_ac:
    ac_count = st.number_input("Number of ACs", min_value=1, max_value=5, value=1)
    st.write("Which days do you use the AC?")
    ac_days = st.multiselect("AC usage days", days, default=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
    for day in ac_days:
        weekly_energy[day] += (ac_count * 3)

# Washing Machine section
st.subheader("👕 Washing Machine")
has_wm = st.checkbox("I have a washing machine")
if has_wm:
    st.write("Which days do you use the washing machine?")
    wm_days = st.multiselect("Washing machine usage days", days, default=["Sunday", "Wednesday"])
    for day in wm_days:
        weekly_energy[day] += 2

# Results section
st.header("📈 Energy Consumption Results")

# Create dataframe for better visualization
df = pd.DataFrame(list(weekly_energy.items()), columns=['Day', 'Energy (kJ)'])

# Calculate totals
total_weekly = sum(weekly_energy.values())
avg_daily = total_weekly / 7

# Display metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("📅 Total Weekly", f"{total_weekly:.1f} kJ")

with col2:
    st.metric("📊 Average Daily", f"{avg_daily:.1f} kJ")

with col3:
    st.metric("📈 Peak Day", f"{max(weekly_energy.values()):.1f} kJ")

# Charts
col1, col2 = st.columns(2)

with col1:
    # Bar chart
    fig_bar = px.bar(df, x='Day', y='Energy (kJ)', 
                     title='Daily Energy Consumption',
                     color='Energy (kJ)',
                     color_continuous_scale='plasma')
    fig_bar.update_layout(showlegend=False)
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    # Pie chart
    fig_pie = px.pie(df, values='Energy (kJ)', names='Day',
                     title='Weekly Energy Distribution')
    st.plotly_chart(fig_pie, use_container_width=True)

# Detailed breakdown
st.header("📋 Detailed Breakdown")

# Create a detailed table
breakdown_data = []
for day in days:
    breakdown_data.append({
        'Day': day,
        'Base Energy': base_energy,
        'Fridge': 4 if has_fridge and day in (fridge_days if has_fridge else []) else 0,
        'AC': (ac_count * 3) if has_ac and day in (ac_days if has_ac else []) else 0,
        'Washing Machine': 2 if has_wm and day in (wm_days if has_wm else []) else 0,
        'Total': weekly_energy[day]
    })

breakdown_df = pd.DataFrame(breakdown_data)
st.dataframe(breakdown_df, use_container_width=True)

# Energy saving tips
st.header("💡 Energy Saving Tips")
tips = [
    "🌟 Use energy-efficient appliances (5-star rating)",
    "🌡️ Set AC temperature to 24°C or higher",
    "🧊 Keep fridge at optimal temperature (3-4°C)",
    "👕 Wash clothes in cold water when possible",
    "💡 Switch to LED bulbs",
    "🔌 Unplug devices when not in use"
]

for tip in tips:
    st.write(tip)

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit | Track your energy, save the planet! 🌍")