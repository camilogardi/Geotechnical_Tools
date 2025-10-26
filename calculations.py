"""
Calculation and visualization functions for geotechnical analysis.

This module contains pure calculation and plotting functions extracted from the
Streamlit interface to improve code organization and testability.
"""

import hashlib
import numpy as np
import plotly.graph_objects as go
import streamlit as st
from scipy.interpolate import interpn
from fpdf import FPDF
from Tools import compute_rectangular_boussinesq


def get_cache_hash(q, Lx, Ly, Xmin, Xmax, Ymin, Ymax, Zmax, Nx, Ny, Nz):
    """Generate a hash for cache file naming based on parameters"""
    params_str = f"{q}_{Lx}_{Ly}_{Xmin}_{Xmax}_{Ymin}_{Ymax}_{Zmax}_{Nx}_{Ny}_{Nz}"
    return hashlib.md5(params_str.encode()).hexdigest()[:8]


@st.cache_data
def compute_boussinesq_cached(q, Lx, Ly, Xmin, Xmax, Ymin, Ymax, Zmax, Nx, Ny, Nz):
    """Cached wrapper for compute_rectangular_boussinesq"""
    return compute_rectangular_boussinesq(q, Lx, Ly, Xmin, Xmax, Ymin, Ymax, Zmax, Nx, Ny, Nz)


def interpolate_value(X, Y, Z, sigma, x_point, y_point, z_point):
    """Interpolate sigma value at a specific point using trilinear interpolation"""
    # Create points array for interpolation
    points = (Z, Y, X)

    # Query point
    xi = np.array([[z_point, y_point, x_point]])

    # Interpolate
    result = interpn(points, sigma, xi, method='linear', bounds_error=False, fill_value=0)
    return result[0]


def create_xz_plot(X, Y, Z, sigma, y_val):
    """Create X-Z contour plot at a specific Y value"""
    # Find nearest Y index
    y_idx = np.argmin(np.abs(Y - y_val))
    actual_y = Y[y_idx]

    # Extract X-Z slice
    sigma_xz = sigma[:, y_idx, :]  # shape (Nz, Nx)

    # Create meshgrid for plotting
    X_grid, Z_grid = np.meshgrid(X, Z)

    # Create plotly contour plot
    fig = go.Figure(data=go.Contour(
        x=X,
        y=Z,
        z=sigma_xz,
        colorscale='Viridis',
        colorbar=dict(title='σz (kPa)'),
        contours=dict(
            showlabels=True,
            labelfont=dict(size=10)
        )
    ))

    fig.update_layout(
        title=f'Corte X-Z en Y = {actual_y:.2f} m',
        xaxis_title='X (m)',
        yaxis_title='Profundidad Z (m)',
        yaxis=dict(autorange='reversed'),  # Depth increases downward
        height=500
    )

    return fig


def create_yz_plot(X, Y, Z, sigma, x_val):
    """Create Y-Z contour plot at a specific X value"""
    # Find nearest X index
    x_idx = np.argmin(np.abs(X - x_val))
    actual_x = X[x_idx]

    # Extract Y-Z slice
    sigma_yz = sigma[:, :, x_idx]  # shape (Nz, Ny)

    # Create plotly contour plot
    fig = go.Figure(data=go.Contour(
        x=Y,
        y=Z,
        z=sigma_yz,
        colorscale='Viridis',
        colorbar=dict(title='σz (kPa)'),
        contours=dict(
            showlabels=True,
            labelfont=dict(size=10)
        )
    ))

    fig.update_layout(
        title=f'Corte Y-Z en X = {actual_x:.2f} m',
        xaxis_title='Y (m)',
        yaxis_title='Profundidad Z (m)',
        yaxis=dict(autorange='reversed'),  # Depth increases downward
        height=500
    )

    return fig


def create_depth_profile_plot(X, Y, Z, sigma, x_point, y_point):
    """Create depth profile plot at a specific (x, y) location"""
    # Find nearest X and Y indices
    x_idx = np.argmin(np.abs(X - x_point))
    y_idx = np.argmin(np.abs(Y - y_point))
    actual_x = X[x_idx]
    actual_y = Y[y_idx]

    # Extract depth profile
    sigma_profile = sigma[:, y_idx, x_idx]

    # Create plotly line plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=sigma_profile,
        y=Z,
        mode='lines+markers',
        name='σz vs Profundidad',
        line=dict(color='blue', width=2),
        marker=dict(size=6)
    ))

    fig.update_layout(
        title=f'Perfil de Esfuerzo en X={actual_x:.2f} m, Y={actual_y:.2f} m',
        xaxis_title='σz (kPa)',
        yaxis_title='Profundidad Z (m)',
        yaxis=dict(autorange='reversed'),  # Depth increases downward
        height=500,
        showlegend=True
    )

    return fig


def generate_pdf_report(params, plots_config, X, Y, Z, sigma):
    """Generate PDF report with parameters and plots"""
    pdf = FPDF()
    pdf.add_page()

    # Title
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Reporte: Cálculo de Esfuerzos Verticales (Boussinesq)', ln=True, align='C')
    pdf.ln(10)

    # Parameters table
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Parámetros de Entrada:', ln=True)
    pdf.set_font('Arial', '', 10)

    params_text = [
        f"Sobrecarga q: {params['q']} kPa",
        f"Dimensiones carga: Lx = {params['Lx']} m, Ly = {params['Ly']} m",
        f"Dominio X: [{params['Xmin']}, {params['Xmax']}] m",
        f"Dominio Y: [{params['Ymin']}, {params['Ymax']}] m",
        f"Profundidad máxima: {params['Zmax']} m",
        f"Resolución malla: Nx={params['Nx']}, Ny={params['Ny']}, Nz={params['Nz']}"
    ]

    for text in params_text:
        pdf.cell(0, 6, text, ln=True)

    pdf.ln(10)

    # Plots section
    if plots_config:
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, 'Gráficas Generadas:', ln=True)
        pdf.set_font('Arial', '', 10)

        for i, plot_cfg in enumerate(plots_config):
            plot_type = plot_cfg['type']
            pdf.cell(0, 6, f"{i+1}. {plot_type}", ln=True)

    # Return PDF as bytes
    return bytes(pdf.output())
