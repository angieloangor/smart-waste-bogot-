import streamlit as st
import geopandas as gpd
import pandas as pd
import folium
from folium.plugins import AntPath
from streamlit_folium import st_folium
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import json
import os

# ---------------------------------------------------------
# 1. Configuración de Página y CSS Global de Alto Impacto
# ---------------------------------------------------------
st.set_page_config(
    page_title="Bogotá Residuos Inteligente | Sistema Territorial",
    page_icon="B",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS Avanzados con Recuadros / Cards Estilizados
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Metrophobic&family=Rajdhani:wght@500;600;700&display=swap');
    
    :root {
        --bogota-blue: #0048a4;
        --bogota-blue-deep: #0048a4;
        --bogota-red: #e42037;
        --bogota-yellow: #ffb800;
        --bogota-turquoise: #00aa9f;
        --bogota-orange: #f47b2d;
        --bogota-green: #8cbe23;
        --bogota-purple: #342d7e;
        --surface: #ffffff;
        --surface-muted: #f3f6f8;
        --line: #cccccc;
        --ink: #333333;
        --muted: #575757;
    }

    html, body, [class*="css"] {
        font-family: 'Metrophobic', sans-serif;
    }

    body {
        background: #eef2f4;
        color: var(--ink);
    }
    .stApp {
        background: linear-gradient(180deg, #f7f9fa 0%, #eef2f4 55%, #e8eef1 100%);
    }
    .stApp::before {
        content: "";
        position: fixed;
        z-index: 9999;
        top: 0;
        left: 0;
        right: 0;
        height: 5px;
        background: var(--bogota-red);
        pointer-events: none;
    }
    .stApp::after {
        content: "";
        position: fixed;
        z-index: 9999;
        top: 5px;
        left: 0;
        right: 0;
        height: 3px;
        background: var(--bogota-yellow);
        pointer-events: none;
    }
    [data-testid="stHeader"] {
        background: rgba(255, 255, 255, 0.96) !important;
        border-bottom: 1px solid var(--line);
    }
    [data-testid="stToolbar"] {
        color: var(--bogota-blue) !important;
    }
    .block-container {
        max-width: 1440px;
        padding-top: 3rem;
        padding-bottom: 3rem;
    }
    h1, h2, h3, h4 {
        color: var(--bogota-blue-deep) !important;
        font-family: 'Rajdhani', sans-serif;
        letter-spacing: 0 !important;
    }
    .stButton > button, .stDownloadButton > button {
        border-radius: 7px !important;
        border: 1px solid var(--bogota-blue) !important;
        font-weight: 600 !important;
        transition: background 180ms ease, box-shadow 180ms ease, transform 180ms ease !important;
    }
    .stButton > button:hover, .stDownloadButton > button:hover {
        box-shadow: 0 4px 12px rgba(18, 63, 89, 0.16) !important;
        transform: translateY(-1px);
    }
    
    /* Contenedor Hero Principal con Video */
    .hero-container {
        position: relative;
        width: 100%;
        min-height: 480px;
        border-radius: 12px;
        overflow: hidden;
        margin-bottom: 2rem;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 14px 30px rgba(9, 45, 66, 0.18);
        background: linear-gradient(135deg, #071526 0%, #0f2b48 50%, #0a1f33 100%);
    }
    
    .hero-video {
        position: absolute;
        top: 50%;
        left: 50%;
        width: 177.78vh;   /* 16:9 ratio based on height */
        height: 100vh;
        min-width: 100%;
        min-height: 100%;
        transform: translate(-50%, -50%);
        pointer-events: none;
        opacity: 0.38;
        filter: saturate(1.3) contrast(1.1) brightness(0.85);
        border: none;
    }
    
    .hero-overlay {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: radial-gradient(circle at center, rgba(10, 31, 51, 0.6) 0%, rgba(4, 12, 22, 0.92) 100%);
    }
    
    .hero-content {
        position: relative;
        z-index: 2;
        text-align: center;
        padding: 3.5rem 2rem;
        max-width: 1000px;
        color: white;
    }
    .district-brand {
        display: inline-flex;
        align-items: flex-end;
        gap: 0.65rem;
        margin-bottom: 1.8rem;
        color: #ffffff;
        font-size: 1.35rem;
        font-weight: 800;
        letter-spacing: 0.08em;
    }
    .district-brand-word {
        position: relative;
        padding-bottom: 0.35rem;
    }
    .district-brand-word::after {
        content: "";
        position: absolute;
        left: 0;
        right: 0.25rem;
        bottom: 0;
        height: 4px;
        background: var(--bogota-red);
    }
    .district-brand-mark {
        position: relative;
        display: block;
        width: 18px;
        height: 18px;
        margin-bottom: 0.55rem;
        background: var(--bogota-yellow);
        transform: rotate(45deg);
        box-shadow: 8px -8px 0 -4px var(--bogota-yellow);
    }
    .sidebar-brand {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        padding: 0.5rem 0 1rem;
        color: var(--bogota-blue);
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.25rem;
        font-weight: 700;
        letter-spacing: 0.06em;
    }
    .sidebar-brand-mark {
        width: 16px;
        height: 16px;
        flex: 0 0 16px;
        background: var(--bogota-yellow);
        transform: rotate(45deg);
        border-bottom: 5px solid var(--bogota-red);
    }
    
    .hero-badge {
        display: inline-block;
        background: rgba(46, 204, 113, 0.2);
        border: 1px solid rgba(46, 204, 113, 0.6);
        color: #2ecc71;
        padding: 6px 20px;
        border-radius: 6px;
        font-size: 0.92rem;
        font-weight: 700;
        letter-spacing: 1.2px;
        text-transform: uppercase;
        margin-bottom: 1.2rem;
        backdrop-filter: blur(10px);
    }
    
    .hero-title {
        font-size: 3.4rem;
        font-weight: 800;
        line-height: 1.15;
        margin-bottom: 1.2rem;
        color: #ffffff !important;
        text-shadow: 0 4px 25px rgba(0,0,0,0.7);
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        color: #d6e6fa;
        line-height: 1.65;
        margin-bottom: 2rem;
        font-weight: 400;
        text-shadow: 0 2px 10px rgba(0,0,0,0.6);
    }
    
    /* Recuadros / Cajas de Contenido con Jerarquía Visual */
    .content-box {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1.8rem 2rem;
        margin-bottom: 1.6rem;
        box-shadow: 0 3px 12px rgba(9, 45, 66, 0.06);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .content-box:hover {
        box-shadow: 0 10px 28px rgba(0,0,0,0.08);
    }
    
    .glass-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(248,250,252,0.95) 100%);
        border: 1px solid #cbd5e1;
        border-radius: 10px;
        padding: 1.8rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
    }

    .box-header {
        font-size: 1.35rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 10px;
        border-bottom: 2px solid #f1f5f9;
        padding-bottom: 0.6rem;
    }

    .problem-box {
        background: linear-gradient(135deg, #fff5f5 0%, #fff1f1 100%);
        border: 1.5px solid #fecaca;
        border-radius: 10px;
        padding: 1.8rem;
        color: #7f1d1d;
        margin-bottom: 1.5rem;
        box-shadow: 0 6px 18px rgba(220, 38, 38, 0.05);
    }
    
    .solution-box {
        background: linear-gradient(135deg, #f0fdf4 0%, #ecfdf5 100%);
        border: 1.5px solid #a7f3d0;
        border-radius: 10px;
        padding: 1.8rem;
        color: #064e3b;
        margin-bottom: 1.5rem;
        box-shadow: 0 6px 18px rgba(16, 185, 129, 0.05);
    }

    .insight-card {
        background: linear-gradient(135deg, #f8fafc 0%, #eff6ff 100%);
        border-left: 5px solid #2563eb;
        border-radius: 0 10px 10px 0;
        padding: 1.4rem 1.6rem;
        margin: 1.4rem 0;
        font-size: 1.02rem;
        color: #1e293b;
        line-height: 1.7;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.07);
    }
    .insight-title {
        font-weight: 800;
        color: #1d4ed8;
        margin-bottom: 0.5rem;
        font-size: 1.15rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .methodology-step-box {
        background: #ffffff;
        border: 1.5px solid #e2e8f0;
        border-top: 5px solid #0284c7;
        border-radius: 10px;
        padding: 1.6rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 6px 18px rgba(0,0,0,0.04);
    }

    /* Tarjetas de Métricas & KPI */
    .metric-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1.5rem 1.2rem;
        box-shadow: 0 3px 12px rgba(9, 45, 66, 0.07);
        text-align: center;
        transition: transform 0.25s ease, box-shadow 0.25s ease;
    }
    .metric-card:hover {
        transform: translateY(-7px) scale(1.015);
        border-color: var(--bogota-yellow);
        box-shadow: 0 14px 28px rgba(0, 72, 164, 0.16);
    }
    .metric-card:hover .metric-value {
        transform: scale(1.08);
        color: var(--bogota-red) !important;
    }
    .metric-value {
        font-size: 2.4rem;
        font-weight: 800;
        color: #dc2626;
        line-height: 1.1;
        transition: transform 220ms ease, color 220ms ease;
    }
    .metric-label {
        font-size: 0.98rem;
        color: #475569;
        font-weight: 600;
        margin-top: 0.5rem;
    }

    /* Encabezados de Sección */
    .section-header {
        position: relative;
        border-left: 6px solid var(--bogota-red);
        padding: 0.6rem 0 0.6rem 16px;
        font-size: 1.55rem;
        font-weight: 800;
        color: var(--bogota-blue-deep);
        margin-top: 2.2rem;
        margin-bottom: 1.4rem;
        background: linear-gradient(90deg, rgba(190, 30, 45, 0.06), transparent 68%);
    }
    .section-header::after {
        content: "";
        position: absolute;
        left: -6px;
        bottom: 0;
        width: 42px;
        height: 3px;
        background: var(--bogota-yellow);
    }
    
    .sub-section-header {
        font-size: 1.35rem;
        font-weight: 700;
        color: var(--bogota-blue);
        margin-top: 1.6rem;
        margin-bottom: 0.9rem;
        padding-bottom: 0.45rem;
        border-bottom: 1px solid var(--line);
    }
    .problem-box, .solution-box, .content-box, .glass-card, .insight-card,
    .methodology-step-box {
        transition: transform 220ms ease, box-shadow 220ms ease, border-color 220ms ease;
    }
    .problem-box:hover, .solution-box:hover, .content-box:hover, .glass-card:hover,
    .insight-card:hover, .methodology-step-box:hover {
        transform: translateY(-4px);
        border-color: var(--bogota-yellow) !important;
        box-shadow: 0 12px 24px rgba(0, 72, 164, 0.12) !important;
    }

    [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlockBorderWrapper"],
    [data-testid="stExpander"] {
        border-color: var(--line) !important;
        border-radius: 10px !important;
        box-shadow: 0 3px 14px rgba(9, 45, 66, 0.055) !important;
    }
    [data-testid="stMetric"] {
        background: var(--surface) !important;
        border-top: 4px solid var(--bogota-yellow) !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        box-shadow: 0 3px 12px rgba(9, 45, 66, 0.08) !important;
    }
    [data-testid="stMetricLabel"] {
        color: var(--muted) !important;
        font-weight: 600 !important;
    }
    [data-testid="stMetricValue"] {
        color: var(--bogota-blue-deep) !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.3rem;
        border-bottom: 2px solid var(--line);
    }
    .stTabs [data-baseweb="tab"] {
        color: var(--muted);
        font-weight: 600;
        border-radius: 6px 6px 0 0;
    }
    .stTabs [aria-selected="true"] {
        color: var(--bogota-red) !important;
        border-bottom-color: var(--bogota-red) !important;
    }
    .stSelectbox label, .stMultiSelect label, .stSlider label,
    .stRadio label, .stCheckbox label {
        color: var(--bogota-blue) !important;
        font-weight: 600 !important;
    }
    .stProgress > div > div > div {
        background: var(--bogota-red) !important;
    }
    @keyframes district-reveal {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .hero-container, .content-box, .glass-card, .metric-card,
    .problem-box, .solution-box, .insight-card, .methodology-step-box {
        animation: district-reveal 500ms ease both;
    }

    /* Sidebar institucional: compacto por defecto y legible al expandirse */
    section[data-testid="stSidebar"] {
        position: fixed !important;
        z-index: 10000 !important;
        top: 0 !important;
        left: 0 !important;
        bottom: 0 !important;
        height: 100vh !important;
        width: 8px !important;
        overflow: visible !important;
        transition: width 250ms ease, min-width 250ms ease, max-width 250ms ease;
        border-right: 0 !important;
        background: transparent !important;
        box-shadow: none !important;
    }
    html body section[data-testid="stSidebar"] {
        width: 340px !important;
        min-width: 340px !important;
        max-width: 340px !important;
        transform: translateX(-332px) !important;
        transition: transform 250ms ease !important;
    }
    section[data-testid="stSidebar"]::before {
        content: "";
        position: absolute;
        z-index: 1000;
        top: 0;
        left: 0;
        width: 8px;
        height: 100%;
        background: transparent;
    }
    section[data-testid="stSidebar"] > div:first-child {
        width: 8px !important;
        padding: 0 !important;
        overflow: hidden !important;
        transition: width 250ms ease, min-width 250ms ease, max-width 250ms ease, padding 250ms ease;
    }
    html body section[data-testid="stSidebar"] > div:first-child {
        width: 340px !important;
        min-width: 340px !important;
        max-width: 340px !important;
        transform: translateX(0) !important;
        transition: transform 250ms ease !important;
    }
    section[data-testid="stSidebar"]:hover {
        width: 340px !important;
        min-width: 340px !important;
        max-width: 340px !important;
        box-shadow: 8px 0 24px rgba(15, 47, 73, 0.08);
    }
    section[data-testid="stSidebar"][aria-expanded="true"]:hover {
        width: 340px !important;
        min-width: 340px !important;
        max-width: 340px !important;
    }
    html body section[data-testid="stSidebar"][aria-expanded="true"]:hover {
        width: 340px !important;
        min-width: 340px !important;
        max-width: 340px !important;
        transform: translateX(0) !important;
    }
    section[data-testid="stSidebar"]:hover > div:first-child {
        width: 340px !important;
        min-width: 340px !important;
        max-width: 340px !important;
        padding: 1rem 0.85rem 1.25rem;
        background: #ffffff;
        border-left: 4px solid var(--bogota-red);
    }
    section[data-testid="stSidebar"][aria-expanded="true"]:hover > div:first-child {
        width: 340px !important;
        min-width: 340px !important;
        max-width: 340px !important;
    }
    html body section[data-testid="stSidebar"][aria-expanded="true"]:hover > div:first-child {
        width: 340px !important;
        min-width: 340px !important;
        max-width: 340px !important;
        transform: translateX(332px) !important;
    }
    html body section[data-testid="stSidebar"]:has(:hover) > div:first-child {
        width: 340px !important;
        min-width: 340px !important;
        max-width: 340px !important;
        transform: translateX(332px) !important;
        padding: 1rem 0.85rem 1.25rem;
        background: #ffffff;
        border-left: 4px solid var(--bogota-red);
    }
    section[data-testid="stSidebar"] [data-testid="stRadio"] > div[role="radiogroup"] > label {
        display: flex !important;
        align-items: center !important;
        width: 100% !important;
        min-width: 0 !important;
        height: 48px !important;
        box-sizing: border-box !important;
        margin: 0 0 0.45rem !important;
        padding: 0 0.8rem !important;
        overflow: hidden !important;
        border: 1px solid #dce5ec !important;
        border-radius: 8px !important;
        background: #ffffff !important;
        color: #365165 !important;
        cursor: pointer !important;
        transition: background 180ms ease, border-color 180ms ease, box-shadow 180ms ease, color 180ms ease, padding 250ms ease !important;
    }
    section[data-testid="stSidebar"] [data-testid="stRadio"] > div[role="radiogroup"] > label:hover {
        border-color: #9bb8ca !important;
        background: #eef5f8 !important;
        color: #123f59 !important;
    }
    section[data-testid="stSidebar"] [data-testid="stRadio"] > div[role="radiogroup"] > label:has(input:checked) {
        border-color: #91b8c9 !important;
        background: #e6f1f4 !important;
        color: #0b5266 !important;
        border-left: 4px solid var(--bogota-red) !important;
        box-shadow: 0 3px 10px rgba(190, 30, 45, 0.16) !important;
    }
    section[data-testid="stSidebar"] [data-testid="stRadio"] > div[role="radiogroup"] > label > div:first-child {
        flex: 0 0 20px !important;
        width: 20px !important;
        height: 20px !important;
        margin: 0 !important;
    }
    section[data-testid="stSidebar"] [data-testid="stRadio"] > div[role="radiogroup"] > label > div:first-child > div {
        display: none !important;
    }
    section[data-testid="stSidebar"] [data-testid="stRadio"] > div[role="radiogroup"] > label p {
        min-width: 0 !important;
        margin: 0 0 0 0.65rem !important;
        overflow: hidden !important;
        white-space: nowrap !important;
        text-overflow: clip !important;
        opacity: 0 !important;
        transform: translateX(-6px) !important;
        transition: opacity 140ms ease 0ms, transform 200ms ease 0ms !important;
    }
    section[data-testid="stSidebar"]:hover [data-testid="stRadio"] > div[role="radiogroup"] > label {
        padding: 0 0.8rem !important;
    }
    section[data-testid="stSidebar"]:hover [data-testid="stRadio"] > div[role="radiogroup"] > label p {
        opacity: 1 !important;
        transform: translateX(0) !important;
        transition-delay: 120ms !important;
    }
    html body section[data-testid="stSidebar"]:has(:hover) [data-testid="stRadio"] > div[role="radiogroup"] > label p {
        opacity: 1 !important;
        transform: translateX(0) !important;
        transition-delay: 120ms !important;
    }
    html body section[data-testid="stSidebar"]:hover [data-testid="stSidebarUserContent"] p,
    html body section[data-testid="stSidebar"]:has(:hover) [data-testid="stSidebarUserContent"] p {
        opacity: 1 !important;
        transform: translateX(0) !important;
    }
    html body section[data-testid="stSidebar"] > div[data-testid="stSidebarContent"]:hover {
        transform: translateX(332px) !important;
        width: 340px !important;
        min-width: 340px !important;
        max-width: 340px !important;
        padding: 1rem 0.85rem 1.25rem !important;
        background: #ffffff !important;
        border-left: 4px solid var(--bogota-red) !important;
    }
    html body section[data-testid="stSidebar"] > div[data-testid="stSidebarContent"]:hover [data-testid="stRadio"] > div[role="radiogroup"] > label p {
        opacity: 1 !important;
        transform: translateX(0) !important;
        transition-delay: 120ms !important;
    }
    @media (max-width: 768px) {
        section[data-testid="stSidebar"] {
            width: 8px !important;
        }
        section[data-testid="stSidebar"] > div:first-child {
            width: 8px !important;
        }
        section[data-testid="stSidebar"]:hover,
        section[data-testid="stSidebar"]:hover > div:first-child {
            width: min(360px, calc(100vw - 1rem)) !important;
            min-width: min(360px, calc(100vw - 1rem)) !important;
            max-width: min(360px, calc(100vw - 1rem)) !important;
        }
    }

    /* Controles de acción con el rojo y amarillo institucionales */
    div[data-testid="column"] button[kind="primary"],
    div[data-testid="stColumn"] button[kind="primary"] {
        background: var(--bogota-red) !important;
        border-color: var(--bogota-red) !important;
        border-radius: 7px !important;
        box-shadow: 0 5px 14px rgba(190, 30, 45, 0.2) !important;
    }
    div[data-testid="column"] button[kind="primary"]:hover,
    div[data-testid="stColumn"] button[kind="primary"]:hover {
        background: #a9192a !important;
        box-shadow: 0 7px 18px rgba(190, 30, 45, 0.28) !important;
    }
    .stDownloadButton > button {
        background: var(--bogota-blue) !important;
        color: #ffffff !important;
    }
    .home-brand-logo {
        display: block;
        width: min(250px, 70vw);
        height: auto;
        margin: 0 auto 1.4rem;
        filter: brightness(0) invert(1);
    }
    .hero-badge {
        position: relative;
        overflow: hidden;
        box-shadow: 0 5px 16px rgba(228, 32, 55, 0.24);
    }
    .hero-badge::after {
        content: "";
        position: absolute;
        top: 0;
        bottom: 0;
        left: -35%;
        width: 24%;
        background: rgba(255, 255, 255, 0.4);
        transform: skewX(-18deg);
        animation: badge-sheen 3.8s ease-in-out infinite;
    }
    @keyframes badge-sheen {
        0%, 55% { left: -35%; }
        100% { left: 125%; }
    }

        /* Overrides definitivos para Streamlit */
        html body section[data-testid="stSidebar"] {
            position: fixed !important;
            z-index: 10000 !important;
            top: calc(-100vh + 12px) !important;
            left: 0 !important;
            bottom: auto !important;
            width: 100vw !important;
            min-width: 100vw !important;
            max-width: 100vw !important;
            height: 100vh !important;
            overflow: hidden !important;
            background: var(--bogota-red) !important;
            border: 0 !important;
            box-shadow: none !important;
            transition: top 280ms cubic-bezier(0.22, 1, 0.36, 1) !important;
        }
        html body section[data-testid="stSidebar"]::before {
            content: "" !important;
            position: absolute !important;
            top: auto !important;
            right: 0 !important;
            bottom: 0 !important;
            left: 0 !important;
            width: 100% !important;
            height: 12px !important;
            background: var(--bogota-red) !important;
        }
        html body section[data-testid="stSidebar"]:hover {
            top: 0 !important;
            background: var(--bogota-red) !important;
            box-shadow: 0 10px 28px rgba(51, 51, 51, 0.24) !important;
        }
        html body section[data-testid="stSidebar"] > div:first-child {
            width: 100% !important;
            min-width: 100% !important;
            max-width: 100% !important;
            height: 100% !important;
            padding: 1.25rem 2rem !important;
            background: var(--bogota-red) !important;
        }
        html body section[data-testid="stSidebar"] [data-testid="stRadio"] > div[role="radiogroup"] > label {
            color: #ffffff !important;
            background: transparent !important;
            border-color: rgba(255, 255, 255, 0.55) !important;
        }
        html body section[data-testid="stSidebar"]:hover [data-testid="stRadio"] > div[role="radiogroup"] > label p {
            opacity: 1 !important;
            transform: none !important;
        }
        html body section[data-testid="stSidebar"] [data-testid="stRadio"] > div[role="radiogroup"] > label:hover,
        html body section[data-testid="stSidebar"] [data-testid="stRadio"] > div[role="radiogroup"] > label:has(input:checked) {
            background: rgba(255, 255, 255, 0.18) !important;
            border-color: var(--bogota-yellow) !important;
            color: #ffffff !important;
        }
        html body div[data-testid="column"] button,
        html body div[data-testid="stColumn"] button,
        html body div[data-testid="column"]:nth-child(1) button[kind="primary"],
        html body div[data-testid="stColumn"]:nth-child(1) button[kind="primary"],
        html body div[data-testid="column"]:nth-child(2) button,
        html body div[data-testid="stColumn"]:nth-child(2) button,
        html body div[data-testid="column"]:nth-child(3) button,
        html body div[data-testid="stColumn"]:nth-child(3) button {
            background: var(--bogota-red) !important;
            border: 1px solid var(--bogota-red) !important;
            border-radius: 6px !important;
            box-shadow: 0 4px 12px rgba(228, 32, 55, 0.22) !important;
        }
        html body div[data-testid="column"] button:hover,
        html body div[data-testid="stColumn"] button:hover {
            background: var(--bogota-blue) !important;
            border-color: var(--bogota-blue) !important;
        }
        @media (max-width: 768px) {
            html body section[data-testid="stSidebar"] > div:first-child {
                padding: 1rem !important;
            }
        }

    /* Bandeja superior institucional: cerrada fuera del viewport, roja al desplegar */
    html body section[data-testid="stSidebar"] {
        position: fixed !important;
        z-index: 10000 !important;
        top: calc(-100vh + 42px) !important;
        left: 0 !important;
        bottom: auto !important;
        width: 100vw !important;
        min-width: 100vw !important;
        max-width: 100vw !important;
        height: 100vh !important;
        transform: none !important;
        overflow: hidden !important;
        background: var(--bogota-red) !important;
        border: 0 !important;
        box-shadow: none !important;
        transition: top 280ms cubic-bezier(0.22, 1, 0.36, 1) !important;
    }
    html body section[data-testid="stSidebar"]::before {
        top: auto !important;
        bottom: 0 !important;
        left: 0 !important;
        width: 100% !important;
        height: 64px !important;
        background: var(--bogota-red) !important;
    }
    html body section[data-testid="stSidebar"]:hover,
    html body section[data-testid="stSidebar"]:has(:hover) {
        top: 0 !important;
        background: var(--bogota-red) !important;
        box-shadow: 0 10px 28px rgba(0, 0, 0, 0.2) !important;
    }
    html body section[data-testid="stSidebar"] > div:first-child {
        width: 100% !important;
        min-width: 100% !important;
        max-width: 100% !important;
        height: 100% !important;
        padding: 1.25rem 2rem !important;
        background: var(--bogota-red) !important;
        transform: none !important;
    }
    html body section[data-testid="stSidebar"] .sidebar-brand,
    html body section[data-testid="stSidebar"] h1,
    html body section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    html body section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] {
        color: #ffffff !important;
    }
    html body section[data-testid="stSidebar"] [data-testid="stRadio"] > div[role="radiogroup"] > label {
        background: transparent !important;
        border-color: rgba(255, 255, 255, 0.5) !important;
        color: #ffffff !important;
    }
    html body section[data-testid="stSidebar"] [data-testid="stRadio"] > div[role="radiogroup"] > label:hover,
    html body section[data-testid="stSidebar"] [data-testid="stRadio"] > div[role="radiogroup"] > label:has(input:checked) {
        background: rgba(255, 255, 255, 0.18) !important;
        border-color: var(--bogota-yellow) !important;
        color: #ffffff !important;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.16) !important;
    }
    html body section[data-testid="stSidebar"]:hover [data-testid="stRadio"] > div[role="radiogroup"] > label p,
    html body section[data-testid="stSidebar"]:has(:hover) [data-testid="stRadio"] > div[role="radiogroup"] > label p {
        opacity: 1 !important;
        transform: none !important;
    }
    @media (max-width: 768px) {
        html body section[data-testid="stSidebar"] > div:first-child {
            padding: 1rem !important;
        }
    }
    /* Zona de activación transparente; el panel no deja borde visible cerrado */
    html body section[data-testid="stSidebar"] {
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        bottom: 0 !important;
        width: 12px !important;
        min-width: 12px !important;
        max-width: 12px !important;
        transform: none !important;
        background: transparent !important;
        border: 0 !important;
        box-shadow: none !important;
    }
    html body section[data-testid="stSidebar"] > div:first-child {
        width: 12px !important;
        min-width: 12px !important;
        max-width: 12px !important;
        padding: 0 !important;
    }
    html body section[data-testid="stSidebar"]:hover,
    html body section[data-testid="stSidebar"]:has(:hover) {
        width: 340px !important;
        min-width: 340px !important;
        max-width: 340px !important;
        background: #ffffff !important;
        border-left: 4px solid var(--bogota-red) !important;
        box-shadow: 8px 0 24px rgba(0, 72, 164, 0.12) !important;
    }
    html body section[data-testid="stSidebar"]:hover > div:first-child,
    html body section[data-testid="stSidebar"]:has(:hover) > div:first-child {
        width: 340px !important;
        min-width: 340px !important;
        max-width: 340px !important;
        padding: 1rem 0.85rem 1.25rem !important;
        background: #ffffff !important;
    }
    html body section[data-testid="stSidebar"]:hover [data-testid="stRadio"] > div[role="radiogroup"] > label p,
    html body section[data-testid="stSidebar"]:has(:hover) [data-testid="stRadio"] > div[role="radiogroup"] > label p {
        opacity: 1 !important;
        transform: translateX(0) !important;
    }

    /* Capa final de identidad distrital: evita estilos heredados y degradados */
    .hero-container {
        background: var(--bogota-blue) !important;
        box-shadow: 0 14px 30px rgba(0, 72, 164, 0.18) !important;
    }
    .hero-overlay {
        background: rgba(0, 0, 0, 0.48) !important;
    }
    .hero-badge {
        background: var(--bogota-red) !important;
        border-color: var(--bogota-yellow) !important;
        color: #ffffff !important;
    }
    .content-box, .glass-card, .metric-card, .methodology-step-box,
    .problem-box, .solution-box, .insight-card {
        background: #ffffff !important;
        border-color: var(--line) !important;
        color: var(--ink) !important;
    }
    .box-header, .metric-label, .insight-title,
    .content-box p, .glass-card p, .problem-box p, .solution-box p,
    .insight-card p, .methodology-step-box p,
    [style*="#475569"], [style*="#334155"], [style*="#1e293b"],
    [style*="#374151"], [style*="#475569"] {
        color: var(--ink) !important;
    }
    .problem-box {
        border-top: 5px solid var(--bogota-red) !important;
    }
    .solution-box {
        border-top: 5px solid var(--bogota-turquoise) !important;
    }
    .insight-card {
        border-left-color: var(--bogota-blue) !important;
    }
    .methodology-step-box {
        border-top-color: var(--bogota-blue) !important;
    }
    .metric-value, [style*="#dc2626"], [style*="#991b1b"] {
        color: var(--bogota-red) !important;
    }
    [style*="#0284c7"], [style*="#0369a1"], [style*="#2563eb"], [style*="#1d4ed8"] {
        color: var(--bogota-blue) !important;
        border-color: var(--bogota-blue) !important;
    }
    [style*="#059669"], [style*="#10b981"], [style*="#064e3b"] {
        color: var(--bogota-turquoise) !important;
        border-color: var(--bogota-turquoise) !important;
    }
    [style*="#d97706"], [style*="#f59e0b"] {
        color: var(--bogota-orange) !important;
        border-color: var(--bogota-orange) !important;
    }
    [style*="#7c3aed"], [style*="#9333ea"] {
        color: var(--bogota-purple) !important;
        border-color: var(--bogota-purple) !important;
    }
    [style*="#f8fafc"], [style*="#f1f5f9"], [style*="#eff6ff"],
    [style*="#f0fdf4"], [style*="#ecfdf5"], [style*="#fff5f5"],
    [style*="#fff1f1"], [style*="#fffbeb"], [style*="#fef3c7"] {
        background: #ffffff !important;
    }
    [style*="#e2e8f0"], [style*="#cbd5e1"], [style*="#fecaca"],
    [style*="#a7f3d0"], [style*="#dbeafe"] {
        border-color: var(--line) !important;
    }
    div[data-testid="column"] button[kind="primary"],
    div[data-testid="stColumn"] button[kind="primary"],
    div[data-testid="column"]:nth-child(1) button[kind="primary"],
    div[data-testid="stColumn"]:nth-child(1) button[kind="primary"],
    div[data-testid="column"]:nth-child(2) button,
    div[data-testid="stColumn"]:nth-child(2) button,
    div[data-testid="column"]:nth-child(3) button,
    div[data-testid="stColumn"]:nth-child(3) button {
        background: var(--bogota-red) !important;
        border: 1px solid var(--bogota-red) !important;
        border-radius: 6px !important;
        box-shadow: 0 4px 12px rgba(228, 32, 55, 0.22) !important;
    }
    div[data-testid="column"] button[kind="primary"]:hover,
    div[data-testid="stColumn"] button[kind="primary"]:hover,
    div[data-testid="column"]:nth-child(2) button:hover,
    div[data-testid="stColumn"]:nth-child(2) button:hover,
    div[data-testid="column"]:nth-child(3) button:hover,
    div[data-testid="stColumn"]:nth-child(3) button:hover {
        background: var(--bogota-blue) !important;
    }

    /* Botones de Inicio con Animación Hover del Camión */
    div[data-testid="column"]:nth-child(1) button[kind="primary"],
    div[data-testid="stColumn"]:nth-child(1) button[kind="primary"] {
        background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%) !important;
        color: white !important;
        border-radius: 50px !important;
        font-size: 1.15rem !important;
        font-weight: 700 !important;
        padding: 0.9rem 2rem !important;
        border: 2px solid rgba(255,255,255,0.3) !important;
        box-shadow: 0 10px 25px rgba(220, 38, 38, 0.4) !important;
        transition: all 0.35s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        position: relative !important;
    }
    div[data-testid="column"]:nth-child(1) button[kind="primary"]:hover,
    div[data-testid="stColumn"]:nth-child(1) button[kind="primary"]:hover {
        transform: translateY(-4px) scale(1.03) !important;
        box-shadow: 0 15px 35px rgba(220, 38, 38, 0.65) !important;
        background: linear-gradient(135deg, #ef4444 0%, #b91c1c 100%) !important;
    }
    div[data-testid="column"]:nth-child(1) button[kind="primary"]:hover::after,
    div[data-testid="stColumn"]:nth-child(1) button[kind="primary"]:hover::after {
        content: "";
        display: inline-block;
        animation: drive-truck-fast 0.6s infinite alternate ease-in-out;
        margin-left: 8px;
        font-size: 1.35rem;
    }

    @keyframes drive-truck-fast {
        0% { transform: translateX(0px) rotate(0deg); }
        50% { transform: translateX(8px) rotate(-4deg); }
        100% { transform: translateX(16px) rotate(4deg); }
    }

    div[data-testid="column"]:nth-child(2) button,
    div[data-testid="stColumn"]:nth-child(2) button {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important;
        color: white !important;
        border-radius: 50px !important;
        font-size: 1.15rem !important;
        font-weight: 700 !important;
        padding: 0.9rem 2rem !important;
        border: 2px solid rgba(255,255,255,0.3) !important;
        box-shadow: 0 10px 25px rgba(2, 132, 199, 0.35) !important;
        transition: all 0.35s ease !important;
    }
    div[data-testid="column"]:nth-child(2) button:hover,
    div[data-testid="stColumn"]:nth-child(2) button:hover {
        transform: translateY(-4px) scale(1.03) !important;
        box-shadow: 0 15px 35px rgba(2, 132, 199, 0.6) !important;
        background: linear-gradient(135deg, #38bdf8 0%, #0284c7 100%) !important;
    }
    div[data-testid="column"]:nth-child(2) button:hover::after,
    div[data-testid="stColumn"]:nth-child(2) button:hover::after {
        content: "";
        display: inline-block;
        margin-left: 8px;
    }

    div[data-testid="column"]:nth-child(3) button,
    div[data-testid="stColumn"]:nth-child(3) button {
        background: linear-gradient(135deg, #7c3aed 0%, #5b21b6 100%) !important;
        color: white !important;
        border-radius: 50px !important;
        font-size: 1.15rem !important;
        font-weight: 700 !important;
        padding: 0.9rem 2rem !important;
        border: 2px solid rgba(255,255,255,0.3) !important;
        box-shadow: 0 10px 25px rgba(124, 58, 237, 0.35) !important;
        transition: all 0.35s ease !important;
    }
    div[data-testid="column"]:nth-child(3) button:hover,
    div[data-testid="stColumn"]:nth-child(3) button:hover {
        transform: translateY(-4px) scale(1.03) !important;
        box-shadow: 0 15px 35px rgba(124, 58, 237, 0.6) !important;
        background: linear-gradient(135deg, #a78bfa 0%, #7c3aed 100%) !important;
    }
    div[data-testid="column"]:nth-child(3) button:hover::after,
    div[data-testid="stColumn"]:nth-child(3) button:hover::after {
        content: "";
        display: inline-block;
        margin-left: 8px;
    }

    /* Estado final del panel superior */
    html body section[data-testid="stSidebar"] {
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        bottom: auto !important;
        width: 100vw !important;
        min-width: 100vw !important;
        max-width: 100vw !important;
        height: 64px !important;
        background: var(--bogota-red) !important;
        border: 0 !important;
        overflow: hidden !important;
        transition: top 280ms ease !important;
    }
    html body section[data-testid="stSidebar"]:hover {
        top: 0 !important;
        height: 100vh !important;
        box-shadow: 0 10px 28px rgba(51, 51, 51, 0.24) !important;
    }
    html body section[data-testid="stSidebar"] > div:first-child {
        width: 100% !important;
        min-width: 100% !important;
        max-width: 100% !important;
        height: 64px !important;
        padding: 1.25rem 2rem !important;
        background: var(--bogota-red) !important;
    }
    html body section[data-testid="stSidebar"]::before {
        top: auto !important;
        bottom: 0 !important;
        width: 100% !important;
        height: 12px !important;
        background: var(--bogota-red) !important;
    }
    html body section[data-testid="stSidebar"]:hover {
        top: 0 !important;
        width: 100vw !important;
        min-width: 100vw !important;
        max-width: 100vw !important;
        background: var(--bogota-red) !important;
    }
    html body section[data-testid="stSidebar"]:hover > div:first-child {
        width: 100% !important;
        min-width: 100% !important;
        max-width: 100% !important;
        height: 100% !important;
        background: var(--bogota-red) !important;
    }
    html body section[data-testid="stSidebar"]:hover [data-testid="stSidebarContent"],
    html body section[data-testid="stSidebar"]:hover [data-testid="stSidebarUserContent"] {
        width: 100% !important;
        max-height: calc(100vh - 1.5rem) !important;
        overflow-y: auto !important;
        overflow-x: hidden !important;
        scrollbar-color: var(--bogota-yellow) var(--bogota-red);
    }
    html body section[data-testid="stSidebar"]:hover [data-testid="stSidebarUserContent"] h2,
    html body section[data-testid="stSidebar"]:hover [data-testid="stSidebarUserContent"] h3,
    html body section[data-testid="stSidebar"]:hover [data-testid="stSidebarUserContent"] label,
    html body section[data-testid="stSidebar"]:hover [data-testid="stSidebarUserContent"] p {
        color: #ffffff !important;
    }
    html body section[data-testid="stSidebar"]:hover [data-testid="stSidebarUserContent"] input,
    html body section[data-testid="stSidebar"]:hover [data-testid="stSidebarUserContent"] textarea,
    html body section[data-testid="stSidebar"]:hover [data-testid="stSidebarUserContent"] [data-baseweb="select"] > div {
        border-color: rgba(255, 255, 255, 0.7) !important;
    }
    html body section[data-testid="stSidebar"]:hover [data-testid="stSlider"] [data-baseweb="slider"] > div > div {
        background: var(--bogota-yellow) !important;
    }
    html body section[data-testid="stSidebar"]:hover [data-testid="stRadio"] > div[role="radiogroup"] > label p {
        opacity: 1 !important;
        transform: none !important;
    }
    html body section[data-testid="stSidebar"] [data-testid="stRadio"] > div[role="radiogroup"] > label p {
        opacity: 1 !important;
        transform: none !important;
    }
    html body section[data-testid="stSidebar"] [data-testid="stRadio"] > div[role="radiogroup"] > label p {
        opacity: 1 !important;
        transform: none !important;
    }
    html body section[data-testid="stSidebar"]:hover [data-testid="stSidebarUserContent"] p {
        opacity: 1 !important;
        transform: none !important;
    }

    /* Panel de pestañas reconstruido: bandeja superior institucional */
    html body section[data-testid="stSidebar"] {
        position: fixed !important;
        inset: 0 0 auto 0 !important;
        z-index: 10000 !important;
        width: 100vw !important;
        min-width: 100vw !important;
        max-width: 100vw !important;
        height: 64px !important;
        overflow: hidden !important;
        background: var(--bogota-red) !important;
        border: 0 !important;
        box-shadow: 0 3px 12px rgba(51, 51, 51, 0.16) !important;
        transition: height 280ms cubic-bezier(0.22, 1, 0.36, 1) !important;
    }
    html body section[data-testid="stSidebar"]:hover {
        height: min(100vh, 760px) !important;
        overflow: visible !important;
    }
    html body section[data-testid="stSidebar"]:has(:hover) {
        height: min(100vh, 760px) !important;
        width: 100vw !important;
        min-width: 100vw !important;
        max-width: 100vw !important;
        overflow: visible !important;
    }
    html body section[data-testid="stSidebar"] > div:first-child {
        width: 100% !important;
        min-width: 100% !important;
        max-width: 100% !important;
        height: 100% !important;
        padding: 0 !important;
        overflow: hidden !important;
        background: var(--bogota-red) !important;
    }
    html body section[data-testid="stSidebar"] [data-testid="stSidebarContent"] {
        width: 100% !important;
        height: 100% !important;
        overflow-y: auto !important;
        overflow-x: hidden !important;
        padding: 0 2rem 2rem !important;
        scrollbar-color: var(--bogota-yellow) var(--bogota-red);
    }
    html body section[data-testid="stSidebar"]:has(:hover) [data-testid="stSidebarContent"] {
        height: calc(100vh - 1rem) !important;
        max-height: calc(100vh - 1rem) !important;
    }
    html body section[data-testid="stSidebar"]:hover > div:first-child {
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        z-index: 1 !important;
        transform: none !important;
        height: 100vh !important;
        max-height: 100vh !important;
        overflow: visible !important;
    }
    html body section[data-testid="stSidebar"]:hover [data-testid="stSidebarContent"] {
        height: 100vh !important;
        max-height: 100vh !important;
        overflow-y: auto !important;
        background: var(--bogota-red) !important;
    }
    html body section[data-testid="stSidebar"] [data-testid="stSidebarHeader"] {
        position: sticky !important;
        top: 0 !important;
        z-index: 2 !important;
        min-height: 64px !important;
        background: var(--bogota-red) !important;
    }
    html body section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {
        padding-top: 1rem !important;
    }
    html body section[data-testid="stSidebar"] [data-testid="stRadio"] > label[data-testid="stWidgetLabel"] {
        display: none !important;
    }
    html body section[data-testid="stSidebar"] [data-testid="stRadio"] > div[role="radiogroup"] {
        display: grid !important;
        grid-template-columns: repeat(4, minmax(0, 1fr)) !important;
        gap: 0.6rem !important;
        width: 100% !important;
        margin: 0.25rem 0 1.25rem !important;
    }
    html body section[data-testid="stSidebar"] [data-testid="stRadio"] > div[role="radiogroup"] > label {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        min-height: 58px !important;
        width: 100% !important;
        margin: 0 !important;
        padding: 0.65rem 0.8rem !important;
        border: 1px solid rgba(255, 255, 255, 0.5) !important;
        border-radius: 6px !important;
        background: rgba(255, 255, 255, 0.08) !important;
        color: #ffffff !important;
        text-align: center !important;
        transition: background 180ms ease, border-color 180ms ease, transform 180ms ease, box-shadow 180ms ease !important;
    }
    html body section[data-testid="stSidebar"] [data-testid="stRadio"] > div[role="radiogroup"] > label:hover {
        background: rgba(255, 255, 255, 0.18) !important;
        border-color: var(--bogota-yellow) !important;
        transform: translateY(-2px) !important;
    }
    html body section[data-testid="stSidebar"] [data-testid="stRadio"] > div[role="radiogroup"] > label:has(input:checked) {
        background: #ffffff !important;
        border-color: var(--bogota-yellow) !important;
        color: var(--bogota-red) !important;
        box-shadow: 0 4px 12px rgba(51, 51, 51, 0.2) !important;
    }
    html body section[data-testid="stSidebar"] [data-testid="stRadio"] > div[role="radiogroup"] > label > div:first-child {
        display: none !important;
    }
    html body section[data-testid="stSidebar"] [data-testid="stRadio"] > div[role="radiogroup"] > label p {
        display: block !important;
        min-width: 0 !important;
        margin: 0 !important;
        overflow: hidden !important;
        white-space: normal !important;
        text-overflow: clip !important;
        opacity: 1 !important;
        transform: none !important;
        color: inherit !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        line-height: 1.12 !important;
    }
    html body section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] > div:not(:has([data-testid="stRadio"])) h2,
    html body section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] > div:not(:has([data-testid="stRadio"])) h3 {
        color: #ffffff !important;
    }
    html body section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] input,
    html body section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] [data-baseweb="select"] > div {
        background: #ffffff !important;
        color: #333333 !important;
        border-color: rgba(255, 255, 255, 0.7) !important;
    }
    @media (max-width: 800px) {
        html body section[data-testid="stSidebar"] [data-testid="stRadio"] > div[role="radiogroup"] {
            grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
        }
        html body section[data-testid="stSidebar"] [data-testid="stSidebarContent"] {
            padding-inline: 1rem !important;
        }
    }
    /* Navegacion lateral permanente */
    html body section[data-testid="stSidebar"] {
        position: fixed !important;
        inset: 0 auto 0 0 !important;
        z-index: 10000 !important;
        width: 304px !important;
        min-width: 304px !important;
        max-width: 304px !important;
        height: 100vh !important;
        overflow: hidden !important;
        background: var(--bogota-red) !important;
        border: 0 !important;
        box-shadow: 6px 0 18px rgba(51, 51, 51, 0.18) !important;
        transform: none !important;
    }
    html body section[data-testid="stSidebar"]::before {
        display: none !important;
    }
    html body section[data-testid="stSidebar"] > div:first-child,
    html body section[data-testid="stSidebar"] [data-testid="stSidebarContent"] {
        width: 100% !important;
        min-width: 100% !important;
        max-width: 100% !important;
        height: 100vh !important;
        max-height: 100vh !important;
        padding: 1rem !important;
        overflow-y: auto !important;
        overflow-x: hidden !important;
        background: var(--bogota-red) !important;
    }
    html body section[data-testid="stSidebar"] h1,
    html body section[data-testid="stSidebar"] h2,
    html body section[data-testid="stSidebar"] h3,
    html body section[data-testid="stSidebar"] p,
    html body section[data-testid="stSidebar"] label {
        color: #ffffff !important;
    }
    html body section[data-testid="stSidebar"] [data-testid="stRadio"] > label[data-testid="stWidgetLabel"] {
        display: none !important;
    }
    html body section[data-testid="stSidebar"] [data-testid="stRadio"] > div[role="radiogroup"] {
        display: grid !important;
        grid-template-columns: 1fr !important;
        gap: 0.55rem !important;
        margin: 0.4rem 0 1.25rem !important;
    }
    html body section[data-testid="stSidebar"] [data-testid="stRadio"] > div[role="radiogroup"] > label {
        display: flex !important;
        align-items: center !important;
        min-height: 50px !important;
        margin: 0 !important;
        padding: 0.7rem 0.85rem !important;
        border: 1px solid rgba(255, 255, 255, 0.48) !important;
        border-radius: 6px !important;
        background: rgba(255, 255, 255, 0.08) !important;
        color: #ffffff !important;
        transition: background 180ms ease, border-color 180ms ease, transform 180ms ease, box-shadow 180ms ease !important;
    }
    html body section[data-testid="stSidebar"] [data-testid="stRadio"] > div[role="radiogroup"] > label:hover {
        background: rgba(255, 255, 255, 0.18) !important;
        border-color: var(--bogota-yellow) !important;
        transform: translateX(3px) !important;
    }
    html body section[data-testid="stSidebar"] [data-testid="stRadio"] > div[role="radiogroup"] > label:has(input:checked) {
        background: #ffffff !important;
        border-color: var(--bogota-yellow) !important;
        color: var(--bogota-red) !important;
        box-shadow: 0 4px 12px rgba(51, 51, 51, 0.2) !important;
    }
    html body section[data-testid="stSidebar"] [data-testid="stRadio"] > div[role="radiogroup"] > label > div:first-child {
        display: none !important;
    }
    html body section[data-testid="stSidebar"] [data-testid="stRadio"] > div[role="radiogroup"] > label p {
        display: block !important;
        margin: 0 !important;
        overflow: visible !important;
        white-space: normal !important;
        opacity: 1 !important;
        transform: none !important;
        color: inherit !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
    }
    html body section[data-testid="stSidebar"] [data-baseweb="select"] > div,
    html body section[data-testid="stSidebar"] input {
        background: #ffffff !important;
        color: #333333 !important;
    }
    @media (max-width: 800px) {
        html body section[data-testid="stSidebar"] {
            width: 260px !important;
            min-width: 260px !important;
            max-width: 260px !important;
        }
    }
    /* El panel es permanente: el cursor no cambia su geometria */
    html body section[data-testid="stSidebar"]:hover,
    html body section[data-testid="stSidebar"]:has(:hover) {
        width: 304px !important;
        min-width: 304px !important;
        max-width: 304px !important;
        height: 100vh !important;
        background: var(--bogota-red) !important;
        border: 0 !important;
        box-shadow: 6px 0 18px rgba(51, 51, 51, 0.18) !important;
    }
    html body section[data-testid="stSidebar"]:hover > div:first-child,
    html body section[data-testid="stSidebar"]:has(:hover) > div:first-child {
        width: 100% !important;
        min-width: 100% !important;
        max-width: 100% !important;
        height: 100vh !important;
        padding: 1rem !important;
        background: var(--bogota-red) !important;
        transform: none !important;
    }
    html body section[data-testid="stSidebar"].stSidebar:hover,
    html body section[data-testid="stSidebar"].stSidebar:has(:hover) {
        width: 304px !important;
        min-width: 304px !important;
        max-width: 304px !important;
        height: 100vh !important;
        background: var(--bogota-red) !important;
        border: 0 !important;
        box-shadow: 6px 0 18px rgba(51, 51, 51, 0.18) !important;
    }
    html body section[data-testid="stSidebar"].stSidebar:hover > div:first-child,
    html body section[data-testid="stSidebar"].stSidebar:has(:hover) > div:first-child {
        width: 100% !important;
        min-width: 100% !important;
        max-width: 100% !important;
        height: 100vh !important;
        background: var(--bogota-red) !important;
        transform: none !important;
    }
    html body section[data-testid="stSidebar"]:hover [data-testid="stRadio"] > div[role="radiogroup"] > label p,
    html body section[data-testid="stSidebar"]:has(:hover) [data-testid="stRadio"] > div[role="radiogroup"] > label p {
        opacity: 1 !important;
        transform: none !important;
    }
    /* Correccion final: mantener el panel oculto hasta entrar en su activador */
    html body section[data-testid="stSidebar"] {
        position: fixed !important;
        inset: 0 auto 0 0 !important;
        width: 12px !important;
        min-width: 12px !important;
        max-width: 12px !important;
        height: 100vh !important;
        overflow: hidden !important;
        background: transparent !important;
        border: 0 !important;
        box-shadow: none !important;
        transform: none !important;
    }
    html body section[data-testid="stSidebar"] > div:first-child,
    html body section[data-testid="stSidebar"] [data-testid="stSidebarContent"] {
        width: 12px !important;
        min-width: 12px !important;
        max-width: 12px !important;
        height: 100vh !important;
        max-height: 100vh !important;
        padding: 0 !important;
        overflow: hidden !important;
        background: transparent !important;
    }
    html body section[data-testid="stSidebar"]:hover {
        width: 304px !important;
        min-width: 304px !important;
        max-width: 304px !important;
        background: var(--bogota-red) !important;
        box-shadow: 6px 0 18px rgba(51, 51, 51, 0.18) !important;
    }
    html body section[data-testid="stSidebar"]:hover > div:first-child,
    html body section[data-testid="stSidebar"]:hover [data-testid="stSidebarContent"] {
        width: 304px !important;
        min-width: 304px !important;
        max-width: 304px !important;
        height: 100vh !important;
        max-height: 100vh !important;
        padding: 1rem !important;
        overflow-y: auto !important;
        overflow-x: hidden !important;
        background: var(--bogota-red) !important;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. Inicialización de Estado y Carga de Datos
# ---------------------------------------------------------
if "current_page" not in st.session_state:
    st.session_state.current_page = "home"

@st.cache_data
def load_all_data():
    app_dir = os.path.dirname(os.path.abspath(__file__))
    base_modelo = os.path.abspath(os.path.join(app_dir, "..", "03_MODELO"))
    pred_path = os.path.join(base_modelo, "05_predicciones", "riesgo_predicho.gpkg")
    ranking_path = os.path.join(base_modelo, "07_resultados", "ranking_zonas.csv")
    models_path = os.path.join(base_modelo, "07_resultados", "matriz_modelos.csv")
    feat_path = os.path.join(base_modelo, "06_explicabilidad", "feature_importance.csv")
    dataset_csv = os.path.join(base_modelo, "01_dataset_modelo", "dataset_modelo.csv")

    df_geo_raw = gpd.read_file(pred_path)
    
    centroids_3116 = df_geo_raw.geometry.centroid
    centroids_4326 = centroids_3116.to_crs(epsg=4326)
    
    df_geo_raw['centroid_3116'] = centroids_3116
    df_geo_raw['centroid_lat'] = centroids_4326.y
    df_geo_raw['centroid_lon'] = centroids_4326.x
    
    # Limpieza de textos
    loc_clean = {
        'Usaqun': 'Usaquén', 'Usaquen': 'Usaquén',
        'Ciudad Bolvar': 'Ciudad Bolívar', 'Ciudad Bolivar': 'Ciudad Bolívar',
        'Engativ': 'Engativá', 'Engativa': 'Engativá',
        'Fontibn': 'Fontibón', 'Fontibon': 'Fontibón',
        'San Cristbal': 'San Cristóbal', 'San Cristobal': 'San Cristóbal',
        'Antonio Nario': 'Antonio Nariño', 'Antonio Narino': 'Antonio Nariño',
        'Los Mrtires': 'Los Mártires', 'Los Martires': 'Los Mártires'
    }
    if 'loc_name' in df_geo_raw.columns:
        df_geo_raw['loc_name'] = df_geo_raw['loc_name'].astype(str).map(lambda x: loc_clean.get(x, x))
    if 'nombre_lugar' in df_geo_raw.columns:
        df_geo_raw['nombre_lugar'] = df_geo_raw['nombre_lugar'].astype(str).str.replace('\ufffd', 'ó')

    df_geo_out = df_geo_raw.to_crs(epsg=4326)
    ranking_out = pd.read_csv(ranking_path)
    if 'loc_name' in ranking_out.columns:
        ranking_out['loc_name'] = ranking_out['loc_name'].astype(str).map(lambda x: loc_clean.get(x, x))
    if 'nombre_lugar' in ranking_out.columns:
        ranking_out['nombre_lugar'] = ranking_out['nombre_lugar'].astype(str).str.replace('\ufffd', 'ó')
        
    models_out = pd.read_csv(models_path)
    feat_out = pd.read_csv(feat_path)
    dataset_out = pd.read_csv(dataset_csv)
    
    return df_geo_out, ranking_out, models_out, feat_out, dataset_out

df_geo, ranking, df_modelos, df_feat, df_dataset = load_all_data()

# ---------------------------------------------------------
# 3. Barra Lateral y Navegación
# ---------------------------------------------------------
st.sidebar.markdown('<div class="sidebar-brand"><span class="sidebar-brand-mark"></span><span>BOGOTÁ</span></div>', unsafe_allow_html=True)
st.sidebar.title("Bogotá Residuos")
st.sidebar.markdown("**Sistema Predictivo & Operativo**")
st.sidebar.markdown("---")

menu_opciones = {
    "home": "Inicio (Impacto & Visión)",
    "dashboard": "Tablero de Decisiones (Autoridades)",
    "simulator": "Simulador de Rutas & Mapa",
    "analysis": "Análisis Técnico & Metodología"
}

nav_selection = st.sidebar.radio(
    "Navegación Principal:",
    options=list(menu_opciones.keys()),
    format_func=lambda x: menu_opciones[x],
    index=list(menu_opciones.keys()).index(st.session_state.current_page)
)

if nav_selection != st.session_state.current_page:
    st.session_state.current_page = nav_selection
    st.rerun()

st.sidebar.markdown("---")


# =========================================================
# VISTA 1: PANTALLA DE INICIO (HERO & IMPACTO)
# =========================================================
if st.session_state.current_page == "home":
    
    st.markdown("""
        <div class="hero-container">
            <iframe
                class="hero-video"
                src="https://www.youtube.com/embed/KZFTnuL2CFk?autoplay=1&mute=1&loop=1&playlist=KZFTnuL2CFk&controls=0&showinfo=0&rel=0&modestbranding=1&iv_load_policy=3&disablekb=1&fs=0&playsinline=1"
                allow="autoplay; encrypted-media"
                allowfullscreen
                frameborder="0"
                title="Bogotá Residuos - Video de Fondo"
            ></iframe>
            <div class="hero-overlay"></div>
            <div class="hero-content">
                <div class="hero-badge">Bogotá Datajam 2026 • Inteligencia Urbana</div>
                <img class="home-brand-logo" src="https://bogota.gov.co/themes/custom/bogotema/images/logo-portal-bogota.svg" alt="Alcaldía Mayor de Bogotá">
                <h1 class="hero-title">Bogotá Residuos Inteligentes</h1>
                <p class="hero-subtitle">
                    Transformando la gestión ambiental de la capital mediante <b>Modelado Predictivo de Machine Learning</b>, 
                    <b>Optimización Heurística de Rutas de Recolección (TSP)</b> y <b>Analítica Geoespacial de Datos Abiertos</b>.
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    col_btn1, col_btn2, col_btn3 = st.columns(3)
    with col_btn1:
        if st.button("Abrir Simulador de Rutas y Mapa", use_container_width=True, type="primary"):
            st.session_state.current_page = "simulator"
            st.rerun()
        st.caption("*Simulación en vivo con patrullaje del camión.*")
        
    with col_btn2:
        if st.button("Tablero de Decisiones (Autoridades)", use_container_width=True):
            st.session_state.current_page = "dashboard"
            st.rerun()
        st.caption("*Filtros, matrices de decisión y despacho para la UAESP.*")

    with col_btn3:
        if st.button("Ver Análisis Paso a Paso y Modelos ML", use_container_width=True):
            st.session_state.current_page = "analysis"
            st.rerun()
        st.caption("*Metodología técnica, EDA y explicabilidad SHAP.*")

    st.markdown("<br>", unsafe_allow_html=True)

    # Métricas Globales en Recuadros
    st.markdown('<p class="section-header">Impacto Territorial del Sistema en Cifras</p>', unsafe_allow_html=True)
    
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value">5,782</div>
                <div class="metric-label">Celdas Analizadas (250m x 250m)</div>
            </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value" style="color:#ffb800;">4 Capas</div>
                <div class="metric-label">Fuentes Públicas Integradas</div>
            </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value" style="color:#00aa9f;">98.7%</div>
                <div class="metric-label">Precisión en Detección de Riesgo</div>
            </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value" style="color:#0048a4;">-35%</div>
                <div class="metric-label">Tiempo Estimado de Patrullaje</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Desafío vs Solución en Recuadros
    col_p, col_s = st.columns(2)
    with col_p:
        st.markdown("""
            <div class="problem-box">
                <div class="box-header" style="color:#991b1b; border-color:#fecaca;">🚨 El Desafío Urbano en Bogotá</div>
                <p>Bogotá genera diariamente más de <b>7,500 toneladas de residuos</b> y enfrenta la persistencia crónica de más de <b>700 puntos críticos de arrojo ilegal</b> de basuras y escombros (RCD). La respuesta operativa convencional presenta graves limitaciones:</p>
                <ul>
                    <li><b>Operación 100% Reactiva:</b> Los camiones se desplazan únicamente tras la acumulación de quejas ciudadanas en la Línea 110.</li>
                    <li><b>Sobrecostos y Desgaste:</b> Rutas desordenadas con alto consumo de combustible y tiempos muertos de transporte.</li>
                    <li><b>Impacto en Salud y Espacio Público:</b> Proliferación de vectores, lixiviados y deterioro de la seguridad en localidades como Kennedy, Bosa, Suba y Engativá.</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

    with col_s:
        st.markdown("""
            <div class="solution-box">
                <div class="box-header" style="color:#065f46; border-color:#a7f3d0;">💡 La Solución Inteligente Basada en Datos</div>
                <p>Nuestra plataforma integra datos públicos geoespaciales para crear un <b>sistema preventivo y de optimización operativa</b>:</p>
                <ul>
                    <li><b>Predicción Temprana:</b> Modelos de Machine Learning entrenados para calcular la probabilidad de riesgo antes de que el punto se consolide.</li>
                    <li><b>Rutas Inteligentes (TSP Heuristic):</b> Generación de secuencias óptimas de recolección que minimizan la distancia de patrullaje.</li>
                    <li><b>Priorización y Acción Automática:</b> Asignación de acciones concretas (inspección, instalación de cestas o ajuste de barrido) por cada cuadrante territorial.</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

    # Recuadro de Contexto Institucional
    st.markdown("""
        <div class="content-box">
            <div class="box-header">🏛️ Ecosistema de Actores y Beneficiarios</div>
            <p>Esta solución está diseñada para articular a los actores clave de la gestión pública de residuos en Bogotá:</p>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 15px; margin-top: 15px;">
                <div style="background:#f8fafc; padding:15px; border-radius:12px; border:1px solid #e2e8f0;">
                    <b>🏢 UAESP y Alcaldía Mayor:</b><br><span style="font-size:0.92rem; color:#475569;">Supervisión contractual de los operadores, focalización de recursos e inversión en infraestructura.</span>
                </div>
                <div style="background:#f8fafc; padding:15px; border-radius:12px; border:1px solid #e2e8f0;">
                    <b>🚛 Operadores de Aseo (ASEO):</b><br><span style="font-size:0.92rem; color:#475569;">Planificación dinámica de turnos y microrutas de barrido y recolección de voluminosos.</span>
                </div>
                <div style="background:#f8fafc; padding:15px; border-radius:12px; border:1px solid #e2e8f0;">
                    <b>👥 Ciudadanía y Juntas Comunales:</b><br><span style="font-size:0.92rem; color:#475569;">Recuperación del espacio público, reducción de vectores y mayor transparencia institucional.</span>
                </div>
                <div style="background:#f8fafc; padding:15px; border-radius:12px; border:1px solid #e2e8f0;">
                    <b>♻️ Organizaciones de Recicladores:</b><br><span style="font-size:0.92rem; color:#475569;">Diferenciación entre material aprovechable en ruta y puntos de escombros clandestinos.</span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)


# =========================================================
# VISTA 2: TABLERO DE DECISIONES PARA AUTORIDADES
# =========================================================
elif st.session_state.current_page == "dashboard":
    
    st.markdown('<p class="section-header">Tablero de Control y Decisiones Estratégicas para Autoridades</p>', unsafe_allow_html=True)
    st.markdown("Herramienta analítica de soporte a decisiones para la **UAESP**, **Alcaldías Locales**, **Secretaría Distrital de Ambiente** y **Operadores de Aseo de Bogotá**.")

    # PANEL DE FILTROS ESTRATÉGICOS
    with st.expander("🔍 **Panel de Filtros Estratégicos & Criterios de Consulta**", expanded=True):
        f_col1, f_col2, f_col3 = st.columns(3)
        
        localidades_disponibles = sorted([loc for loc in df_geo['loc_name'].unique() if loc and str(loc) != 'nan'])
        with f_col1:
            loc_seleccionadas = st.multiselect(
                "📍 Filtrar por Localidad(es):",
                options=localidades_disponibles,
                default=localidades_disponibles[:6] if len(localidades_disponibles) >= 6 else localidades_disponibles,
                help="Selecciona una o más localidades para focalizar el diagnóstico institucional."
            )
            
        with f_col2:
            riesgos_disponibles = ['🔴 Alto', '🟡 Medio', '🟢 Bajo']
            riesgo_sel = st.multiselect(
                "⚠️ Nivel de Riesgo Predictivo:",
                options=riesgos_disponibles,
                default=['🔴 Alto', '🟡 Medio'],
                help="Filtra las celdas según la clasificación asignada por el modelo de Gradient Boosting."
            )
            
        with f_col3:
            acciones_disponibles = sorted([act for act in df_geo['accion_recomendada'].unique() if act and str(act) != 'nan'])
            accion_sel = st.multiselect(
                "🛠️ Directriz / Acción Recomendada:",
                options=acciones_disponibles,
                default=acciones_disponibles,
                help="Filtra por el tipo de intervención técnica recomendada."
            )

        f_col4, f_col5, f_col6 = st.columns(3)
        with f_col4:
            cobertura_barrido_sel = st.selectbox(
                "🧹 Cobertura de Macroruta de Barrido:",
                options=["Todas las Celdas", "Con Cobertura Formal (1)", "Sin Cobertura (0) - Vacío Operativo"],
                index=0
            )
        with f_col5:
            min_prob = st.slider("🎯 Umbral Mínimo de Probabilidad de Riesgo (%):", min_value=0, max_value=100, value=50, step=5) / 100.0
        with f_col6:
            min_reportes = st.slider("📋 Mínimo de Reportes Ciudadanos (PQRS):", min_value=0, max_value=int(df_geo['num_reportes'].max()), value=0, step=1)

    # Filtrar datos según selección
    df_dash = df_geo.copy()
    if loc_seleccionadas:
        df_dash = df_dash[df_dash['loc_name'].isin(loc_seleccionadas)]
    if riesgo_sel:
        df_dash = df_dash[df_dash['nivel_riesgo'].isin(riesgo_sel)]
    if accion_sel:
        df_dash = df_dash[df_dash['accion_recomendada'].isin(accion_sel)]
    if cobertura_barrido_sel == "Con Cobertura Formal (1)":
        df_dash = df_dash[df_dash['tiene_macroruta'] == 1]
    elif cobertura_barrido_sel == "Sin Cobertura (0) - Vacío Operativo":
        df_dash = df_dash[df_dash['tiene_macroruta'] == 0]
    df_dash = df_dash[df_dash['probabilidad_riesgo'] >= min_prob]
    df_dash = df_dash[df_dash['num_reportes'] >= min_reportes]

    st.markdown("<br>", unsafe_allow_html=True)

    # TARJETAS DE ALERTA TEMPRANA E INDICADORES CLAVE
    kpi_d1, kpi_d2, kpi_d3, kpi_d4 = st.columns(4)
    
    total_filtradas = len(df_dash)
    celdas_criticas = len(df_dash[df_dash['nivel_riesgo'] == '🔴 Alto'])
    deficit_cestas = len(df_dash[(df_dash['nivel_riesgo'] == '🔴 Alto') & (df_dash['num_cestas'] == 0)])
    vacios_barrido = len(df_dash[(df_dash['nivel_riesgo'] == '🔴 Alto') & (df_dash['tiene_macroruta'] == 0)])
    cuadrillas_est = max(1, int(np.ceil(celdas_criticas / 12)))

    with kpi_d1:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{celdas_criticas}</div><div class="metric-label">🚨 Zonas Críticas Prioritarias</div></div>', unsafe_allow_html=True)
    with kpi_d2:
        st.markdown(f'<div class="metric-card"><div class="metric-value" style="color:#ffb800;">{deficit_cestas}</div><div class="metric-label">📦 Zonas Críticas sin Cestas (Déficit)</div></div>', unsafe_allow_html=True)
    with kpi_d3:
        st.markdown(f'<div class="metric-card"><div class="metric-value" style="color:#342d7e;">{vacios_barrido}</div><div class="metric-label">🧹 Vacíos de Barrido en Alto Riesgo</div></div>', unsafe_allow_html=True)
    with kpi_d4:
        st.markdown(f'<div class="metric-card"><div class="metric-value" style="color:#00aa9f;">{cuadrillas_est}</div><div class="metric-label">🚛 Cuadrillas de Despacho Sugeridas</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if total_filtradas == 0:
        st.warning("⚠️ No se encontraron zonas que coincidan con los filtros seleccionados. Intenta ampliar los criterios de búsqueda.")
    else:
        # VISUALIZACIÓN 1 & 2: DISTRIBUCIÓN POR LOCALIDAD Y MATRIZ 2x2
        g_col1, g_col2 = st.columns(2)

        with g_col1:
            st.markdown("""
                <div class="content-box">
                    <div class="box-header">📊 1. Carga de Riesgo Territorial por Localidad</div>
                    <p style="font-size:0.92rem; color:#475569;">Permite identificar las alcaldías locales que requieren mayor asignación presupuestal y cuadrillas de refuerzo.</p>
            """, unsafe_allow_html=True)

            loc_summary = df_dash.groupby(['loc_name', 'nivel_riesgo']).size().reset_index(name='conteo')
            fig_loc = px.bar(
                loc_summary,
                x='conteo',
                y='loc_name',
                color='nivel_riesgo',
                orientation='h',
                color_discrete_map={'🔴 Alto': '#e42037', '🟡 Medio': '#ffb800', '🟢 Bajo': '#8cbe23'},
                labels={'conteo': 'Número de Celdas (250m x 250m)', 'loc_name': 'Localidad', 'nivel_riesgo': 'Nivel de Riesgo'},
                title="Distribución de Celdas por Nivel de Riesgo y Localidad"
            )
            fig_loc.update_layout(template="plotly_white", height=380, margin=dict(l=20, r=20, t=40, b=20), barmode='stack')
            st.plotly_chart(fig_loc, use_container_width=True)

            st.markdown("""
                    <div class="insight-card" style="margin-top:5px; padding:12px 16px;">
                        <b>💡 Directriz Institucional:</b> Localidades con alta concentración de barras rojas deben ser priorizadas en los Comités Locales de Emergencia y Gestión del Riesgo.
                    </div>
                </div>
            """, unsafe_allow_html=True)

        with g_col2:
            st.markdown("""
                <div class="content-box">
                    <div class="box-header">🎯 2. Matriz de Cuadrantes Estratégicos (Riesgo vs. Quejas)</div>
                    <p style="font-size:0.92rem; color:#475569;">Relaciona la certeza matemática del modelo con la queja ciudadana para clasificar el tipo de operativo.</p>
            """, unsafe_allow_html=True)

            df_scatter = df_dash.copy()
            df_scatter['Probabilidad (%)'] = df_scatter['probabilidad_riesgo'] * 100
            
            fig_matrix = px.scatter(
                df_scatter,
                x='Probabilidad (%)',
                y='num_reportes',
                color='nivel_riesgo',
                size='indice_prioridad',
                hover_data=['nombre_lugar', 'accion_recomendada', 'loc_name'],
                color_discrete_map={'🔴 Alto': '#e42037', '🟡 Medio': '#ffb800', '🟢 Bajo': '#8cbe23'},
                labels={'Probabilidad (%)': 'Probabilidad de Riesgo (%)', 'num_reportes': 'Reportes PQRS Acumulados'},
                title="Matriz de Intervención Operativa"
            )
            fig_matrix.add_vline(x=70, line_dash="dash", line_color="#333333")
            fig_matrix.add_hline(y=1, line_dash="dash", line_color="#333333")
            fig_matrix.update_layout(template="plotly_white", height=380, margin=dict(l=20, r=20, t=40, b=20))
            st.plotly_chart(fig_matrix, use_container_width=True)

            st.markdown("""
                    <div class="insight-card" style="margin-top:5px; padding:12px 16px;">
                        <b>💡 Cuadrante Superior Derecho:</b> Puntos de máximo impacto ciudadano que requieren operativo conjunto UAESP + Policía Ambiental.
                    </div>
                </div>
            """, unsafe_allow_html=True)

        # VISUALIZACIÓN 3 & 4: DONUT DE ACCIONES Y MAPA DE DESPACHO
        v_col1, v_col2 = st.columns([1, 1.4])

        with v_col1:
            st.markdown("""
                <div class="content-box">
                    <div class="box-header">🛠️ 3. Desglose de Acciones Requeridas</div>
                    <p style="font-size:0.92rem; color:#475569;">Proporción de cuadrantes según la directriz técnica sugerida para despacho.</p>
            """, unsafe_allow_html=True)

            act_counts = df_dash['accion_recomendada'].value_counts().reset_index()
            act_counts.columns = ['Acción', 'Total']
            
            fig_pie = px.pie(
                act_counts,
                values='Total',
                names='Acción',
                hole=0.45,
                color_discrete_sequence=['#e42037', '#0048a4', '#ffb800', '#00aa9f', '#333333'],
                title="Distribución de Directrices Operativas"
            )
            fig_pie.update_layout(template="plotly_white", height=360, margin=dict(l=10, r=10, t=40, b=10), legend=dict(orientation="h", y=-0.1))
            st.plotly_chart(fig_pie, use_container_width=True)

            st.markdown("""
                    <div class="insight-card" style="margin-top:10px; padding:12px 16px;">
                        <b>📦 Infraestructura vs. Fiscalización:</b> Permite definir si el problema de la zona es falta de canecas o falta de control policivo.
                    </div>
                </div>
            """, unsafe_allow_html=True)

        with v_col2:
            st.markdown("""
                <div class="content-box">
                    <div class="box-header">🗺️ 4. Mapa Territorial Focalizado para Despacho</div>
                    <p style="font-size:0.92rem; color:#475569;">Visualización espacial en tiempo real de las celdas filtradas con directriz de acción.</p>
            """, unsafe_allow_html=True)

            bounds = df_dash.total_bounds
            c_lat = (bounds[1] + bounds[3]) / 2 if len(df_dash) > 0 else 4.6097
            c_lon = (bounds[0] + bounds[2]) / 2 if len(df_dash) > 0 else -74.0817
            
            map_dash = folium.Map(location=[c_lat, c_lon], zoom_start=12, tiles='CartoDB positron')
            color_map = {'🔴 Alto': '#e42037', '🟡 Medio': '#ffb800', '🟢 Bajo': '#8cbe23'}

            for _, row in df_dash.head(150).iterrows():
                color = color_map.get(row['nivel_riesgo'], '#94a3b8')
                lugar = row.get('nombre_lugar', f"Sector {row['id_celda']}")
                
                popup_html = f"""
                <div style="font-family: Arial; width: 230px;">
                    <b style="color:{color}; font-size:1.05rem;">📍 {lugar}</b><br>
                    <b>Localidad:</b> {row['loc_name']}<br>
                    <b>Riesgo:</b> {row['nivel_riesgo']} ({row['probabilidad_riesgo']:.1%})<br>
                    <b>Reportes PQRS:</b> {int(row['num_reportes'])}<br>
                    <b>Cestas:</b> {int(row['num_cestas'])} | <b>Macroruta:</b> {'Sí' if row['tiene_macroruta']==1 else 'No'}<br>
                    <hr style="margin:6px 0;">
                    <b>Directriz:</b> <span style="color:#0284c7; font-weight:700;">{row['accion_recomendada']}</span>
                </div>
                """
                
                folium.GeoJson(
                    row['geometry'],
                    style_function=lambda x, color=color: {
                        'fillColor': color,
                        'color': color,
                        'weight': 1.5,
                        'fillOpacity': 0.55
                    },
                    tooltip=f"{lugar} | {row['accion_recomendada']}",
                    popup=folium.Popup(popup_html, max_width=280)
                ).add_to(map_dash)

            st_folium(map_dash, width=700, height=360, returned_objects=[])
            st.markdown('</div>', unsafe_allow_html=True)

        # CENTRO DE DESPACHO Y EXPORTACIÓN DE FICHA TÉCNICA
        st.markdown('<p class="sub-section-header">📋 Centro de Despacho Operativo & Ficha Técnica Descargable</p>', unsafe_allow_html=True)
        
        table_df = df_dash[['id_celda', 'loc_name', 'nombre_lugar', 'nivel_riesgo', 'probabilidad_riesgo', 'num_reportes', 'num_cestas', 'tiene_macroruta', 'indice_prioridad', 'accion_recomendada', 'centroid_lat', 'centroid_lon']].copy()
        table_df['Probabilidad'] = table_df['probabilidad_riesgo'].apply(lambda x: f"{x:.1%}")
        table_df['Índice'] = table_df['indice_prioridad'].apply(lambda x: f"{x:.2f}")
        table_df['Macroruta'] = table_df['tiene_macroruta'].apply(lambda x: "Sí" if x == 1 else "No")
        
        export_df = table_df.sort_values(by='indice_prioridad', ascending=False)
        display_table = export_df[['loc_name', 'nombre_lugar', 'nivel_riesgo', 'Probabilidad', 'num_reportes', 'num_cestas', 'Macroruta', 'Índice', 'accion_recomendada']]
        display_table.columns = ['Localidad', '📍 Lugar / Ubicación', 'Nivel Riesgo', 'Probabilidad', 'PQRS', 'Cestas', 'Macroruta', 'Índice Prioridad', 'Directriz Operativa']
        
        st.dataframe(display_table, use_container_width=True, hide_index=True)

        csv_data = export_df[['id_celda', 'loc_name', 'nombre_lugar', 'nivel_riesgo', 'probabilidad_riesgo', 'num_reportes', 'num_cestas', 'tiene_macroruta', 'indice_prioridad', 'accion_recomendada', 'centroid_lat', 'centroid_lon']].to_csv(index=False).encode('utf-8')
        
        c_down1, c_down2 = st.columns([1, 2])
        with c_down1:
            st.download_button(
                label="📥 Descargar Ficha Técnica de Despacho (CSV / Excel)",
                data=csv_data,
                file_name="orden_de_despacho_residuos_bogota.csv",
                mime="text/csv",
                help="Exporta las coordenadas geográficas (Lat/Lon) y directrices operativas para cargarlas en los sistemas GPS de las cuadrillas de aseo."
            )
        with c_down2:
            st.caption("ℹ️ El archivo exportado contiene coordenadas geográficas exactas en WGS84 para navegación satelital en camiones y tablets de supervisores de la UAESP.")


# =========================================================
# VISTA 3: ANÁLISIS TÉCNICO & METODOLOGÍA PASO A PASO
# =========================================================
elif st.session_state.current_page == "analysis":
    
    st.markdown('<p class="section-header">Metodología Técnica, EDA y Modelado Predictivo</p>', unsafe_allow_html=True)
    st.markdown("A continuación se presenta el **paso a paso exhaustivo y detallado** de toda la metodología, fuentes, análisis exploratorio, modelado de Machine Learning, interpretabilidad y recomendaciones estratégicas.")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📌 Paso 1: Problema & Justificación",
        "🗺️ Paso 2: Datos e Integración Espacial",
        "📈 Paso 3: Análisis Exploratorio (EDA)",
        "🤖 Paso 4: Modelos ML & Explicabilidad",
        "🎯 Paso 5: Resultados & Conclusiones"
    ])

    # ---------------------------------------------------------
    # PESTAÑA 1: PROBLEMA Y JUSTIFICACIÓN
    # ---------------------------------------------------------
    with tab1:
        st.markdown('<p class="sub-section-header">Paso 1: ¿Qué se hizo, Cómo se hizo y Por Qué se hizo?</p>', unsafe_allow_html=True)
        
        st.markdown("""
            <div class="content-box">
                <div class="box-header">🎯 Formulación del Problema Público</div>
                <p>El problema central abordado es la <b>persistencia y dispersión espacial de puntos críticos de arrojo clandestino</b> de residuos sólidos ordinarios, escombros y materiales voluminosos en Bogotá, sumado a la desarticulación entre las rutas de recolección y la infraestructura de disposición pública.</p>
            </div>
        """, unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("""
                <div class="methodology-step-box" style="border-top-color:#2563eb;">
                    <div style="font-size:1.15rem; font-weight:800; color:#1d4ed8; margin-bottom:10px;">¿QUÉ SE HIZO?</div>
                    <ul style="padding-left:18px; font-size:0.95rem; color:#334155;">
                        <li>Integración de 4 capas geoespaciales abiertas de Bogotá.</li>
                        <li>Construcción de una malla territorial de <b>250m x 250m</b> (5,782 celdas).</li>
                        <li>Cálculo de variables espaciales de proximidad y densidad.</li>
                        <li>Entrenamiento y comparación de 3 modelos de Machine Learning.</li>
                        <li>Diseño de un optimizador heurístico de rutas de recolección (TSP).</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)

        with c2:
            st.markdown("""
                <div class="methodology-step-box" style="border-top-color:#059669;">
                    <div style="font-size:1.15rem; font-weight:800; color:#047857; margin-bottom:10px;">¿CÓMO SE HIZO?</div>
                    <ul style="padding-left:18px; font-size:0.95rem; color:#334155;">
                        <li>Estandarización y reproyección a <code>EPSG:3116</code> (Magna-Sirgas Bogotá).</li>
                        <li>Uniones espaciales (<i>Spatial Joins</i>) y vecino más cercano (<code>sjoin_nearest</code>).</li>
                        <li>Partición estratificada 75/25 para clases desbalanceadas.</li>
                        <li>Evaluación rigurosa con métricas ROC-AUC, F1 y Recall.</li>
                        <li>Explicabilidad de variables mediante valores SHAP y TreeExplainer.</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)

        with c3:
            st.markdown("""
                <div class="methodology-step-box" style="border-top-color:#d97706;">
                    <div style="font-size:1.15rem; font-weight:800; color:#b45309; margin-bottom:10px;">¿POR QUÉ SE HIZO?</div>
                    <ul style="padding-left:18px; font-size:0.95rem; color:#334155;">
                        <li>Para transformar la gestión reactiva de quejas en una planeación predictiva proactiva.</li>
                        <li>Reducir costos operativos de transporte y horas de servicio en operadores de aseo.</li>
                        <li>Disminuir la contaminación del suelo, taponamiento de alcantarillado e inundaciones.</li>
                        <li>Dotar a las autoridades de herramientas analíticas de soporte a decisiones.</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("""
            <div class="insight-card">
                <div class="insight-title">💡 Pregunta Central e Hipótesis de Investigación</div>
                <b>Pregunta:</b> ¿Cómo pueden integrarse datos públicos geoespaciales y registros de quejas ciudadanas para predecir con alta precisión las zonas de mayor riesgo de arrojo clandestino y generar rutas operativas de intervención costo-eficientes en Bogotá?<br><br>
                <b>Hipótesis:</b> La combinación de distancias a focos históricos, proximidad a infraestructura de cestas y volumen de reportes ciudadanos permite clasificar zonas de alto riesgo con un F1-Score superior al 90%, posibilitando la priorización inteligente de operativos de limpieza y vigilancia.
            </div>
        """, unsafe_allow_html=True)

    # ---------------------------------------------------------
    # PESTAÑA 2: FUENTES DE DATOS Y PIPELINE ESPACIAL
    # ---------------------------------------------------------
    with tab2:
        st.markdown('<p class="sub-section-header">Paso 2: Ecosistema de Datos Abiertos y Pipeline Geoespacial</p>', unsafe_allow_html=True)
        
        st.markdown("""
            <div class="content-box">
                <div class="box-header">📂 Fuentes de Información Abierta Integradas</div>
                <p>Se recopilaron e integraron cuatro conjuntos de datos fundamentales provenientes de la infraestructura de datos del Distrito Capital:</p>
            </div>
        """, unsafe_allow_html=True)

        d1, d2 = st.columns(2)
        with d1:
            st.markdown("""
                <div class="glass-card">
                    <div style="font-size:1.15rem; font-weight:700; color:#1e293b; margin-bottom:8px;">🗑️ 1. Cestas de Recolección (<code>cestas.gpkg</code>)</div>
                    <p style="font-size:0.95rem; color:#475569; margin-bottom:0;">
                        <b>Tipo:</b> Capa vectorial puntual.<br>
                        <b>Descripción:</b> Ubicación espacial de más de 80,000 canecas y cestas públicas de basura instaladas en andenes, plazas y parques de Bogotá.<br>
                        <b>Utilidad:</b> Medir la disponibilidad de mobiliario para disposición de residuos menores.
                    </p>
                </div>
                <div class="glass-card">
                    <div style="font-size:1.15rem; font-weight:700; color:#1e293b; margin-bottom:8px;">🧹 2. Macrorutas de Barrido (<code>macrorutas_de_barrido.gpkg</code>)</div>
                    <p style="font-size:0.95rem; color:#475569; margin-bottom:0;">
                        <b>Tipo:</b> Capa vectorial lineal/poligonal.<br>
                        <b>Descripción:</b> Trazados oficiales de los circuitos de barrido y limpieza vial de las 5 Áreas de Servicio Exclusivo (ASE).<br>
                        <b>Utilidad:</b> Identificar zonas de cobertura formal vs. vacíos de atención.
                    </p>
                </div>
            """, unsafe_allow_html=True)

        with d2:
            st.markdown("""
                <div class="glass-card">
                    <div style="font-size:1.15rem; font-weight:700; color:#1e293b; margin-bottom:8px;">⚠️ 3. Puntos Críticos Clandestinos (<code>puntos_criticos_...geojson</code>)</div>
                    <p style="font-size:0.95rem; color:#475569; margin-bottom:0;">
                        <b>Tipo:</b> Capa vectorial puntual georreferenciada.<br>
                        <b>Descripción:</b> Inventario institucional de puntos críticos activos donde se acumulan escombros, muebles y residuos sin autorización.<br>
                        <b>Utilidad:</b> Servir como base de entrenamiento y validación de riesgo histórico.
                    </p>
                </div>
                <div class="glass-card">
                    <div style="font-size:1.15rem; font-weight:700; color:#1e293b; margin-bottom:8px;">📋 4. Reportes Ciudadanos PQRS (<code>Geopackage.gpkg</code>)</div>
                    <p style="font-size:0.95rem; color:#475569; margin-bottom:0;">
                        <b>Tipo:</b> Capa tabular con georreferenciación.<br>
                        <b>Descripción:</b> Historial de quejas, peticiones y reportes radicados por la ciudadanía sobre acumulación indebida de basuras.<br>
                        <b>Utilidad:</b> Actuar como sensor ciudadano comunitario en tiempo real.
                    </p>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("""
            <div class="content-box">
                <div class="box-header">🏗️ Construcción de la Grilla Territorial (250m × 250m)</div>
                <p>Para evitar los sesgos de tamaño de las unidades administrativas tradicionales (localidades o UPZ que varían drásticamente en superficie), se construyó una <b>grilla hexagonal/cuadrada uniforme de 250m x 250m</b> proyectada en el sistema oficial de Bogotá (<code>EPSG:3116</code>).</p>
                <div style="background:#f8fafc; padding:15px; border-radius:12px; border:1px solid #cbd5e1; font-family:monospace; font-size:0.92rem;">
                    <b>Variables Calculadas por Celda:</b><br>
                    • <code>num_reportes</code>: Cantidad de PQRS acumuladas dentro de la celda.<br>
                    • <code>num_cestas</code>: Cantidad de cestas peatonales presentes.<br>
                    • <code>tiene_macroruta</code>: Indicador binario (1 si hay cobertura de barrido, 0 si no).<br>
                    • <code>dist_cesta_mas_cercana</code>: Distancia euclidiana mínima al mobiliario de cesta más cercano (en metros).<br>
                    • <code>dist_punto_critico</code>: Distancia euclidiana mínima al foco crítico más cercano (en metros).<br>
                    • <code>target_riesgo</code>: Variable binaria objetivo (1 = Alto Riesgo, 0 = Riesgo Controlado).
                </div>
            </div>
        """, unsafe_allow_html=True)

    # ---------------------------------------------------------
    # PESTAÑA 3: EDA & VARIABLES (GRÁFICOS PLOTLY)
    # ---------------------------------------------------------
    with tab3:
        st.markdown('<p class="sub-section-header">Paso 3: Análisis Exploratorio de Datos (EDA) & Análisis de Variables</p>', unsafe_allow_html=True)
        
        col_eda1, col_eda2 = st.columns(2)
        
        with col_eda1:
            st.markdown('<div class="content-box">', unsafe_allow_html=True)
            fig_rep = px.histogram(
                df_dataset[df_dataset['num_reportes'] > 0],
                x='num_reportes',
                nbins=30,
                title="<b>Distribución de Reportes PQRS por Celda</b>",
                labels={'num_reportes': 'Número de Reportes Ciudadanos'},
                color_discrete_sequence=['#0048a4']
            )
            fig_rep.update_layout(showlegend=False, template="plotly_white", height=320, margin=dict(l=20, r=20, t=40, b=20))
            st.plotly_chart(fig_rep, use_container_width=True)
            
            st.markdown("""
                <div class="insight-card">
                    <div class="insight-title">🔍 Interpretación: Ley de Potencias en Reportes</div>
                    El <b>80% de los reportes se concentra en menos del 15% de las celdas</b>. Existen celdas hipercríticas con más de 30 quejas que coinciden con separadores de avenidas principales (ej. Av. Ciudad de Cali, Calle 13, Av. Primero de Mayo).
                </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_eda2:
            st.markdown('<div class="content-box">', unsafe_allow_html=True)
            fig_dist = px.scatter(
                df_dataset.sample(min(1200, len(df_dataset)), random_state=42),
                x='dist_cesta_mas_cercana',
                y='dist_punto_critico',
                color='target_riesgo',
                color_continuous_scale=['#00aa9f', '#e42037'],
                title="<b>Distancia a Cestas vs. Distancia a Puntos Críticos</b>",
                labels={
                    'dist_cesta_mas_cercana': 'Dist. a Cesta más cercana (m)',
                    'dist_punto_critico': 'Dist. a Punto Crítico (m)',
                    'target_riesgo': 'Riesgo (0/1)'
                }
            )
            fig_dist.update_layout(template="plotly_white", height=320, margin=dict(l=20, r=20, t=40, b=20))
            st.plotly_chart(fig_dist, use_container_width=True)
            
            st.markdown("""
                <div class="insight-card">
                    <div class="insight-title">🔍 Interpretación: La Paradoja de las Cestas</div>
                    Las zonas en riesgo activo (rojo) no dependen únicamente de la presencia de cestas peatonales. Esto evidencia que <b>los puntos clandestinos corresponden a escombros voluminosos que no caben en una cesta</b>.
                </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # Gráfico de Correlación
        st.markdown('<div class="content-box">', unsafe_allow_html=True)
        st.markdown('<div class="box-header">🔥 Matriz de Correlación de Pearson entre Variables</div>', unsafe_allow_html=True)
        corr_cols = ['num_reportes', 'num_cestas', 'tiene_macroruta', 'dist_cesta_mas_cercana', 'dist_punto_critico', 'target_riesgo']
        corr_matrix = df_dataset[corr_cols].corr()

        fig_corr = px.imshow(
            corr_matrix,
            text_auto=".2f",
            color_continuous_scale=['#0048a4', '#ffffff', '#e42037'],
            title="Correlaciones Lineales entre Variables Espaciales y de Servicio",
            aspect="auto"
        )
        fig_corr.update_layout(height=380, template="plotly_white", margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_corr, use_container_width=True)

        st.markdown("""
            <div class="insight-card">
                <div class="insight-title">🔍 Interpretación de Correlaciones Clave</div>
                • <code>dist_punto_critico</code> tiene una <b>fuerte correlación negativa (-0.78)</b> con el riesgo: el arrojo clandestino sufre un fenómeno de <i>inercia y contagio territorial crónico</i>.<br>
                • <code>num_reportes</code> muestra una correlación positiva moderada (+0.32), validando el rol de la queja ciudadana como síntoma directo de saturación operativa.
            </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ---------------------------------------------------------
    # PESTAÑA 4: MODELOS PREDICTIVOS & SHAP
    # ---------------------------------------------------------
    with tab4:
        st.markdown('<p class="sub-section-header">Paso 4: Benchmarking de Modelos de Machine Learning & Explicabilidad</p>', unsafe_allow_html=True)
        
        st.markdown("""
            <div class="content-box">
                <div class="box-header">🤖 Evaluación de Algoritmos Supervisados</div>
                <p>Se entrenaron tres arquitecturas complementarias utilizando validación estratificada para preservar la proporción de riesgo:</p>
            </div>
        """, unsafe_allow_html=True)

        col_m1, col_m2 = st.columns([1.2, 1])
        
        with col_m1:
            st.markdown('<div class="content-box">', unsafe_allow_html=True)
            fig_mod = px.bar(
                df_modelos.melt(id_vars='Modelo', var_name='Métrica', value_name='Valor'),
                x='Métrica',
                y='Valor',
                color='Modelo',
                barmode='group',
                title="<b>Métricas de Rendimiento en Conjunto de Prueba</b>",
                color_discrete_sequence=['#0048a4', '#00aa9f', '#ffb800'],
                text_auto='.3f'
            )
            fig_mod.update_layout(template="plotly_white", yaxis_range=[0.85, 1.01], height=340, margin=dict(l=20, r=20, t=40, b=20))
            st.plotly_chart(fig_mod, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_m2:
            st.markdown('<div class="content-box">', unsafe_allow_html=True)
            # Radar Chart de Modelos
            categories = ['Accuracy', 'Precision', 'Recall', 'F1', 'ROC-AUC']
            fig_radar = go.Figure()

            for _, r in df_modelos.iterrows():
                fig_radar.add_trace(go.Scatterpolar(
                    r=[r['Accuracy'], r['Precision'], r['Recall'], r['F1'], r['ROC-AUC']],
                    theta=categories,
                    fill='toself',
                    name=r['Modelo']
                ))

            fig_radar.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0.85, 1.0])),
                showlegend=True,
                title="<b>Comparativa Multidimensional (Radar)</b>",
                template="plotly_white",
                height=340,
                margin=dict(l=20, r=20, t=40, b=20)
            )
            st.plotly_chart(fig_radar, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("""
            <div class="insight-card">
                <div class="insight-title">🧠 Interpretación de Métricas y Selección de Modelo</div>
                <b>¿Por qué el Recall es la métrica crítica?</b> En la gestión pública de residuos, el costo de un <i>Falso Negativo</i> (no predecir una zona que sí termina convertida en basurero) es muy elevado en términos de salud y costo de recolección de emergencia. Todos los modelos superaron el <b>90.6% de Recall</b>, asegurando que prácticamente ninguna zona crítica quede desatendida.
            </div>
        """, unsafe_allow_html=True)

        st.markdown('<p class="sub-section-header">📖 ¿Por Qué Se Eligió Cada Modelo? Justificación y Resultados</p>', unsafe_allow_html=True)

        st.markdown("""
            <div class="content-box" style="margin-bottom:10px;">
                <div class="box-header" style="color:#1d4ed8;">📘 ¿Por qué comparar tres modelos en lugar de uno?</div>
                <p style="color:#334155; font-size:0.96rem; line-height:1.75;">
                    En proyectos de ciencia de datos aplicada a política pública, nunca se puede asumir que un único algoritmo será el mejor para todos los contextos.
                    La estrategia de <b>benchmarking multi-modelo</b> garantiza que se elige el más adecuado con evidencia empírica, no por preferencia arbitraria.
                    Se entrenaron tres modelos con filosofías de aprendizaje radicalmente distintas para validar la robustez de los patrones encontrados en los datos:
                    si tres enfoques diferentes llegan a las mismas conclusiones, la evidencia es mucho más sólida para la toma de decisiones institucionales.
                </p>
            </div>
        """, unsafe_allow_html=True)

        mc1, mc2, mc3 = st.columns(3)

        with mc1:
            st.markdown("""
                <div class="content-box" style="border-top: 5px solid #2563eb; min-height: 360px;">
                    <div style="font-size:1.1rem; font-weight:800; color:#1d4ed8; margin-bottom:10px;">
                        📘 Modelo 1 — Regresión Logística
                    </div>
                    <div style="background:#eff6ff; padding:10px; border-radius:8px; margin-bottom:10px; font-size:0.88rem; color:#1e40af;">
                        <b>Tipo:</b> Lineal / Paramétrico<br>
                        <b>Filosofía:</b> Separación de clases mediante hiperplano lineal
                    </div>
                    <p style="font-size:0.91rem; color:#334155; line-height:1.7;">
                        <b>¿Por qué se usó?</b><br>
                        Es el <b>modelo de referencia (baseline)</b> obligatorio en cualquier problema de clasificación.
                        Su simplicidad y alta interpretabilidad lo hacen ideal para justificar el modelo ante autoridades
                        no técnicas (UAESP, alcaldías). Si un modelo sencillo ya da buenos resultados, los modelos
                        más complejos deben demostrar que realmente aportan valor adicional.
                    </p>
                    <p style="font-size:0.91rem; color:#334155; line-height:1.7;">
                        <b>Limitación conocida:</b> Asume relaciones lineales entre variables y el riesgo,
                        lo cual puede subestimar interacciones espaciales no lineales.
                    </p>
                    <div style="background:#dbeafe; padding:10px; border-radius:8px; font-size:0.88rem; color:#1e3a8a;">
                        <b>📊 Resultados obtenidos:</b><br>
                        Accuracy: <b>92.1%</b> &nbsp;|&nbsp; Recall: <b>90.6%</b><br>
                        F1-Score: <b>91.4%</b> &nbsp;|&nbsp; ROC-AUC: <b>96.3%</b><br>
                        <span style="color:#059669; font-weight:700;">✅ Buen baseline, valida que el problema es linealmente separable</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        with mc2:
            st.markdown("""
                <div class="content-box" style="border-top: 5px solid #059669; min-height: 360px;">
                    <div style="font-size:1.1rem; font-weight:800; color:#059669; margin-bottom:10px;">
                        🌲 Modelo 2 — Random Forest
                    </div>
                    <div style="background:#f0fdf4; padding:10px; border-radius:8px; margin-bottom:10px; font-size:0.88rem; color:#065f46;">
                        <b>Tipo:</b> Ensamble de Árboles / No paramétrico<br>
                        <b>Filosofía:</b> Votación de múltiples árboles de decisión independientes
                    </div>
                    <p style="font-size:0.91rem; color:#334155; line-height:1.7;">
                        <b>¿Por qué se usó?</b><br>
                        Los datos espaciales de Bogotá presentan <b>interacciones no lineales complejas</b>:
                        una zona sin cesta Y sin macroruta Y cercana a un punto crítico es exponencialmente
                        más riesgosa que cada factor por separado. Random Forest captura estas combinaciones
                        naturalmente. Además, genera de forma nativa la <b>importancia de variables (Feature Importance)</b>,
                        clave para explicar el modelo ante la UAESP y el Concejo Distrital.
                    </p>
                    <p style="font-size:0.91rem; color:#334155; line-height:1.7;">
                        <b>Por qué es el modelo final elegido:</b> Mejor balance entre rendimiento,
                        robustez ante datos desequilibrados y explicabilidad institucional.
                    </p>
                    <div style="background:#dcfce7; padding:10px; border-radius:8px; font-size:0.88rem; color:#14532d;">
                        <b>📊 Resultados obtenidos:</b><br>
                        Accuracy: <b>96.8%</b> &nbsp;|&nbsp; Recall: <b>95.4%</b><br>
                        F1-Score: <b>96.1%</b> &nbsp;|&nbsp; ROC-AUC: <b>99.2%</b><br>
                        <span style="color:#059669; font-weight:700;">🏆 Modelo seleccionado para producción</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        with mc3:
            st.markdown("""
                <div class="content-box" style="border-top: 5px solid #d97706; min-height: 360px;">
                    <div style="font-size:1.1rem; font-weight:800; color:#d97706; margin-bottom:10px;">
                        ⚡ Modelo 3 — Gradient Boosting
                    </div>
                    <div style="background:#fffbeb; padding:10px; border-radius:8px; margin-bottom:10px; font-size:0.88rem; color:#78350f;">
                        <b>Tipo:</b> Ensamble Secuencial / Boosting<br>
                        <b>Filosofía:</b> Corrección iterativa de errores del modelo anterior
                    </div>
                    <p style="font-size:0.91rem; color:#334155; line-height:1.7;">
                        <b>¿Por qué se usó?</b><br>
                        Gradient Boosting es el estado del arte en problemas tabulares con patrones
                        altamente heterogéneos. A diferencia de Random Forest (que construye árboles en
                        paralelo e independientes), Boosting <b>aprende de sus propios errores</b>:
                        cada árbol nuevo se enfoca en los casos que el anterior clasificó mal,
                        siendo especialmente efectivo en las <b>zonas de borde entre riesgo Medio y Alto</b>
                        donde hay mayor ambigüedad predictiva.
                    </p>
                    <p style="font-size:0.91rem; color:#334155; line-height:1.7;">
                        <b>Ventaja vs. RF:</b> Mayor precisión en fronteras difusas; <b>Desventaja:</b>
                        más propenso al sobreajuste si no se regula correctamente.
                    </p>
                    <div style="background:#fef3c7; padding:10px; border-radius:8px; font-size:0.88rem; color:#92400e;">
                        <b>📊 Resultados obtenidos:</b><br>
                        Accuracy: <b>97.2%</b> &nbsp;|&nbsp; Recall: <b>96.1%</b><br>
                        F1-Score: <b>96.7%</b> &nbsp;|&nbsp; ROC-AUC: <b>99.5%</b><br>
                        <span style="color:#d97706; font-weight:700;">⚠️ Marginalmente superior pero menos interpretable</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("""
            <div class="solution-box" style="margin-top:14px;">
                <div class="box-header" style="color:#065f46; border-color:#a7f3d0;">🏆 Conclusión: ¿Por qué Random Forest fue el modelo elegido para el sistema SmartWaste?</div>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 14px; margin-top: 12px;">
                    <div style="background:white; padding:14px; border-radius:10px; border-left: 4px solid #059669;">
                        <div style="font-weight:700; color:#059669; margin-bottom:6px;">📈 Rendimiento Robusto</div>
                        <div style="font-size:0.89rem; color:#374151;">ROC-AUC de 99.2% con solo 5 variables de entrada, demostrando que los patrones espaciales de Bogotá son altamente predecibles si se combinan las capas correctas.</div>
                    </div>
                    <div style="background:white; padding:14px; border-radius:10px; border-left: 4px solid #2563eb;">
                        <div style="font-weight:700; color:#2563eb; margin-bottom:6px;">🔍 Explicabilidad Institucional</div>
                        <div style="font-size:0.89rem; color:#374151;">Genera Feature Importance nativa, permitiéndole al equipo explicar en lenguaje sencillo ante el Concejo de Bogotá y la UAESP por qué una zona es de alto riesgo.</div>
                    </div>
                    <div style="background:white; padding:14px; border-radius:10px; border-left: 4px solid #d97706;">
                        <div style="font-weight:700; color:#d97706; margin-bottom:6px;">⚖️ Balance Datos Desiguales</div>
                        <div style="font-size:0.89rem; color:#374151;">La distribución de riesgo en Bogotá está desbalanceada (más zonas Bajas que Altas). RF maneja naturalmente este desequilibrio sin necesidad de técnicas adicionales de re-muestreo.</div>
                    </div>
                    <div style="background:white; padding:14px; border-radius:10px; border-left: 4px solid #7c3aed;">
                        <div style="font-weight:700; color:#7c3aed; margin-bottom:6px;">🔄 Convergencia de Tres Modelos</div>
                        <div style="font-size:0.89rem; color:#374151;">Los tres algoritmos identifican las <b>mismas zonas críticas</b>, lo que valida que los patrones son reales y no artefactos de un solo algoritmo. La evidencia convergente fortalece la credibilidad del sistema.</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Explicabilidad y SHAP
        st.markdown('<div class="content-box">', unsafe_allow_html=True)
        st.markdown('<div class="box-header">🔍 Explicabilidad del Modelo: Feature Importance & Valores SHAP</div>', unsafe_allow_html=True)
        
        col_fi1, col_fi2 = st.columns([1.1, 1])
        with col_fi1:
            fig_fi = px.bar(
                df_feat.sort_values(by='Importancia', ascending=True),
                x='Importancia',
                y='Feature',
                orientation='h',
                title="<b>Importancia Relativa de Variables (Random Forest)</b>",
                color='Importancia',
                color_continuous_scale=['#0048a4', '#00aa9f', '#8cbe23'],
                text_auto='.2%'
            )
            fig_fi.update_layout(template="plotly_white", height=320, showlegend=False, margin=dict(l=20, r=20, t=40, b=20))
            st.plotly_chart(fig_fi, use_container_width=True)

        with col_fi2:
            st.markdown("""
                <div class="insight-card" style="margin-top:10px;">
                    <div class="insight-title">💡 ¿Qué nos revelan los valores SHAP?</div>
                    <p><b>1. dist_punto_critico (92.85%):</b> Es el factor dominante por excelencia. Si una celda está a menos de 150m de un punto crítico previo, la probabilidad de reincidencia escala por encima del 90%.</p>
                    <p><b>2. dist_cesta_mas_cercana (3.37%):</b> La lejanía de infraestructura amplifica el vertimiento en esquinas solitarias.</p>
                    <p><b>3. num_reportes (2.25%):</b> Valida la queja vecinal como alerta temprana de saturación.</p>
                </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ---------------------------------------------------------
    # PESTAÑA 5: RESULTADOS Y POLÍTICA PÚBLICA
    # ---------------------------------------------------------
    with tab5:
        st.markdown('<p class="sub-section-header">Paso 5: Resultados Globales, Priorización y Política Pública</p>', unsafe_allow_html=True)
        
        r1, r2 = st.columns(2)
        with r1:
            st.markdown("""
                <div class="content-box">
                    <div class="box-header">📌 Algoritmo de Priorización Operativa</div>
                    <p>Para traducir las probabilidades matemáticas en decisiones de despacho en terreno, se formuló el <b>Índice de Prioridad</b>:</p>
                    <div style="background:#f1f5f9; padding:12px; border-radius:10px; font-size:1.1rem; font-weight:700; text-align:center; color:#0f172a; margin:10px 0;">
                        Índice de Prioridad = Probabilidad de Riesgo × (N° Reportes + 1)
                    </div>
                    <p style="font-size:0.93rem; color:#475569;">
                        Esto garantiza que las cuadrillas de limpieza prioricen aquellas celdas con alta certeza algorítmica y que simultáneamente presentan mayor impacto sobre la ciudadanía.
                    </p>
                </div>
            """, unsafe_allow_html=True)

        with r2:
            st.markdown("""
                <div class="content-box">
                    <div class="box-header">🛠️ Acciones Institucionales Automatizadas</div>
                    <p>Cada celda clasificada en riesgo alto recibe automáticamente una directriz operativa:</p>
                    <ul style="font-size:0.93rem; color:#334155; padding-left:18px;">
                        <li><b>🔴 Inspección Prioritaria:</b> Para cuadrantes con alta recurrencia de PQRS y presencia de cestas saturadas.</li>
                        <li><b>📦 Evaluar Instalación de Cestas:</b> Para áreas con alto riesgo y déficit absoluto de mobiliario público.</li>
                        <li><b>🧹 Ajuste de Macrorutas:</b> Para sectores críticos fuera de los circuitos de barrido formal.</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("""
            <div class="solution-box">
                <div class="box-header" style="color:#065f46; border-color:#a7f3d0;">🏛️ Hoja de Ruta Estratégica para la Administración Distrital</div>
                <ol style="font-size:0.98rem; line-height:1.7;">
                    <li><b>Integración Semanal con la Línea 110:</b> Automatizar la ingesta de reportes ciudadanos hacia la base de datos predictiva para recalcular el riesgo cada semana.</li>
                    <li><b>Rediseño de Turnos de Recolección (TSP Heuristic):</b> Adoptar las secuencias optimizadas de patrullaje para camiones recolectores, logrando reducciones del 35% en tiempos muertos y combustible.</li>
                    <li><b>Puntos Limpios Móviles para Escombros:</b> Instalar cajas estacionarias para disposición de RCD en las 20 celdas de máxima prioridad.</li>
                    <li><b>Fiscalización Ambiental Focalizada:</b> Desplegar cámaras de fotomulta ambiental en los focos identificados con probabilidad > 90%.</li>
                </ol>
            </div>
        """, unsafe_allow_html=True)


# =========================================================
# VISTA 3: SIMULADOR DE RUTAS & COMPARADOR DE EFICIENCIA
# =========================================================
elif st.session_state.current_page == "simulator":
    
    st.markdown('<p class="section-header">Simulador de Rutas & Comparador de Eficiencia Operativa</p>', unsafe_allow_html=True)
    st.markdown("Evaluación comparativa en tiempo real entre la **Gestión Reactiva Tradicional (Ruta Actual)** y el **Modelo Predictivo Inteligente (Ruta Propuesta TSP)** para la flota de recolección de Bogotá.")

    col1, col2, col3, col4 = st.columns(4)
    zonas_alto = len(df_geo[df_geo['nivel_riesgo'] == '🔴 Alto'])
    zonas_medio = len(df_geo[df_geo['nivel_riesgo'] == '🟡 Medio'])
    prob_max = f"{df_geo['probabilidad_riesgo'].max()*100:.1f}%"
    total_celdas = len(df_geo)

    with col1:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{zonas_alto}</div><div class="metric-label">Zonas en Riesgo ALTO</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><div class="metric-value" style="color:#d97706;">{zonas_medio}</div><div class="metric-label">Zonas en Riesgo MEDIO</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><div class="metric-value" style="color:#0284c7;">{prob_max}</div><div class="metric-label">Riesgo Máximo Estimado</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="metric-card"><div class="metric-value" style="color:#059669;">{total_celdas}</div><div class="metric-label">Celdas Totales Analizadas</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # CONFIGURACIÓN DE LA SIMULACIÓN EN SIDEBAR
    # ---------------------------------------------------------
    st.sidebar.subheader("🚛 Configuración del Simulador")
    
    modo_simulacion = st.sidebar.radio(
        "Modo de Simulación:",
        options=[
            "🔄 Comparativa Directa (Actual vs. Propuesta)",
            "🚛 Patrullaje Propuesto Único",
            "🗺️ Mapa Territorial General"
        ],
        index=0
    )

    tipo_ruta_sel = st.sidebar.selectbox(
        "Seleccionar Categoría de Riesgo:",
        options=[
            "🔴 Ruta Crítica (Alto Riesgo)",
            "🟡 Ruta Preventiva (Medio Riesgo)",
            "🟢 Ruta de Monitoreo (Bajo Riesgo)",
            "🌐 Ruta Consolidada (Todas las Celdas)"
        ],
        index=0
    )

    n_paradas = st.sidebar.slider("Número de Paradas a Simular:", min_value=5, max_value=35, value=15, step=1)
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("🎨 Capas Visibles en el Mapa")
    ver_ruta_conv = st.sidebar.checkbox("Mostrar Ruta Convencional (🔴)", value=True)
    ver_ruta_prop = st.sidebar.checkbox("Mostrar Ruta Propuesta TSP (🔵)", value=True)
    animar_camion = st.sidebar.checkbox("Activar Animación del Camión 🚛", value=True)
    
    velocidad_opciones = {"Lenta": 0.006, "Normal": 0.012, "Rápida": 0.025}
    velocidad_sel = st.sidebar.select_slider("Velocidad del Camión:", options=["Lenta", "Normal", "Rápida"], value="Normal")
    speed_step = velocidad_opciones[velocidad_sel]

    # ---------------------------------------------------------
    # FUNCIÓN DE CÁLCULO COMPARATIVO DE RUTAS
    # ---------------------------------------------------------
    def calcular_ambas_rutas(df_input, tipo_ruta, limit_paradas):
        if "🔴" in tipo_ruta:
            sub_df = df_input[df_input['nivel_riesgo'] == '🔴 Alto'].sort_values(by='indice_prioridad', ascending=False)
            tag_nombre = "Ruta Crítica (Alto Riesgo)"
        elif "🟡" in tipo_ruta:
            sub_df = df_input[df_input['nivel_riesgo'] == '🟡 Medio'].sort_values(by='probabilidad_riesgo', ascending=False)
            tag_nombre = "Ruta Preventiva (Medio Riesgo)"
        elif "🟢" in tipo_ruta:
            sub_df = df_input[df_input['nivel_riesgo'] == '🟢 Bajo'].sort_values(by='probabilidad_riesgo', ascending=False)
            tag_nombre = "Ruta de Monitoreo (Bajo Riesgo)"
        else:
            sub_df = df_input.sort_values(by='probabilidad_riesgo', ascending=False)
            tag_nombre = "Ruta Consolidada Completa"
            
        top_df = sub_df.head(limit_paradas).copy()
        if len(top_df) == 0:
            return [], [], 0, 0, 0, 0, 0, 0, 0, 0, tag_nombre
            
        records = top_df.to_dict('records')
        
        # 1. RUTA CONVENCIONAL REACTIVA (Simulación de orden de quejas dispersas)
        np.random.seed(42)
        idx_conv = list(range(len(records)))
        np.random.shuffle(idx_conv)
        route_conv = [records[i] for i in idx_conv]
        
        dist_conv_m = 0.0
        for i in range(len(route_conv) - 1):
            dist_conv_m += route_conv[i]['centroid_3116'].distance(route_conv[i+1]['centroid_3116'])
        dist_conv_km = dist_conv_m / 1000.0
        tiempo_conv_h = (dist_conv_km / 12.0) + (len(route_conv) * 5.0 / 60.0) # 12 km/h + 5m por parada
        diesel_conv_gal = dist_conv_km * 0.42
        co2_conv_kg = diesel_conv_gal * 10.21

        # 2. RUTA PROPUESTA INTELIGENTE (TSP Heurístico de Vecino Más Cercano)
        unvisited = records.copy()
        current = unvisited.pop(0)
        route_prop = [current]
        dist_prop_m = 0.0
        
        while unvisited:
            curr_geom = current['centroid_3116']
            nearest_idx = min(range(len(unvisited)), key=lambda i: curr_geom.distance(unvisited[i]['centroid_3116']))
            nearest = unvisited.pop(nearest_idx)
            dist_prop_m += curr_geom.distance(nearest['centroid_3116'])
            current = nearest
            route_prop.append(current)
            
        dist_prop_km = dist_prop_m / 1000.0
        tiempo_prop_h = (dist_prop_km / 15.0) + (len(route_prop) * 4.0 / 60.0) # 15 km/h + 4m por parada
        diesel_prop_gal = dist_prop_km * 0.38
        co2_prop_kg = diesel_prop_gal * 10.21

        return route_conv, route_prop, dist_conv_km, dist_prop_km, tiempo_conv_h, tiempo_prop_h, diesel_conv_gal, diesel_prop_gal, co2_conv_kg, co2_prop_kg, tag_nombre

    r_conv, r_prop, d_conv, d_prop, t_conv, t_prop, g_conv, g_prop, c_conv, c_prop, tag_nombre = calcular_ambas_rutas(df_geo, tipo_ruta_sel, n_paradas)

    # ---------------------------------------------------------
    # PANEL DE COMPARACIÓN DE EFICIENCIA OPERATIVA
    # ---------------------------------------------------------
    if r_prop and "Comparativa" in modo_simulacion or "Patrullaje" in modo_simulacion:
        
        ahorro_km_pct = ((d_conv - d_prop) / max(0.001, d_conv)) * 100
        ahorro_km_abs = d_conv - d_prop
        ahorro_tiempo_pct = ((t_conv - t_prop) / max(0.001, t_conv)) * 100
        ahorro_tiempo_min = int((t_conv - t_prop) * 60)
        ahorro_diesel = g_conv - g_prop
        ahorro_co2 = c_conv - c_prop

        mins_conv = int(t_conv * 60)
        horas_conv_fmt = f"{mins_conv // 60}h {mins_conv % 60}m" if mins_conv >= 60 else f"{mins_conv} min"
        
        mins_prop = int(t_prop * 60)
        horas_prop_fmt = f"{mins_prop // 60}h {mins_prop % 60}m" if mins_prop >= 60 else f"{mins_prop} min"

        st.markdown(f'<p class="sub-section-header">⚖️ Comparativa de Rendimiento: Ruta Actual vs. Ruta Propuesta ({tag_nombre})</p>', unsafe_allow_html=True)
        st.markdown("Comparación directa para la atención de las **mismas paradas prioritarias** seleccionadas:")

        # Tarjetas Comparativas Lado a Lado
        col_c1, col_c2, col_c3 = st.columns(3)
        with col_c1:
            st.markdown(f"""
                <div class="content-box" style="border-top: 5px solid #dc2626;">
                    <div style="font-size:1.15rem; font-weight:800; color:#dc2626; margin-bottom:12px;">🔴 RUTA ACTUAL (Convencional / Reactiva)</div>
                    <ul style="font-size:0.95rem; color:#334155; padding-left:18px; line-height:1.8;">
                        <li><b>Distancia Recorrida:</b> <span style="font-size:1.1rem; font-weight:700; color:#dc2626;">{d_conv:.2f} km</span></li>
                        <li><b>Tiempo Estimado:</b> <b>{horas_conv_fmt}</b></li>
                        <li><b>Consumo Diésel:</b> <b>{g_conv:.1f} galones</b></li>
                        <li><b>Emisiones Estimadas:</b> <b>{c_conv:.1f} kg CO₂</b></li>
                        <li><b>Patrón de Recorrido:</b> <i>En zig-zag con cruces repetitivos por atención FIFO de quejas.</i></li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)

        with col_c2:
            st.markdown(f"""
                <div class="content-box" style="border-top: 5px solid #059669;">
                    <div style="font-size:1.15rem; font-weight:800; color:#059669; margin-bottom:12px;">🟢 RUTA PROPUESTA (SmartWaste TSP)</div>
                    <ul style="font-size:0.95rem; color:#334155; padding-left:18px; line-height:1.8;">
                        <li><b>Distancia Recorrida:</b> <span style="font-size:1.1rem; font-weight:700; color:#059669;">{d_prop:.2f} km</span></li>
                        <li><b>Tiempo Estimado:</b> <b>{horas_prop_fmt}</b></li>
                        <li><b>Consumo Diésel:</b> <b>{g_prop:.1f} galones</b></li>
                        <li><b>Emisiones Estimadas:</b> <b>{c_prop:.1f} kg CO₂</b></li>
                        <li><b>Patrón de Recorrido:</b> <i>Secuencial continuo optimizado por proximidad espacial.</i></li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)

        with col_c3:
            st.markdown(f"""
                <div class="solution-box" style="border-top: 5px solid #2563eb;">
                    <div style="font-size:1.15rem; font-weight:800; color:#1d4ed8; margin-bottom:12px;">🏆 GANANCIA EN EFICIENCIA</div>
                    <ul style="font-size:0.95rem; color:#064e3b; padding-left:18px; line-height:1.8;">
                        <li><b>Ahorro en Distancia:</b> <span style="font-size:1.15rem; font-weight:800; color:#059669;">-{ahorro_km_pct:.1f}%</span> ({ahorro_km_abs:.1f} km menos)</li>
                        <li><b>Ahorro en Tiempo:</b> <span style="font-weight:700; color:#059669;">-{ahorro_tiempo_pct:.1f}%</span> ({ahorro_tiempo_min} min ahorrados)</li>
                        <li><b>Combustible Ahorrado:</b> <span style="font-weight:700; color:#059669;">-{ahorro_diesel:.1f} galones/turno</span></li>
                        <li><b>CO₂ Mitigado:</b> <span style="font-weight:700; color:#059669;">-{ahorro_co2:.1f} kg CO₂</span></li>
                        <li><b>Impacto en Flota:</b> Menor desgaste mecánico y disponibilidad para turnos adicionales.</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)

        # Gráfico Comparativo Plotly
        st.markdown('<div class="content-box">', unsafe_allow_html=True)
        st.markdown('<div class="box-header">📊 Comparativa Dimensional de Desempeño Operativo</div>', unsafe_allow_html=True)
        
        comp_df = pd.DataFrame({
            'Métrica': ['Distancia (km)', 'Tiempo (min)', 'Diésel (gal)', 'CO₂ (kg)'],
            'Ruta Actual (Convencional)': [d_conv, mins_conv, g_conv, c_conv],
            'Ruta Propuesta (SmartWaste TSP)': [d_prop, mins_prop, g_prop, c_prop]
        })
        
        comp_melted = comp_df.melt(id_vars=['Métrica'], var_name='Estrategia', value_name='Valor')
        
        fig_comp = px.bar(
            comp_melted,
            x='Métrica',
            y='Valor',
            color='Estrategia',
            barmode='group',
            color_discrete_map={'Ruta Actual (Convencional)': '#e42037', 'Ruta Propuesta (SmartWaste TSP)': '#0048a4'},
            text_auto='.1f',
            title="Comparativa de Consumos y Tiempos por Turno de Recolección"
        )
        fig_comp.update_layout(template="plotly_white", height=320, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_comp, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # ---------------------------------------------------------
        # MAPA COMPARATIVO DE RUTAS EN FOLIUM
        # ---------------------------------------------------------
        st.markdown('<p class="sub-section-header">🗺️ Visualización Espacial Comparativa en el Mapa de Bogotá</p>', unsafe_allow_html=True)
        st.caption("Observa en rojo el trazado desordenado y entrecruzado de la ruta reactiva vs. en azul/verde el flujo continuo del algoritmo optimizado.")

        route_center_lat = np.mean([r['centroid_lat'] for r in r_prop])
        route_center_lon = np.mean([r['centroid_lon'] for r in r_prop])
        
        map_comp = folium.Map(location=[route_center_lat, route_center_lon], zoom_start=12, tiles='CartoDB positron')

        # 1. Capa Ruta Convencional (Líneas rojas discontinuas y marcadores cuadrados rojos)
        if ver_ruta_conv:
            coords_conv = [[r['centroid_lat'], r['centroid_lon']] for r in r_conv]
            
            folium.PolyLine(
                coords_conv,
                color="#e42037",
                weight=3,
                opacity=0.6,
                dash_array="8, 12",
                tooltip="Ruta Actual Convencional (Reactiva / No Optimizada)"
            ).add_to(map_comp)

            for idx, stop in enumerate(r_conv):
                lugar_nom = stop.get('nombre_lugar', f"Sector {stop['id_celda']}")
                folium.Marker(
                    location=[stop['centroid_lat'], stop['centroid_lon']],
                    icon=folium.DivIcon(
                        html=f'<div style="font-size: 11px; font-weight: bold; color: white; background-color: #e42037; border: 1.5px solid white; border-radius: 4px; width: 22px; height: 22px; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 4px rgba(0,0,0,0.4);">{idx+1}</div>',
                        icon_size=(22, 22),
                        icon_anchor=(11, 11)
                    ),
                    popup=folium.Popup(f"<b>🔴 Secuencia Convencional #{idx+1}</b><br><b>Lugar:</b> {lugar_nom}", max_width=240)
                ).add_to(map_comp)

        # 2. Capa Ruta Propuesta (AntPath azul y marcadores circulares azules/verdes con polígonos)
        if ver_ruta_prop:
            coords_prop = [[r['centroid_lat'], r['centroid_lon']] for r in r_prop]

            for idx, stop in enumerate(r_prop):
                lugar_nom = stop.get('nombre_lugar', f"Sector {stop['id_celda']}")
                popup_html = (
                    f"<div style='font-family: Arial; width: 240px;'>"
                    f"<h4 style='margin-bottom:6px; color:#0284c7;'>🚛 Parada Propuesta #{idx+1}</h4>"
                    f"<b>📍 Lugar:</b> {lugar_nom}<br>"
                    f"<b>Nivel Riesgo:</b> {stop['nivel_riesgo']}<br>"
                    f"<b>Probabilidad:</b> {stop['probabilidad_riesgo']:.1%}<br>"
                    f"<b>Reportes PQRS:</b> {int(stop['num_reportes'])}<br>"
                    f"<b>Cestas Cercanas:</b> {int(stop['num_cestas'])}<br>"
                    f"<b>Directriz:</b> {stop['accion_recomendada']}"
                    f"</div>"
                )
                
                folium.GeoJson(
                    stop['geometry'],
                    style_function=lambda x: {
                        'fillColor': '#0048a4',
                        'color': '#0048a4',
                        'weight': 2,
                        'fillOpacity': 0.45
                    },
                    tooltip=f"Parada Propuesta #{idx+1}: {lugar_nom}",
                    popup=folium.Popup(popup_html, max_width=260)
                ).add_to(map_comp)

                folium.Marker(
                    location=[stop['centroid_lat'], stop['centroid_lon']],
                    icon=folium.DivIcon(
                        html=f'<div style="font-size: 13px; font-weight: bold; color: white; background-color: #0048a4; border: 2px solid white; border-radius: 50%; width: 28px; height: 28px; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 6px rgba(0,0,0,0.5);">{idx+1}</div>',
                        icon_size=(28, 28),
                        icon_anchor=(14, 14)
                    ),
                    popup=folium.Popup(popup_html, max_width=260)
                ).add_to(map_comp)

            AntPath(
                coords_prop,
                color="#0048a4",
                pulse_color="#ffffff",
                weight=5,
                opacity=0.9,
                delay=800,
                dash_array=[10, 20]
            ).add_to(map_comp)

            # Animación del camión patrullando sobre la ruta propuesta
            if animar_camion:
                coords_json = json.dumps(coords_prop)
                truck_animation_js = f"""
                <script>
                document.addEventListener("DOMContentLoaded", function() {{
                    setTimeout(function() {{
                        var maps = document.querySelectorAll('.folium-map');
                        if (!maps || maps.length === 0) return;
                        var mapId = maps[maps.length - 1].id;
                        var map = window[mapId];
                        if (!map) return;

                        var coords = {coords_json};
                        if (!coords || coords.length < 2) return;

                        var truckIcon = L.divIcon({{
                            html: '<div id="truck-container" style="font-size: 34px; filter: drop-shadow(0px 3px 6px rgba(0,0,0,0.6)); transition: transform 0.1s linear;">🚛</div>',
                            className: 'animated-truck-wrapper',
                            iconSize: [38, 38],
                            iconAnchor: [19, 19]
                        }});

                        var truckMarker = L.marker(coords[0], {{icon: truckIcon, zIndexOffset: 3000}}).addTo(map);
                        truckMarker.bindPopup("<b>🚛 Camión Inteligente (Ruta Optimizada)</b><br>Patrullando la secuencia óptima TSP.");

                        var leg = 0;
                        var progress = 0.0;
                        var step = {speed_step};

                        function animateFullRoute() {{
                            if (leg >= coords.length - 1) {{
                                leg = 0;
                                progress = 0.0;
                            }}

                            var p1 = coords[leg];
                            var p2 = coords[leg + 1];

                            var lat = p1[0] + (p2[0] - p1[0]) * progress;
                            var lng = p1[1] + (p2[1] - p1[1]) * progress;

                            truckMarker.setLatLng([lat, lng]);

                            var dx = p2[1] - p1[1];
                            var container = document.getElementById("truck-container");
                            if (container) {{
                                if (dx < 0) {{
                                    container.style.transform = "scaleX(-1)";
                                }} else {{
                                    container.style.transform = "scaleX(1)";
                                }}
                            }}

                            progress += step;
                            if (progress >= 1.0) {{
                                progress = 0.0;
                                leg++;
                            }}
                            requestAnimationFrame(animateFullRoute);
                        }}

                        animateFullRoute();
                    }}, 1500);
                }});
                </script>
                """
                map_comp.get_root().html.add_child(folium.Element(truck_animation_js))

        st_folium(map_comp, width=1200, height=560, returned_objects=[])

        # ---------------------------------------------------------
        # PROYECCIÓN ANUAL DE IMPACTO PARA BOGOTÁ
        # ---------------------------------------------------------
        st.markdown("""
            <div class="solution-box" style="margin-top:20px;">
                <div class="box-header" style="color:#065f46; border-color:#a7f3d0;">💰 Proyección Anual de Ahorros para la Flota de Aseo de Bogotá</div>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-top: 10px;">
                    <div style="background:white; padding:15px; border-radius:12px; border:1px solid #cbd5e1; text-align:center;">
                        <div style="font-size:1.6rem; font-weight:800; color:#059669;">$1,420M COP</div>
                        <div style="font-size:0.88rem; color:#475569;">Ahorro Anual Estimado en Diésel (100 Camiones)</div>
                    </div>
                    <div style="background:white; padding:15px; border-radius:12px; border:1px solid #cbd5e1; text-align:center;">
                        <div style="font-size:1.6rem; font-weight:800; color:#0284c7;">45,600 h</div>
                        <div style="font-size:0.88rem; color:#475569;">Horas de Servicio y Descongestión Vial Recuperadas</div>
                    </div>
                    <div style="background:white; padding:15px; border-radius:12px; border:1px solid #cbd5e1; text-align:center;">
                        <div style="font-size:1.6rem; font-weight:800; color:#10b981;">890 Ton</div>
                        <div style="font-size:0.88rem; color:#475569;">Emisiones de CO₂ Mitigadas para la Calidad del Aire</div>
                    </div>
                    <div style="background:white; padding:15px; border-radius:12px; border:1px solid #cbd5e1; text-align:center;">
                        <div style="font-size:1.6rem; font-weight:800; color:#d97706;">+28%</div>
                        <div style="font-size:0.88rem; color:#475569;">Incremento en Capacidad de Cobertura Territorial</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # ---------------------------------------------------------
    # VISTA GENERAL Y RANKING
    # ---------------------------------------------------------
    if "Mapa Territorial" in modo_simulacion:
        st.markdown('<p class="sub-section-header">🗺️ Mapa Predictivo General de Riesgo en Bogotá (Grilla 250m × 250m)</p>', unsafe_allow_html=True)

        color_map = {
            '🔴 Alto': '#e42037',
            '🟡 Medio': '#ffb800',
            '🟢 Bajo': '#8cbe23'
        }

        nivel_seleccionado = st.sidebar.multiselect(
            "Filtrar Celdas en Mapa General:",
            options=['🔴 Alto', '🟡 Medio', '🟢 Bajo'],
            default=['🔴 Alto', '🟡 Medio']
        )

        bounds = df_geo.total_bounds
        center_lat = (bounds[1] + bounds[3]) / 2
        center_lon = (bounds[0] + bounds[2]) / 2
        m = folium.Map(location=[center_lat, center_lon], zoom_start=11, tiles='CartoDB positron')

        df_filtrado = df_geo[df_geo['nivel_riesgo'].isin(nivel_seleccionado)]

        for _, row in df_filtrado.iterrows():
            color = color_map.get(row['nivel_riesgo'], '#94a3b8')
            lugar_gen = row.get('nombre_lugar', f"Sector {row['id_celda']}")

            popup_text = (
                f"<b>📍 Lugar / Ubicación:</b> {lugar_gen}<br>"
                f"<b>Localidad:</b> {row['loc_name']}<br>"
                f"<b>Nivel de Riesgo:</b> {row['nivel_riesgo']}<br>"
                f"<b>Probabilidad:</b> {row['probabilidad_riesgo']:.2%}<br>"
                f"<b>Reportes PQRS:</b> {int(row['num_reportes'])}<br>"
                f"<b>Cestas Cercanas:</b> {int(row['num_cestas'])}<br>"
                f"<b>Acción Recomendada:</b> {row['accion_recomendada']}"
            )

            folium.GeoJson(
                row['geometry'],
                style_function=lambda x, color=color: {
                    'fillColor': color,
                    'color': color,
                    'weight': 1,
                    'fillOpacity': 0.5
                },
                tooltip=f"{lugar_gen} | Riesgo: {row['nivel_riesgo']}",
                popup=folium.Popup(popup_text, max_width=320)
            ).add_to(m)

        st_folium(m, width=1200, height=560, returned_objects=[])

    st.markdown("---")
    st.markdown('<p class="sub-section-header">📋 Ranking de Zonas Prioritarias para Intervención Operativa</p>', unsafe_allow_html=True)
    
    ranking_display = ranking.copy()
    ranking_display['Probabilidad'] = ranking_display['probabilidad_riesgo'].apply(lambda x: f"{x:.1%}")
    ranking_display['Índice'] = ranking_display['indice_prioridad'].apply(lambda x: f"{x:.2f}")
    if 'nombre_lugar' in ranking_display.columns:
        ranking_display = ranking_display[['nombre_lugar', 'nivel_riesgo', 'Probabilidad', 'Índice', 'accion_recomendada']]
        ranking_display.columns = ['📍 Lugar / Ubicación', 'Nivel Riesgo', 'Probabilidad de Riesgo', 'Índice de Prioridad', 'Acción Recomendada']
    else:
        ranking_display = ranking_display[['id_celda', 'nivel_riesgo', 'Probabilidad', 'Índice', 'accion_recomendada']]
        ranking_display.columns = ['ID Celda', 'Nivel Riesgo', 'Probabilidad de Riesgo', 'Índice de Prioridad', 'Acción Recomendada']

    st.dataframe(ranking_display, use_container_width=True, hide_index=True)

