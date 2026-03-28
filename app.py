import streamlit as st
import pandas as pd

# 1. Load the database
@st.cache_data
def load_data():
    return pd.read_csv('cfd_database.csv')

try:
    df = load_data()
except FileNotFoundError:
    st.error("Error: Please make sure 'cfd_database.csv' is in the same folder as this script.")
    st.stop()

# 2. Build the User Interface
st.title("CFD Parameter Setup Optimizer")
st.write("Stop guessing. Get research-backed simulation parameters instantly.")

col1, col2 = st.columns(2)

with col1:
    # Dropdown for Geometry
    geom_list = df['Geometry Type'].unique()
    selected_geom = st.selectbox("Select Geometry", geom_list)

with col2:
    # Dropdown for Flow Regime (filtered by the selected geometry)
    filtered_df = df[df['Geometry Type'] == selected_geom]
    flow_list = filtered_df['Flow Velocity / Mach Number'].unique()
    selected_flow = st.selectbox("Select Flow Condition", flow_list)

# 3. The Retrieval Engine
if st.button("Get Parameters"):
    # Find the exact row matching the user's inputs
    result = filtered_df[filtered_df['Flow Velocity / Mach Number'] == selected_flow].iloc[0]
    
    st.success("Optimal Parameters Retrieved!")
    
    # Display the outputs cleanly
    st.subheader("Mesh Sizing")
    st.write(f"**Target y+ Value:** {result['Target y+ Value']}")
    st.write(f"**First Cell Height:** {result['First Cell Height']}")
    st.write(f"**Mesh Growth Rate:** {result['Mesh Growth Rate']}")
    
    st.subheader("Physics Setup")
    st.write(f"**Recommended Turbulence Model:** {result['Recommended Turbulence Model']}")
    st.write(f"**Reynolds Number:** {result['Reynolds Number']}")