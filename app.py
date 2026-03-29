import streamlit as st
import pandas as pd
import math

# --- 1. Load the Static Database ---
@st.cache_data
def load_data():
    return pd.read_csv('cfd_database.csv')

try:
    df = load_data()
except FileNotFoundError:
    st.error("Error: Please make sure 'cfd_database.csv' is in the same folder as this script.")
    st.stop()

# --- 2. The Math Engine (Menter's y+ Logic) ---
def calculate_first_cell_height(velocity, length, target_yplus, density=1.225, viscosity=1.789e-5):
    # Step 1: Reynolds Number
    reynolds = (density * velocity * length) / viscosity
    
    # Step 2: Skin Friction Coefficient (Empirical for turbulent flat plate)
    cf = 0.026 * math.pow(reynolds, -1/7)
    
    # Step 3: Wall Shear Stress
    tau_w = 0.5 * cf * density * math.pow(velocity, 2)
    
    # Step 4: Friction Velocity
    u_tau = math.sqrt(tau_w / density)
    
    # Step 5: First Cell Height (delta y)
    first_cell_height = (target_yplus * viscosity) / (density * u_tau)
    
    return first_cell_height, reynolds

# --- 3. Build the User Interface ---
st.title("CFD Parameter Setup Optimizer")
st.write("Research-backed simulation parameters and dynamic mesh sizing.")

st.divider()

# --- Section A: Database Retrieval ---
st.subheader("1. Standard Validation Geometries")
col1, col2 = st.columns(2)

with col1:
    geom_list = df['Geometry Type'].unique()
    selected_geom = st.selectbox("Select Geometry", geom_list)

with col2:
    filtered_df = df[df['Geometry Type'] == selected_geom]
    flow_list = filtered_df['Flow Velocity / Mach Number'].unique()
    selected_flow = st.selectbox("Select Flow Condition", flow_list)

if st.button("Get Baseline Parameters"):
    result = filtered_df[filtered_df['Flow Velocity / Mach Number'] == selected_flow].iloc[0]
    st.success("Optimal Baseline Retrieved!")
    st.write(f"**Recommended Turbulence Model:** {result['Recommended Turbulence Model']}")
    st.write(f"**Target y+ Value:** {result['Target y+ Value']}")

st.divider()

# --- Section B: Dynamic Mesh Calculator ---
st.subheader("2. Dynamic First Cell Height Calculator")
st.write("Calculate exact boundary layer thickness for your custom setup (Default fluid: Air at Sea Level).")

calc_col1, calc_col2 = st.columns(2)

with calc_col1:
    custom_velocity = st.number_input("Freestream Velocity (m/s)", min_value=0.1, value=50.0, step=5.0)
    custom_length = st.number_input("Reference Length / Chord (meters)", min_value=0.01, value=1.0, step=0.1)

with calc_col2:
    custom_yplus = st.number_input("Target y+ Value", min_value=0.1, value=1.0, step=0.1)
    
if st.button("Calculate Exact Mesh Size"):
    calc_height, calc_re = calculate_first_cell_height(custom_velocity, custom_length, custom_yplus)
    
    st.info("Mathematical Mesh Setup (Menter / Roache Guidelines)")
    st.write(f"**Calculated Reynolds Number:** {calc_re:.2e}")
    st.write(f"**Exact First Cell Height:** {calc_height:.6f} meters")
    
    # Quick conversion for Ansys (often easier in mm)
    st.write(f"*(That is exactly **{calc_height * 1000:.4f} millimeters** in Ansys)*")
