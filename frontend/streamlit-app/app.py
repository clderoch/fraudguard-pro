import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import warnings
import random  # Added missing import
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="FraudGuard Pro - Small Business Protection",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enterprise-grade CSS inspired by Kount, Signifyd, and Forter
st.markdown("""
<style>
    /* Import professional fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
    
    /* Advanced CSS Variables for Enterprise Design System */
    :root {
        /* Professional Color Palette */
        --primary-50: #f0f9ff;
        --primary-100: #e0f2fe;
        --primary-200: #bae6fd;
        --primary-300: #7dd3fc;
        --primary-400: #38bdf8;
        --primary-500: #0ea5e9;
        --primary-600: #0284c7;
        --primary-700: #0369a1;
        --primary-800: #075985;
        --primary-900: #0c4a6e;
        
        /* Sophisticated Neutral Scale */
        --gray-25: #fcfcfd;
        --gray-50: #f8fafc;
        --gray-100: #f1f5f9;
        --gray-200: #e2e8f0;
        --gray-300: #cbd5e1;
        --gray-400: #94a3b8;
        --gray-500: #64748b;
        --gray-600: #475569;
        --gray-700: #334155;
        --gray-800: #1e293b;
        --gray-900: #0f172a;
        
        /* Enterprise Status Colors */
        --success-50: #f0fdf4;
        --success-100: #dcfce7;
        --success-500: #22c55e;
        --success-600: #16a34a;
        --success-700: #15803d;
        
        --warning-50: #fffbeb;
        --warning-100: #fef3c7;
        --warning-500: #f59e0b;
        --warning-600: #d97706;
        --warning-700: #b45309;
        
        --error-50: #fef2f2;
        --error-100: #fee2e2;
        --error-500: #ef4444;
        --error-600: #dc2626;
        --error-700: #b91c1c;
        
        /* Advanced Shadows */
        --shadow-xs: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow-sm: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px -1px rgba(0, 0, 0, 0.1);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.1);
        --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
        
        /* Professional Border Radius */
        --radius-xs: 0.125rem;
        --radius-sm: 0.25rem;
        --radius-md: 0.375rem;
        --radius-lg: 0.5rem;
        --radius-xl: 0.75rem;
        --radius-2xl: 1rem;
        --radius-3xl: 1.5rem;
        
        /* Typography Scale */
        --text-xs: 0.75rem;
        --text-sm: 0.875rem;
        --text-base: 1rem;
        --text-lg: 1.125rem;
        --text-xl: 1.25rem;
        --text-2xl: 1.5rem;
        --text-3xl: 1.875rem;
        --text-4xl: 2.25rem;
        --text-5xl: 3rem;
    }
    
    /* Reset and Base Styles */
    * {
        box-sizing: border-box;
    }
    
    /* Hide Streamlit default elements with enhanced selectors */
    .css-1d391kg, [data-testid="stHeader"] {padding: 1rem 2rem 2rem;}
    .css-k1vhr4 {margin-top: -60px;}
    [data-testid="stToolbar"] {visibility: hidden;}
    
    /* Global Typography Enhancement */
    html, body, .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
        font-feature-settings: 'cv11', 'ss01';
        font-variation-settings: 'opsz' 32;
        background-color: var(--gray-25);
        color: var(--gray-800);
        line-height: 1.6;
    }
    
    /* Enterprise Header with Professional Branding */
    .main-header {
        background: linear-gradient(135deg, var(--primary-600) 0%, var(--primary-700) 50%, var(--primary-800) 100%);
        border: 1px solid var(--primary-200);
        padding: 3rem 2rem;
        border-radius: var(--radius-2xl);
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: var(--shadow-xl);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, rgba(255,255,255,0.1) 0%, transparent 50%);
        pointer-events: none;
    }
    
    .main-header h1 {
        font-size: var(--text-4xl);
        font-weight: 800;
        margin-bottom: 0.75rem;
        letter-spacing: -0.025em;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .main-header p {
        font-size: var(--text-lg);
        font-weight: 400;
        opacity: 0.95;
        margin: 0;
        max-width: 600px;
        margin: 0 auto;
    }
    
    /* Professional Status Indicators */
    /* Professional Status Indicators */
    .status-good {
        background: linear-gradient(135deg, var(--success-500) 0%, var(--success-600) 100%);
        border: 1px solid var(--success-200);
        color: white;
        padding: 1.25rem 2rem;
        border-radius: var(--radius-xl);
        text-align: center;
        margin: 1.5rem 0;
        font-size: var(--text-lg);
        font-weight: 600;
        box-shadow: var(--shadow-lg);
        backdrop-filter: blur(10px);
        position: relative;
    }
    
    .status-warning {
        background: linear-gradient(135deg, var(--warning-500) 0%, var(--warning-600) 100%);
        border: 1px solid var(--warning-200);
        color: white;
        padding: 1.25rem 2rem;
        border-radius: var(--radius-xl);
        text-align: center;
        margin: 1.5rem 0;
        font-size: var(--text-lg);
        font-weight: 600;
        box-shadow: var(--shadow-lg);
        backdrop-filter: blur(10px);
    }
    
    .status-danger {
        background: linear-gradient(135deg, var(--error-500) 0%, var(--error-600) 100%);
        border: 1px solid var(--error-200);
        color: white;
        padding: 1.25rem 2rem;
        border-radius: var(--radius-xl);
        text-align: center;
        margin: 1.5rem 0;
        font-size: var(--text-lg);
        font-weight: 600;
        box-shadow: var(--shadow-lg);
        backdrop-filter: blur(10px);
    }
    
    /* Enterprise Upload Section */
    .upload-container {
        background: var(--gray-25);
        border: 2px dashed var(--primary-300);
        border-radius: var(--radius-2xl);
        padding: 3rem 2rem;
        text-align: center;
        margin: 2rem 0;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .upload-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, var(--primary-50) 0%, transparent 50%);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .upload-container:hover {
        border-color: var(--primary-500);
        background: var(--primary-50);
        transform: translateY(-1px);
        box-shadow: var(--shadow-lg);
    }
    
    .upload-container:hover::before {
        opacity: 1;
    }
    
    /* Professional Metric Cards */
    .big-number-card {
        background: white;
        border: 1px solid var(--gray-200);
        padding: 2rem;
        border-radius: var(--radius-2xl);
        box-shadow: var(--shadow-sm);
        text-align: center;
        margin: 1rem 0;
        border-left: 4px solid var(--success-500);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .big-number-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(255,255,255,0.8) 0%, rgba(255,255,255,0.2) 100%);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .big-number-card:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
    }
    
    .big-number-card:hover::before {
        opacity: 1;
    }
    
    .big-number {
        font-size: var(--text-4xl);
        font-weight: 800;
        color: var(--gray-900);
        margin: 0;
        line-height: 1.1;
        font-feature-settings: 'tnum', 'lnum';
        position: relative;
        z-index: 1;
    }
    
    .big-label {
        font-size: var(--text-base);
        color: var(--gray-600);
        margin: 0.75rem 0 0 0;
        font-weight: 500;
        letter-spacing: 0.025em;
        position: relative;
        z-index: 1;
    }
    
    .action-needed {
        border-left-color: var(--error-500);
        background: linear-gradient(135deg, var(--error-50) 0%, white 100%);
    }
    
    .action-needed .big-number {
        color: var(--error-600);
    }
    
    .watch-closely {
        border-left-color: var(--warning-500);
        background: linear-gradient(135deg, var(--warning-50) 0%, white 100%);
    }
    
    .watch-closely .big-number {
        color: var(--warning-600);
    }
    
    .all-good {
        border-left-color: var(--success-500);
        background: linear-gradient(135deg, var(--success-50) 0%, white 100%);
    }
    
    .all-good .big-number {
        color: var(--success-600);
    }
    
    /* Professional Action Buttons */
    /* Professional Action Buttons */
    .action-button {
        background: linear-gradient(135deg, var(--primary-500) 0%, var(--primary-600) 100%);
        border: 1px solid var(--primary-300);
        color: white;
        padding: 0.875rem 1.75rem;
        border-radius: var(--radius-lg);
        text-decoration: none;
        font-weight: 600;
        font-size: var(--text-sm);
        border: none;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        margin: 0.375rem;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        position: relative;
        overflow: hidden;
        box-shadow: var(--shadow-sm);
    }
    
    .action-button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .action-button:hover {
        transform: translateY(-1px);
        box-shadow: var(--shadow-lg);
        background: linear-gradient(135deg, var(--primary-600) 0%, var(--primary-700) 100%);
    }
    
    .action-button:hover::before {
        left: 100%;
    }
    
    .urgent-button {
        background: linear-gradient(135deg, var(--error-500) 0%, var(--error-600) 100%);
        border: 1px solid var(--error-300);
        font-size: var(--text-lg);
        padding: 1.25rem 2.5rem;
        box-shadow: var(--shadow-lg);
        font-weight: 700;
    }
    
    .urgent-button:hover {
        background: linear-gradient(135deg, var(--error-600) 0%, var(--error-700) 100%);
        box-shadow: var(--shadow-xl);
    }
    
    /* Enterprise Explanation Boxes */
    .explanation-box {
        background: white;
        border: 1px solid var(--gray-200);
        border-radius: var(--radius-xl);
        padding: 1.5rem;
        margin: 1.5rem 0;
        box-shadow: var(--shadow-sm);
        position: relative;
        overflow: hidden;
    }
    
    .explanation-box::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(180deg, var(--primary-500) 0%, var(--primary-600) 100%);
    }
    
    .explanation-title {
        font-size: var(--text-lg);
        font-weight: 600;
        color: var(--gray-900);
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .explanation-text {
        font-size: var(--text-base);
        color: var(--gray-700);
        line-height: 1.6;
        margin: 0;
    }
    
    /* Professional Traffic Light System */
    .traffic-light {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 1.5rem;
        background: white;
        border: 1px solid var(--gray-200);
        border-radius: var(--radius-2xl);
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: var(--shadow-md);
    }
    
    .traffic-item {
        text-align: center;
        padding: 1.5rem;
        border-radius: var(--radius-xl);
        transition: all 0.3s ease;
        border: 1px solid transparent;
    }
    
    .traffic-item:hover {
        transform: translateY(-2px);
        border-color: var(--gray-200);
        box-shadow: var(--shadow-md);
    }
    
    .traffic-circle {
        width: 4rem;
        height: 4rem;
        border-radius: 50%;
        margin: 0 auto 1rem auto;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: var(--text-xl);
        font-weight: 800;
        color: white;
        box-shadow: var(--shadow-lg);
        position: relative;
    }
    
    .traffic-circle::after {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        border-radius: 50%;
        background: linear-gradient(45deg, rgba(255,255,255,0.3), rgba(255,255,255,0.1));
        z-index: -1;
    }
    
    .green { 
        background: linear-gradient(135deg, var(--success-500) 0%, var(--success-600) 100%);
    }
    .yellow { 
        background: linear-gradient(135deg, var(--warning-500) 0%, var(--warning-600) 100%);
    }
    .red { 
        background: linear-gradient(135deg, var(--error-500) 0%, var(--error-600) 100%);
    }
    
    .traffic-label {
        font-size: var(--text-lg);
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: var(--gray-900);
    }
    
    .traffic-description {
        font-size: var(--text-sm);
        color: var(--gray-600);
        line-height: 1.5;
    }
    
    /* Professional Alert Cards */
    /* Professional Alert Cards */
    .alert-card {
        background: white;
        border: 1px solid var(--gray-200);
        border-radius: var(--radius-xl);
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: var(--shadow-md);
        border-left: 4px solid var(--error-500);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .alert-card::before {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 100px;
        height: 100px;
        background: radial-gradient(circle, rgba(239, 68, 68, 0.1) 0%, transparent 70%);
        transform: translateX(50%) translateY(-50%);
    }
    
    .alert-card:hover {
        transform: translateY(-1px);
        box-shadow: var(--shadow-lg);
    }
    
    .alert-high {
        border-left-color: var(--error-500);
        background: linear-gradient(135deg, var(--error-50) 0%, white 100%);
    }
    
    .alert-medium {
        border-left-color: var(--warning-500);
        background: linear-gradient(135deg, var(--warning-50) 0%, white 100%);
    }
    
    .alert-low {
        border-left-color: var(--primary-500);
        background: linear-gradient(135deg, var(--primary-50) 0%, white 100%);
    }
    
    .alert-title {
        font-size: var(--text-lg);
        font-weight: 600;
        margin-bottom: 0.75rem;
        color: var(--gray-900);
        position: relative;
        z-index: 1;
    }
    
    .alert-details {
        font-size: var(--text-base);
        margin-bottom: 1rem;
        color: var(--gray-700);
        line-height: 1.6;
        position: relative;
        z-index: 1;
    }
    
    .alert-action {
        font-size: var(--text-base);
        font-weight: 600;
        color: var(--gray-900);
        position: relative;
        z-index: 1;
    }
    
    /* Enterprise Chart Containers */
    .simple-chart {
        background: white;
        border: 1px solid var(--gray-200);
        padding: 2rem;
        border-radius: var(--radius-2xl);
        box-shadow: var(--shadow-md);
        margin: 2rem 0;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .simple-chart::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--primary-500) 0%, var(--primary-600) 50%, var(--primary-700) 100%);
    }
    
    .simple-chart:hover {
        transform: translateY(-1px);
        box-shadow: var(--shadow-lg);
    }
    
    .chart-title {
        font-size: var(--text-2xl);
        font-weight: 600;
        color: var(--gray-900);
        margin-bottom: 1.5rem;
        text-align: center;
        position: relative;
    }
    
    /* Professional Progress Bars */
    .progress-container {
        background: var(--gray-100);
        border-radius: var(--radius-lg);
        padding: 0.25rem;
        margin: 1rem 0;
        box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.1);
    }
    
    .progress-bar {
        height: 1.25rem;
        border-radius: var(--radius-md);
        transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .progress-bar::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, rgba(255,255,255,0.2) 25%, transparent 25%, transparent 50%, rgba(255,255,255,0.2) 50%, rgba(255,255,255,0.2) 75%, transparent 75%);
        background-size: 1rem 1rem;
        animation: progress-shine 2s linear infinite;
    }
    
    @keyframes progress-shine {
        0% { background-position: -1rem 0; }
        100% { background-position: 1rem 0; }
    }
    
    .progress-green { 
        background: linear-gradient(135deg, var(--success-500) 0%, var(--success-600) 100%);
    }
    .progress-yellow { 
        background: linear-gradient(135deg, var(--warning-500) 0%, var(--warning-600) 100%);
    }
    .progress-red { 
        background: linear-gradient(135deg, var(--error-500) 0%, var(--error-600) 100%);
    }
    
    /* Enhanced Streamlit Components */
    .stMetric {
        background: white;
        border: 1px solid var(--gray-200);
        border-radius: var(--radius-lg);
        padding: 1rem;
        box-shadow: var(--shadow-sm);
    }
    
    .stMetric > div {
        font-size: var(--text-lg);
        font-weight: 600;
    }
    
    /* Enterprise Transaction Display Styles */
    /* Enterprise Transaction Display Styles */
    .transaction-summary {
        background: white;
        border: 1px solid var(--gray-200);
        border-radius: var(--radius-xl);
        padding: 1.5rem;
        margin: 0.75rem 0;
        box-shadow: var(--shadow-sm);
        border-left: 4px solid var(--error-500);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .transaction-summary::before {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 60px;
        height: 60px;
        background: radial-gradient(circle, rgba(239, 68, 68, 0.08) 0%, transparent 70%);
        transform: translateX(30%) translateY(-30%);
    }
    
    .transaction-summary:hover {
        transform: translateY(-1px);
        box-shadow: var(--shadow-md);
    }
    
    .risk-category-item {
        background: white;
        border: 1px solid var(--gray-200);
        padding: 1.25rem;
        margin: 0.75rem 0;
        border-radius: var(--radius-lg);
        border-left: 4px solid var(--error-500);
        box-shadow: var(--shadow-sm);
        transition: all 0.3s ease;
        position: relative;
    }
    
    .risk-category-item:hover {
        transform: translateX(2px);
        box-shadow: var(--shadow-md);
    }
    
    .risk-progress-bar {
        background: var(--error-100);
        height: 6px;
        border-radius: var(--radius-sm);
        margin-top: 0.75rem;
        overflow: hidden;
        position: relative;
    }
    
    .risk-progress-fill {
        background: linear-gradient(90deg, var(--error-500) 0%, var(--error-600) 100%);
        height: 6px;
        border-radius: var(--radius-sm);
        transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
    }
    
    .risk-progress-fill::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, rgba(255,255,255,0.3) 25%, transparent 25%);
        background-size: 8px 8px;
        animation: progress-slide 1.5s linear infinite;
    }
    
    @keyframes progress-slide {
        0% { background-position: 0 0; }
        100% { background-position: 16px 0; }
    }
    
    .transaction-expandable {
        border: 1px solid var(--gray-200);
        border-radius: var(--radius-lg);
        margin: 0.75rem 0;
        background: white;
        overflow: hidden;
        box-shadow: var(--shadow-sm);
        transition: all 0.3s ease;
    }
    
    .transaction-expandable:hover {
        box-shadow: var(--shadow-md);
    }
    
    .transaction-header {
        padding: 1.25rem;
        background: linear-gradient(135deg, var(--gray-50) 0%, var(--gray-25) 100%);
        border-bottom: 1px solid var(--gray-200);
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
    }
    
    .transaction-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(255,255,255,0.5) 0%, transparent 50%);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .transaction-header:hover {
        background: linear-gradient(135deg, var(--gray-100) 0%, var(--gray-50) 100%);
        transform: translateY(-1px);
    }
    
    .transaction-header:hover::before {
        opacity: 1;
    }
    
    .transaction-content {
        padding: 1.5rem;
        background: white;
    }
    
    .risk-factor-item {
        padding: 0.75rem;
        margin: 0.375rem 0;
        background: linear-gradient(135deg, var(--error-50) 0%, white 100%);
        border: 1px solid var(--error-200);
        border-left: 3px solid var(--error-500);
        border-radius: var(--radius-md);
        font-size: var(--text-sm);
        color: var(--gray-700);
        transition: all 0.3s ease;
    }
    
    .risk-factor-item:hover {
        background: linear-gradient(135deg, var(--error-100) 0%, var(--error-50) 100%);
        transform: translateX(2px);
    }
    
    .filter-section {
        background: linear-gradient(135deg, var(--gray-50) 0%, white 100%);
        border: 1px solid var(--gray-200);
        padding: 1.5rem;
        border-radius: var(--radius-xl);
        margin: 1.5rem 0;
        box-shadow: var(--shadow-sm);
        position: relative;
        overflow: hidden;
    }
    
    .filter-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--primary-500) 0%, var(--primary-600) 100%);
    }
    
    .metric-card {
        background: white;
        border: 1px solid var(--gray-200);
        padding: 2rem;
        border-radius: var(--radius-2xl);
        box-shadow: var(--shadow-md);
        text-align: center;
        border-left: 4px solid var(--success-500);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 80px;
        height: 80px;
        background: radial-gradient(circle, rgba(34, 197, 94, 0.08) 0%, transparent 70%);
        transform: translateX(40%) translateY(-40%);
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
    }
    
    .metric-value {
        font-size: var(--text-3xl);
        font-weight: 800;
        color: var(--gray-900);
        margin: 0;
        font-feature-settings: 'tnum', 'lnum';
        position: relative;
        z-index: 1;
    }
    
    .metric-label {
        font-size: var(--text-sm);
        color: var(--gray-600);
        margin-top: 0.75rem;
        font-weight: 500;
        letter-spacing: 0.025em;
        position: relative;
        z-index: 1;
    }
    
    .tab-content {
        padding: 1.5rem 0;
    }
    
    .pagination-info {
        background: linear-gradient(135deg, var(--primary-50) 0%, white 100%);
        border: 1px solid var(--primary-200);
        padding: 1rem;
        border-radius: var(--radius-lg);
        margin: 1.5rem 0;
        text-align: center;
        font-weight: 600;
        color: var(--primary-700);
        box-shadow: var(--shadow-sm);
    }
    
    /* Professional Responsive Design */
    @media (max-width: 1024px) {
        .traffic-light {
            grid-template-columns: 1fr;
            gap: 1rem;
        }
        
        .main-header {
            padding: 2rem 1.5rem;
        }
        
        .main-header h1 {
            font-size: var(--text-3xl);
        }
    }
    
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: var(--text-2xl);
        }
        
        .big-number {
            font-size: var(--text-3xl);
        }
        
        .action-button {
            display: block;
            text-align: center;
            margin: 0.75rem 0;
            width: 100%;
        }
        
        .big-number-card {
            padding: 1.5rem;
        }
        
        .transaction-header,
        .transaction-content {
            padding: 1rem;
        }
        
        .simple-chart {
            padding: 1.5rem;
        }
    }
    
    @media (max-width: 480px) {
        .main-header {
            padding: 1.5rem 1rem;
        }
        
        .explanation-box,
        .filter-section {
            padding: 1rem;
        }
        
        .urgent-button {
            padding: 1rem 1.5rem;
            font-size: var(--text-base);
        }
    }
    
    /* Advanced Interactive States */
    .action-button:active {
        transform: translateY(0);
        box-shadow: var(--shadow-sm);
    }
    
    .big-number-card:active {
        transform: translateY(0);
    }
    
    /* Loading States */
    .loading-shimmer {
        background: linear-gradient(90deg, var(--gray-200) 25%, var(--gray-100) 50%, var(--gray-200) 75%);
        background-size: 200% 100%;
        animation: shimmer 1.5s infinite;
    }
    
    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    
    /* Professional Focus States for Accessibility */
    .action-button:focus-visible,
    .transaction-header:focus-visible {
        outline: 2px solid var(--primary-500);
        outline-offset: 2px;
    }
    
    /* Print Styles */
    @media print {
        .action-button,
        .urgent-button {
            display: none;
        }
        
        .main-header {
            background: var(--gray-100) !important;
            color: var(--gray-900) !important;
        }
        
        .simple-chart {
            break-inside: avoid;
        }
    }
</style>
""", unsafe_allow_html=True)

class SimpleFraudDetectionModel:
    """Enhanced fraud detection with industry-specific rules and adaptive thresholds"""
    
    def __init__(self):
        self.risk_score_calculated = False
        # US ZIP code to state mapping (simplified sample)
        self.zip_to_state = {
            '90210': 'CA', '10001': 'NY', '60601': 'IL', '33101': 'FL',
            '77001': 'TX', '30301': 'GA', '02101': 'MA', '98101': 'WA',
            '80201': 'CO', '85001': 'AZ', '97201': 'OR', '89101': 'NV'
        }
        
        # IP address to general location mapping (simplified sample)
        self.ip_to_location = {
            '192.168': 'Local Network',
            '8.8.8': 'Mountain View, CA',
            '4.4.4': 'Level 3, US',
            '1.1.1': 'Cloudflare, Global'
        }
        
        # Industry-specific fraud patterns and thresholds
        self.industry_patterns = {
            'mobile_app': {
                'typical_amounts': (0.99, 49.99),
                'suspicious_amounts': [9999.99, 999.99, 99.99],  # Common price points for fraud
                'velocity_threshold': 10,  # transactions per hour
                'refund_rate_threshold': 0.15,  # 15% refund rate is suspicious
                'common_fraud_indicators': ['rooted_device', 'emulator', 'vpn_detected'],
                'peak_hours': [18, 19, 20, 21, 22],  # Gaming/app usage peaks
                'risk_multiplier': 1.2
            },
            'healthcare': {
                'typical_amounts': (25, 500),
                'suspicious_amounts': [999.99, 1999.99, 4999.99],  # Insurance limits
                'velocity_threshold': 3,  # Much lower - medical visits are infrequent
                'billing_patterns': ['urgent_care', 'emergency', 'specialist'],
                'compliance_required': True,
                'peak_hours': [9, 10, 11, 14, 15, 16],  # Medical office hours
                'risk_multiplier': 0.8,  # Generally lower risk industry
                'age_verification': True
            },
            'gaming': {
                'typical_amounts': (4.99, 99.99),
                'whale_threshold': 500,  # High spenders
                'velocity_threshold': 20,  # Gaming can have high velocity
                'common_fraud_amounts': [1.00, 10.00, 100.00],
                'peak_hours': [18, 19, 20, 21, 22, 23],
                'risk_multiplier': 1.3
            },
            'financial': {
                'structuring_threshold': 9000,  # BSA compliance
                'velocity_threshold': 5,
                'high_risk_amounts': [9999, 9998, 9997, 9990],  # Structuring patterns
                'peak_hours': [9, 10, 11, 14, 15, 16],
                'risk_multiplier': 1.5
            },
            'subscription': {
                'trial_abuse_threshold': 5,  # Multiple trials
                'common_amounts': [0.01, 1.00, 9.99, 29.99],
                'chargeback_threshold': 0.1,
                'risk_multiplier': 1.1
            }
        }
    
    def check_geographical_anomalies(self, row):
        """Check for geographical mismatches"""
        anomalies = []
        score_increase = 0
        
        # Get relevant fields
        customer_state = str(row.get('customer_state', '')).strip().upper()
        customer_zip = str(row.get('customer_zip_code', '')).strip()
        customer_ip = str(row.get('customer_ip_address', '')).strip()
        customer_city = str(row.get('customer_city', '')).strip()
        
        # Check ZIP code to state mismatch
        if customer_zip and customer_state:
            # Extract first 5 digits of ZIP
            zip_code = customer_zip[:5] if len(customer_zip) >= 5 else customer_zip
            
            # Check against known ZIP patterns (simplified check)
            expected_state = self.zip_to_state.get(zip_code, '')
            
            if expected_state and expected_state != customer_state:
                anomalies.append(f"ZIP {zip_code} doesn't match state {customer_state}")
                score_increase += 35
            
            # Simple ZIP code validation patterns
            if customer_state == 'CA' and not (zip_code.startswith('9') or zip_code.startswith('8')):
                anomalies.append("California ZIP doesn't match typical CA pattern")
                score_increase += 25
            elif customer_state == 'NY' and not (zip_code.startswith('1') or zip_code.startswith('0')):
                anomalies.append("New York ZIP doesn't match typical NY pattern")
                score_increase += 25
            elif customer_state == 'TX' and not zip_code.startswith('7'):
                anomalies.append("Texas ZIP doesn't match typical TX pattern")
                score_increase += 25
            elif customer_state == 'FL' and not zip_code.startswith('3'):
                anomalies.append("Florida ZIP doesn't match typical FL pattern")
                score_increase += 25
        
        # Check IP address geographical consistency
        if customer_ip and customer_state:
            # Extract IP prefix for simplified geolocation
            ip_prefix = '.'.join(customer_ip.split('.')[:3])
            
            # Check for private/local IP addresses (higher risk)
            if customer_ip.startswith('192.168.') or customer_ip.startswith('10.') or customer_ip.startswith('172.'):
                anomalies.append("Transaction from private/local IP address")
                score_increase += 20
            
            # Check for known VPN/proxy ranges (simplified)
            suspicious_ip_ranges = ['45.', '103.', '185.', '198.']
            if any(customer_ip.startswith(range_) for range_ in suspicious_ip_ranges):
                anomalies.append("Transaction from potential VPN/proxy IP")
                score_increase += 30
            
            # Check for international IP with US address (simplified)
            international_ranges = ['41.', '103.', '115.', '200.']
            if any(customer_ip.startswith(range_) for range_ in international_ranges) and customer_state:
                anomalies.append("International IP with US address")
                score_increase += 40
        
        # Check for impossible travel patterns (if multiple transactions)
        # This would require checking previous transactions from same customer
        # For now, we'll do a simple distance check between city and typical locations
        
        return anomalies, score_increase
    
    def check_velocity_anomalies(self, df, current_index, customer_id, amount, transaction_time):
        """Check for velocity-based anomalies (frequency, amount patterns)"""
        anomalies = []
        score_increase = 0
        
        # Get all transactions for this customer up to current transaction
        customer_transactions = df[df['customer_id'] == customer_id].iloc[:current_index + 1]
        
        if len(customer_transactions) > 1:
            # Check for rapid successive transactions
            if len(customer_transactions) >= 3:
                # Check if 3+ transactions in last hour
                recent_transactions = 0
                current_time = pd.to_datetime(transaction_time)
                for _, tx in customer_transactions.iterrows():
                    tx_time = pd.to_datetime(tx['transaction_time'])
                    if (current_time - tx_time).total_seconds() <= 3600:  # 1 hour
                        recent_transactions += 1
                
                if recent_transactions >= 3:
                    anomalies.append("Multiple transactions within 1 hour")
                    score_increase += 35
            
            # Check for amount escalation pattern (card testing)
            amounts = customer_transactions['amount'].tolist()
            if len(amounts) >= 3:
                # Check if amounts are increasing rapidly
                if amounts[-1] > amounts[-2] * 3 and amounts[-2] > amounts[-3] * 2:
                    anomalies.append("Rapid amount escalation (card testing pattern)")
                    score_increase += 40
        
        return anomalies, score_increase
    
    def check_payment_anomalies(self, row):
        """Check for payment method and card-related anomalies"""
        anomalies = []
        score_increase = 0
        
        # Check payment method patterns
        payment_method = str(row.get('payment_method', '')).lower()
        card_last4 = str(row.get('card_last4', ''))
        response_code = str(row.get('response_code', ''))
        
        # Multiple payment method attempts (if available)
        # This would need transaction history - simplified for now
        
        # Check for failed payment indicators
        if response_code and response_code != '00':
            if response_code in ['05', '51', '14', '61']:
                anomalies.append(f"Payment declined (code: {response_code})")
                score_increase += 30
        
        # Check for suspicious card patterns
        if card_last4 and len(card_last4) == 4:
            # Sequential numbers (potential fake cards)
            if card_last4 in ['1234', '2345', '3456', '4567', '5678', '6789', '7890']:
                anomalies.append("Sequential card number pattern")
                score_increase += 45
            
            # Repeated digits
            if len(set(card_last4)) == 1:
                anomalies.append("Repeated digits in card number")
                score_increase += 35
        
        return anomalies, score_increase
    
    def check_behavioral_anomalies(self, row, df, current_index):
        """Check for unusual customer behavior patterns"""
        anomalies = []
        score_increase = 0
        
        amount = row.get('amount', 0)
        customer_id = row.get('customer_id', '')
        merchant_category = str(row.get('merchant_category', '')).lower()
        
        # Check for unusual merchant categories for customer (only if merchant_category is available)
        if customer_id and merchant_category:
            customer_history = df[df['customer_id'] == customer_id].iloc[:current_index]
            if len(customer_history) > 0 and 'merchant_category' in df.columns:
                # Get previous categories
                prev_categories = customer_history['merchant_category'].unique()
                
                # Check if this is a completely new category for regular customer
                if len(customer_history) >= 3 and merchant_category not in [cat.lower() for cat in prev_categories]:
                    anomalies.append("New merchant category for returning customer")
                    score_increase += 20
        
        # Check for round number amounts (often indicates fraud)
        if amount > 0 and amount == round(amount) and amount % 100 == 0:
            if amount >= 500:  # Round hundreds above $500
                anomalies.append(f"Suspicious round amount (${amount:,.0f})")
                score_increase += 25
        
        # Check for common fraud amounts
        common_fraud_amounts = [1.00, 5.00, 10.00, 100.00, 500.00, 1000.00]
        if amount in common_fraud_amounts:
            anomalies.append(f"Common fraud testing amount (${amount:.2f})")
            score_increase += 30
        
        return anomalies, score_increase
    
    def check_temporal_anomalies(self, row, df):
        """Check for time-based anomalies"""
        anomalies = []
        score_increase = 0
        
        transaction_time = str(row.get('transaction_time', ''))
        transaction_date = str(row.get('transaction_date', ''))
        
        if transaction_time and ':' in transaction_time:
            try:
                hour = int(transaction_time.split(':')[0])
                minute = int(transaction_time.split(':')[1])
                
                # Check for exact hour/minute patterns (automated/bot behavior)
                if minute == 0:  # Transactions exactly on the hour
                    hour_transactions = len(df[df['transaction_time'].str.startswith(f"{hour:02d}:00")])
                    if hour_transactions > len(df) * 0.1:  # More than 10% of transactions
                        anomalies.append("Unusual concentration of transactions at exact hour")
                        score_increase += 20
                
                # Weekend late-night transactions (higher risk)
                if transaction_date:
                    try:
                        date_obj = pd.to_datetime(transaction_date)
                        weekday = date_obj.dayofweek  # 0=Monday, 6=Sunday
                        if weekday >= 5 and (hour <= 6 or hour >= 23):  # Weekend nights
                            anomalies.append("Weekend late-night transaction")
                            score_increase += 15
                    except:
                        pass
                
                # Business hours anomaly for B2B transactions
                merchant_category = str(row.get('merchant_category', '')).lower()
                if any(term in merchant_category for term in ['business', 'office', 'professional']):
                    if hour < 8 or hour > 18:  # Outside business hours
                        anomalies.append("B2B transaction outside business hours")
                        score_increase += 20
                        
            except:
                pass
        
        return anomalies, score_increase
    
    def check_data_quality_anomalies(self, row):
        """Check for data quality issues that might indicate fraud"""
        anomalies = []
        score_increase = 0
        
        # Check for missing or suspicious data patterns
        customer_name = str(row.get('customer_name', '')).strip()
        customer_email = str(row.get('customer_email', '')).strip()
        customer_phone = str(row.get('customer_phone', '')).strip()
        
        # Suspicious name patterns
        if customer_name:
            name_lower = customer_name.lower()
            suspicious_names = ['test', 'demo', 'fake', 'admin', 'null', 'none']
            if any(sus in name_lower for sus in suspicious_names):
                anomalies.append("Suspicious customer name pattern")
                score_increase += 30
            
            # Very short names (less than 3 characters)
            if len(customer_name.replace(' ', '')) < 3:
                anomalies.append("Unusually short customer name")
                score_increase += 25
        
        # Email pattern checks
        if customer_email:
            email_lower = customer_email.lower()
            # Temporary email domains
            temp_domains = ['10minutemail', 'tempmail', 'guerrillamail', 'mailinator']
            if any(domain in email_lower for domain in temp_domains):
                anomalies.append("Temporary/disposable email address")
                score_increase += 35
            
            # Sequential email patterns
            if any(char.isdigit() for char in email_lower):
                digits = ''.join([c for c in email_lower if c.isdigit()])
                if len(digits) >= 4 and digits == sorted(digits):
                    anomalies.append("Sequential digits in email address")
                    score_increase += 20
        
        return anomalies, score_increase
    
    def detect_fraud(self, df):
        """Enhanced fraud detection with industry-specific rules and adaptive thresholds"""
        df_analyzed = df.copy()
        
        try:
            # Ensure amount is numeric
            df_analyzed['amount'] = pd.to_numeric(df_analyzed['amount'], errors='coerce').fillna(0)
            
            # Convert time columns for analysis
            df_analyzed['transaction_time'] = df_analyzed['transaction_time'].astype(str)
            df_analyzed['transaction_date'] = df_analyzed['transaction_date'].astype(str)
            
            # Enhanced risk scoring with industry-specific rules
            risk_scores = []
            risk_levels = []
            anomaly_flags = []
            industry_types = []
            
            for idx, row in df_analyzed.iterrows():
                score = 0
                amount = row.get('amount', 0)
                current_anomalies = []
                
                # Determine industry type for adaptive thresholds
                industry_type = self.get_industry_type(row)
                industry_types.append(industry_type)
                
                # Get industry-specific multiplier
                risk_multiplier = self.industry_patterns.get(industry_type, {}).get('risk_multiplier', 1.0)
                
                # 1. Industry-adaptive amount-based risk
                if industry_type == 'healthcare':
                    # Healthcare has different risk thresholds
                    if amount > 2000:
                        score += 50
                        current_anomalies.append("High healthcare transaction amount")
                    elif amount > 500:
                        score += 25
                elif industry_type == 'mobile_app':
                    # Mobile apps have lower typical amounts
                    if amount > 100:
                        score += 45
                        current_anomalies.append("High mobile app purchase amount")
                    elif amount < 1:
                        score += 35
                        current_anomalies.append("Very small amount (card testing)")
                elif industry_type == 'financial':
                    # Financial transactions have high scrutiny
                    if amount > 5000:
                        score += 60
                        current_anomalies.append("Large financial transaction")
                    elif amount > 1000:
                        score += 30
                else:
                    # General amount-based risk
                    if amount > 1000:
                        score += 40
                        current_anomalies.append("Large transaction amount")
                    elif amount > 500:
                        score += 20
                    elif amount < 5:
                        score += 30
                        current_anomalies.append("Very small amount (card testing)")
                    else:
                        score += 5
                
                # 2. Time-based risk with industry context
                if 'transaction_time' in df_analyzed.columns:
                    time_str = str(row.get('transaction_time', '12:00:00'))
                    try:
                        if ':' in time_str:
                            hour = int(time_str.split(':')[0])
                            
                            # Industry-specific time analysis
                            pattern = self.industry_patterns.get(industry_type, {})
                            peak_hours = pattern.get('peak_hours', [9, 10, 11, 14, 15, 16])
                            
                            if hour not in peak_hours:
                                if hour >= 22 or hour <= 6:  # Late night/early morning
                                    score += 25
                                    current_anomalies.append("Late night/early morning transaction")
                                else:
                                    score += 10  # Off-peak but not extreme
                    except:
                        pass
                
                # 3. Customer pattern risk
                if 'customer_id' in df_analyzed.columns:
                    customer_id = str(row.get('customer_id', ''))
                    if customer_id.startswith('CUST_') and random.random() < 0.1:
                        score += 15
                        current_anomalies.append("New customer pattern")
                
                # 4. Core anomaly checks
                geo_anomalies, geo_score = self.check_geographical_anomalies(row)
                score += geo_score
                current_anomalies.extend(geo_anomalies)
                
                velocity_anomalies, velocity_score = self.check_velocity_anomalies(
                    df_analyzed, idx, row.get('customer_id', ''), amount, row.get('transaction_time', '')
                )
                score += velocity_score
                current_anomalies.extend(velocity_anomalies)
                
                payment_anomalies, payment_score = self.check_payment_anomalies(row)
                score += payment_score
                current_anomalies.extend(payment_anomalies)
                
                behavioral_anomalies, behavioral_score = self.check_behavioral_anomalies(row, df_analyzed, idx)
                score += behavioral_score
                current_anomalies.extend(behavioral_anomalies)
                
                temporal_anomalies, temporal_score = self.check_temporal_anomalies(row, df_analyzed)
                score += temporal_score
                current_anomalies.extend(temporal_anomalies)
                
                quality_anomalies, quality_score = self.check_data_quality_anomalies(row)
                score += quality_score
                current_anomalies.extend(quality_anomalies)
                
                # 5. NEW: Industry-specific fraud checks
                if industry_type == 'mobile_app':
                    mobile_anomalies, mobile_score = self.check_mobile_app_fraud(row, df_analyzed, idx)
                    score += mobile_score
                    current_anomalies.extend(mobile_anomalies)
                
                elif industry_type == 'healthcare':
                    health_anomalies, health_score = self.check_healthcare_fraud(row, df_analyzed, idx)
                    score += health_score
                    current_anomalies.extend(health_anomalies)
                
                elif industry_type == 'gaming':
                    gaming_anomalies, gaming_score = self.check_gaming_fraud(row, df_analyzed, idx)
                    score += gaming_score
                    current_anomalies.extend(gaming_anomalies)
                
                elif industry_type == 'financial':
                    financial_anomalies, financial_score = self.check_financial_fraud(row, df_analyzed, idx)
                    score += financial_score
                    current_anomalies.extend(financial_anomalies)
                
                elif industry_type == 'subscription':
                    sub_anomalies, sub_score = self.check_subscription_fraud(row, df_analyzed, idx)
                    score += sub_score
                    current_anomalies.extend(sub_anomalies)
                
                # Apply industry risk multiplier
                score = int(score * risk_multiplier)
                
                # Add minimal randomness
                score += np.random.randint(0, 3)
                
                risk_scores.append(min(score, 100))
                anomaly_flags.append('; '.join(current_anomalies) if current_anomalies else 'None detected')
                
                # Industry-adaptive categorization
                if industry_type == 'healthcare':
                    # Healthcare is more conservative
                    if score > 60:
                        risk_levels.append('Needs Your Attention')
                    elif score > 30:
                        risk_levels.append('Watch Closely')
                    else:
                        risk_levels.append('Safe')
                elif industry_type == 'financial':
                    # Financial is most strict
                    if score > 50:
                        risk_levels.append('Needs Your Attention')
                    elif score > 25:
                        risk_levels.append('Watch Closely')
                    else:
                        risk_levels.append('Safe')
                elif industry_type == 'mobile_app':
                    # Mobile apps need higher thresholds due to legitimate high velocity
                    if score > 75:
                        risk_levels.append('Needs Your Attention')
                    elif score > 45:
                        risk_levels.append('Watch Closely')
                    else:
                        risk_levels.append('Safe')
                else:
                    # General thresholds
                    if score > 70:
                        risk_levels.append('Needs Your Attention')
                    elif score > 40:
                        risk_levels.append('Watch Closely')
                    else:
                        risk_levels.append('Safe')
            
            df_analyzed['risk_score'] = risk_scores
            df_analyzed['safety_level'] = risk_levels
            df_analyzed['anomaly_flags'] = anomaly_flags
            df_analyzed['industry_type'] = industry_types
            
            # Add hour for visualization
            if 'transaction_time' in df_analyzed.columns:
                hours = []
                for time_val in df_analyzed['transaction_time']:
                    try:
                        time_str = str(time_val)
                        if ':' in time_str:
                            hour = int(time_str.split(':')[0])
                            hours.append(hour)
                        else:
                            hours.append(12)
                    except:
                        hours.append(12)
                df_analyzed['hour'] = hours
            else:
                df_analyzed['hour'] = 12
            
            return df_analyzed
            
        except Exception as e:
            st.error(f"Error in fraud detection: {e}")
            # Ultra-simple fallback
            df_analyzed['risk_score'] = np.random.uniform(10, 70, len(df_analyzed))
            df_analyzed['safety_level'] = 'Safe'
            df_analyzed['anomaly_flags'] = 'None detected'
            df_analyzed['industry_type'] = 'general'
            df_analyzed['hour'] = 12
            return df_analyzed

    def get_industry_type(self, row):
        """Determine industry type from merchant category or transaction details"""
        merchant_category = str(row.get('merchant_category', '')).lower()
        merchant_name = str(row.get('merchant_name', '')).lower()
        
        # Mobile app indicators
        if any(term in merchant_category for term in ['gaming', 'mobile', 'app', 'game']):
            return 'mobile_app'
        if any(term in merchant_name for term in ['game', 'app', 'mobile']):
            return 'mobile_app'
            
        # Healthcare indicators
        if any(term in merchant_category for term in ['health', 'medical', 'telehealth', 'clinic']):
            return 'healthcare'
        if any(term in merchant_name for term in ['health', 'medical', 'clinic', 'doctor']):
            return 'healthcare'
            
        # Gaming (broader than mobile)
        if any(term in merchant_category for term in ['gaming', 'entertainment']):
            return 'gaming'
            
        # Financial services
        if any(term in merchant_category for term in ['financial', 'payment', 'bank', 'finance']):
            return 'financial'
            
        # Subscription services
        if any(term in merchant_category for term in ['subscription', 'saas', 'software']):
            return 'subscription'
            
        return 'general'

    def check_mobile_app_fraud(self, row, df, current_index):
        """Specialized fraud detection for mobile app transactions"""
        anomalies = []
        score_increase = 0
        
        amount = row.get('amount', 0)
        customer_id = row.get('customer_id', '')
        device_type = str(row.get('device_type', '')).lower()
        
        # Mobile app specific patterns
        pattern = self.industry_patterns['mobile_app']
        
        # 1. Device analysis
        if 'emulator' in device_type or 'simulator' in device_type:
            anomalies.append("Transaction from device emulator")
            score_increase += 50
        
        # 2. Amount pattern analysis for mobile apps
        if amount in pattern['suspicious_amounts']:
            anomalies.append(f"Suspicious mobile app amount (${amount})")
            score_increase += 40
        
        # 3. Micro-transaction abuse detection
        customer_transactions = df[df['customer_id'] == customer_id].iloc[:current_index + 1]
        if len(customer_transactions) >= 5:
            # Check for rapid small purchases (potential in-app purchase fraud)
            small_amounts = [tx for tx in customer_transactions['amount'] if tx < 5.0]
            if len(small_amounts) >= 5:
                anomalies.append("Multiple micro-transactions (potential fraud)")
                score_increase += 35
        
        # 4. Premium currency purchase patterns
        if amount > 99.99 and amount < pattern['typical_amounts'][1]:
            # Large currency purchases can indicate stolen accounts
            anomalies.append("Large virtual currency purchase")
            score_increase += 25
        
        # 5. Velocity checks specific to mobile gaming
        if len(customer_transactions) > pattern['velocity_threshold']:
            recent_hour_count = len([tx for _, tx in customer_transactions.iterrows() 
                                   if pd.to_datetime(tx['transaction_time']) > 
                                   pd.to_datetime(row['transaction_time']) - pd.Timedelta(hours=1)])
            if recent_hour_count > 10:
                anomalies.append("Excessive mobile app transactions per hour")
                score_increase += 45
        
        return anomalies, score_increase

    def check_healthcare_fraud(self, row, df, current_index):
        """Specialized fraud detection for healthcare transactions"""
        anomalies = []
        score_increase = 0
        
        amount = row.get('amount', 0)
        customer_id = row.get('customer_id', '')
        transaction_time = str(row.get('transaction_time', ''))
        
        pattern = self.industry_patterns['healthcare']
        
        # 1. Healthcare amount validation
        if amount > 5000:
            anomalies.append("Unusually high healthcare charge")
            score_increase += 40
        
        if amount in pattern['suspicious_amounts']:
            anomalies.append("Amount matches insurance fraud pattern")
            score_increase += 35
        
        # 2. Medical billing time patterns
        if transaction_time and ':' in transaction_time:
            try:
                hour = int(transaction_time.split(':')[0])
                # Medical services outside normal hours are suspicious
                if hour < 6 or hour > 22:
                    anomalies.append("Healthcare transaction outside normal hours")
                    score_increase += 30
            except:
                pass
        
        # 3. Rapid medical service billing (potential billing fraud)
        customer_transactions = df[df['customer_id'] == customer_id].iloc[:current_index + 1]
        if len(customer_transactions) > pattern['velocity_threshold']:
            # Multiple medical services in short time is suspicious
            same_day_transactions = len([tx for _, tx in customer_transactions.iterrows() 
                                       if tx['transaction_date'] == row['transaction_date']])
            if same_day_transactions > 3:
                anomalies.append("Multiple healthcare charges same day")
                score_increase += 40
        
        # 4. Insurance billing patterns
        # Check for amounts just under insurance limits
        insurance_limits = [999.99, 1999.99, 4999.99]
        if any(abs(amount - limit) < 0.01 for limit in insurance_limits):
            anomalies.append("Amount matches insurance limit avoidance")
            score_increase += 30
        
        # 5. Age verification for certain procedures
        customer_email = str(row.get('customer_email', '')).lower()
        if any(term in customer_email for term in ['youth', 'teen', 'kid', 'child']):
            if amount > 1000:
                anomalies.append("High-value healthcare for youth account")
                score_increase += 25
        
        return anomalies, score_increase

    def check_gaming_fraud(self, row, df, current_index):
        """Enhanced gaming fraud detection"""
        anomalies = []
        score_increase = 0
        
        amount = row.get('amount', 0)
        customer_id = row.get('customer_id', '')
        
        pattern = self.industry_patterns['gaming']
        
        # 1. Whale detection
        if amount > pattern['whale_threshold']:
            # Large spenders need verification
            anomalies.append("High-value gaming purchase (whale behavior)")
            score_increase += 20  # Lower score for whales as they're often legitimate
        
        # 2. Card testing in gaming
        if amount in pattern['common_fraud_amounts']:
            anomalies.append("Common gaming fraud testing amount")
            score_increase += 35
        
        # 3. Account takeover patterns
        customer_transactions = df[df['customer_id'] == customer_id].iloc[:current_index + 1]
        if len(customer_transactions) > 1:
            # Sudden spending spike indicates account takeover
            avg_amount = customer_transactions['amount'].mean()
            if amount > avg_amount * 5:
                anomalies.append("Sudden gaming spending spike")
                score_increase += 45
        
        return anomalies, score_increase

    def check_financial_fraud(self, row, df, current_index):
        """Enhanced financial services fraud detection"""
        anomalies = []
        score_increase = 0
        
        amount = row.get('amount', 0)
        pattern = self.industry_patterns['financial']
        
        # 1. Structuring detection (BSA compliance)
        if amount >= pattern['structuring_threshold'] * 0.9:  # 90% of threshold
            anomalies.append("Amount near structuring threshold")
            score_increase += 50
        
        if amount in pattern['high_risk_amounts']:
            anomalies.append("Amount matches structuring pattern")
            score_increase += 60
        
        # 2. Round amount detection for money laundering
        if amount >= 1000 and amount % 1000 == 0:
            anomalies.append("Large round amount (potential money laundering)")
            score_increase += 40
        
        return anomalies, score_increase

    def check_subscription_fraud(self, row, df, current_index):
        """Enhanced subscription fraud detection"""
        anomalies = []
        score_increase = 0
        
        amount = row.get('amount', 0)
        customer_email = str(row.get('customer_email', '')).lower()
        pattern = self.industry_patterns['subscription']
        
        # 1. Trial abuse detection
        if amount in pattern['common_amounts'][:2]:  # Small trial amounts
            # Check for disposable email patterns
            disposable_patterns = ['temp', '10min', 'guerrilla', 'mailinator']
            if any(pattern in customer_email for pattern in disposable_patterns):
                anomalies.append("Trial abuse with disposable email")
                score_increase += 45
        
        # 2. Subscription jumping (rapid cancellation/renewal)
        customer_id = row.get('customer_id', '')
        customer_transactions = df[df['customer_id'] == customer_id].iloc[:current_index + 1]
        
        if len(customer_transactions) >= pattern['trial_abuse_threshold']:
            trial_transactions = [tx for tx in customer_transactions['amount'] if tx < 2.0]
            if len(trial_transactions) >= 3:
                anomalies.append("Multiple trial subscriptions (abuse pattern)")
                score_increase += 50
        
        return anomalies, score_increase

    def check_fraud(self, row, df, current_index):
        """Comprehensive fraud check combining all methods"""
        anomalies = []
        score_increase = 0
        
        # 1. Geographical anomalies
        geo_anomalies, geo_score = self.check_geographical_anomalies(row)
        anomalies.extend(geo_anomalies)
        score_increase += geo_score
        
        # 2. Velocity anomalies
        velocity_anomalies, velocity_score = self.check_velocity_anomalies(df, current_index, 
                                                                        row.get('customer_id', ''), 
                                                                        row.get('amount', 0), 
                                                                        row.get('transaction_time', ''))
        anomalies.extend(velocity_anomalies)
        score_increase += velocity_score
        
        # 3. Payment anomalies
        payment_anomalies, payment_score = self.check_payment_anomalies(row)
        anomalies.extend(payment_anomalies)
        score_increase += payment_score
        
        # 4. Behavioral anomalies
        behavioral_anomalies, behavioral_score = self.check_behavioral_anomalies(row, df, current_index)
        anomalies.extend(behavioral_anomalies)
        score_increase += behavioral_score
        
        # 5. Temporal anomalies
        temporal_anomalies, temporal_score = self.check_temporal_anomalies(row, df)
        anomalies.extend(temporal_anomalies)
        score_increase += temporal_score
        
        # 6. Data quality anomalies
        quality_anomalies, quality_score = self.check_data_quality_anomalies(row)
        anomalies.extend(quality_anomalies)
        score_increase += quality_score
        
        # 7. Industry-specific checks
        industry_type = self.get_industry_type(row)
        
        if industry_type == 'mobile_app':
            mobile_anomalies, mobile_score = self.check_mobile_app_fraud(row, df, current_index)
            anomalies.extend(mobile_anomalies)
            score_increase += mobile_score
        elif industry_type == 'healthcare':
            healthcare_anomalies, healthcare_score = self.check_healthcare_fraud(row, df, current_index)
            anomalies.extend(healthcare_anomalies)
            score_increase += healthcare_score
        elif industry_type == 'gaming':
            gaming_anomalies, gaming_score = self.check_gaming_fraud(row, df, current_index)
            anomalies.extend(gaming_anomalies)
            score_increase += gaming_score
        elif industry_type == 'financial':
            financial_anomalies, financial_score = self.check_financial_fraud(row, df, current_index)
            anomalies.extend(financial_anomalies)
            score_increase += financial_score
        elif industry_type == 'subscription':
            subscription_anomalies, subscription_score = self.check_subscription_fraud(row, df, current_index)
            anomalies.extend(subscription_anomalies)
            score_increase += subscription_score
        
        # Cap the score to 100
        score_increase = min(score_increase, 100)
        
        return anomalies, score_increase

def create_smb_friendly_charts(df_analyzed):
    """Create simple, easy-to-understand charts for SMB owners"""
    
    charts = {}
    
    try:
        # 1. Simple Daily Transaction Count
        daily_counts = df_analyzed.groupby('transaction_date').size().reset_index(name='transactions')
        
        if len(daily_counts) > 0:
            charts['daily_simple'] = px.bar(
                daily_counts,
                x='transaction_date',
                y='transactions',
                title='Daily Payments to Your Business',
                color_discrete_sequence=['#0ea5e9']  # Professional primary blue
            )
            charts['daily_simple'].update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                title_font_size=20,
                title_font_color='#0f172a',  # Deep slate
                title_font_family="Open Sans, Arial, sans-serif",
                xaxis_title="Date",
                yaxis_title="Number of Payments",
                font_family="Open Sans, Arial, sans-serif",
                font_size=14,
                height=400,
                showlegend=False,
                margin=dict(t=60, b=60, l=60, r=60),
                title_x=0.5  # Center the title
            )
            charts['daily_simple'].update_traces(
                marker_line_color='#0284c7',  # Darker blue border
                marker_line_width=1.5,
                hovertemplate='<b>%{x}</b><br>Payments: %{y}<extra></extra>'
            )
            charts['daily_simple'].update_xaxes(
                title_font_size=16,
                title_font_color='#374151',
                tickfont_size=12,
                tickfont_color='#6b7280'
            )
            charts['daily_simple'].update_yaxes(
                title_font_size=16,
                title_font_color='#374151',
                tickfont_size=12,
                tickfont_color='#6b7280'
            )
        else:
            charts['daily_simple'] = None
    
    except Exception as e:
        st.warning(f"Could not create daily chart: {e}")
        charts['daily_simple'] = None
    
    try:
        # 2. Traffic Light Safety Overview
        if 'safety_level' in df_analyzed.columns:
            safety_counts = df_analyzed['safety_level'].value_counts()
            
            # Ensure all categories are present
            categories = ['Safe', 'Watch Closely', 'Needs Your Attention']
            safety_data = []
            colors = ['#22c55e', '#f59e0b', '#ef4444']  # Professional status colors
            
            for i, category in enumerate(categories):
                count = safety_counts.get(category, 0)
                safety_data.append({
                    'Category': category,
                    'Count': count,
                    'Percentage': round((count / len(df_analyzed)) * 100, 1) if len(df_analyzed) > 0 else 0
                })
            
            safety_df = pd.DataFrame(safety_data)
            
            charts['safety_overview'] = px.bar(
                safety_df,
                x='Category',
                y='Count',
                title='Payment Safety Overview',
                color='Category',
                color_discrete_map={
                    'Safe': '#22c55e',         # Professional green
                    'Watch Closely': '#f59e0b', # Professional amber
                    'Needs Your Attention': '#ef4444'  # Professional red
                }
            )
            charts['safety_overview'].update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                title_font_size=20,
                title_font_color='#0f172a',
                title_font_family="Open Sans, Arial, sans-serif",
                xaxis_title="Safety Level",
                yaxis_title="Number of Payments",
                font_family="Open Sans, Arial, sans-serif",
                font_size=14,
                height=400,
                showlegend=False,
                margin=dict(t=60, b=60, l=60, r=60),
                title_x=0.5  # Center the title
            )
            charts['safety_overview'].update_traces(
                marker_line_width=1.5,
                hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>'
            )
            charts['safety_overview'].update_xaxes(
                title_font_size=16,
                title_font_color='#374151',
                tickfont_size=12,
                tickfont_color='#6b7280'
            )
            charts['safety_overview'].update_yaxes(
                title_font_size=16,
                title_font_color='#374151',
                tickfont_size=12,
                tickfont_color='#6b7280'
            )
        else:
            charts['safety_overview'] = None
    
    except Exception as e:
        st.warning(f"Could not create safety overview: {e}")
        charts['safety_overview'] = None
    
    return charts

def display_smb_status(df_analyzed):
    """Display simple status for SMB owners"""
    
    total_transactions = len(df_analyzed)
    
    if 'safety_level' in df_analyzed.columns:
        needs_attention = len(df_analyzed[df_analyzed['safety_level'] == 'Needs Your Attention'])
        watch_closely = len(df_analyzed[df_analyzed['safety_level'] == 'Watch Closely'])
        safe_payments = len(df_analyzed[df_analyzed['safety_level'] == 'Safe'])
    else:
        # Fallback if safety_level doesn't exist
        needs_attention = len(df_analyzed[df_analyzed.get('risk_score', 0) > 70])
        watch_closely = len(df_analyzed[(df_analyzed.get('risk_score', 0) > 40) & (df_analyzed.get('risk_score', 0) <= 70)])
        safe_payments = len(df_analyzed[df_analyzed.get('risk_score', 0) <= 40])
    
    # Calculate potential money at risk
    if 'amount' in df_analyzed.columns and 'safety_level' in df_analyzed.columns:
        money_at_risk = df_analyzed[df_analyzed['safety_level'] == 'Needs Your Attention']['amount'].sum()
    else:
        money_at_risk = 0
    
    # Determine overall status
    if needs_attention == 0:
        status = "EXCELLENT"
        status_class = "status-good"
        status_message = "🛡️ Your business is well protected! All payments look normal."
    elif needs_attention <= total_transactions * 0.05:  # Less than 5%
        status = "GOOD"
        status_class = "status-good"
        status_message = f"✅ Only {needs_attention} payments need attention. You're doing great!"
    elif needs_attention <= total_transactions * 0.15:  # 5-15%
        status = "WATCH"
        status_class = "status-warning"
        status_message = f"⚠️ {needs_attention} payments need your review. Check them when you can."
    else:
        status = "ACTION NEEDED"
        status_class = "status-danger"
        status_message = f"🚨 {needs_attention} payments need immediate attention!"
    
    # Display status
    st.markdown(f'<div class="{status_class}">Security Status: {status}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="explanation-box"><div class="explanation-text">{status_message}</div></div>', unsafe_allow_html=True)
    
    # Big number cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="big-number-card all-good">
            <p class="big-number">{safe_payments:,}</p>
            <p class="big-label">Safe Payments</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if watch_closely > 0:
            st.markdown(f"""
            <div class="big-number-card watch-closely">
                <p class="big-number">{watch_closely:,}</p>
                <p class="big-label">Watch Closely</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="big-number-card all-good">
                <p class="big-number">{watch_closely:,}</p>
                <p class="big-label">Watch Closely</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col3:
        if needs_attention > 0:
            st.markdown(f"""
            <div class="big-number-card action-needed">
                <p class="big-number">{needs_attention:,}</p>
                <p class="big-label">Need Attention</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="big-number-card all-good">
                <p class="big-number">{needs_attention:,}</p>
                <p class="big-label">Need Attention</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col4:
        if money_at_risk > 0:
            st.markdown(f"""
            <div class="big-number-card action-needed">
                <p class="big-number">${money_at_risk:,.0f}</p>
                <p class="big-label">Money at Risk</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="big-number-card all-good">
                <p class="big-number">$0</p>
                <p class="big-label">Money at Risk</p>
            </div>
            """, unsafe_allow_html=True)
    
    return needs_attention, safe_payments, money_at_risk

def display_simple_charts(charts):
    """Display simplified charts"""
    
    if charts.get('daily_simple'):
        st.markdown('<div class="simple-chart">', unsafe_allow_html=True)
        st.plotly_chart(charts['daily_simple'], use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="explanation-box">
            <div class="explanation-title">What This Shows</div>
            <div class="explanation-text">This chart shows how many payments you received each day. Look for unusual spikes or patterns that don't match your normal business.</div>
        </div>
        """, unsafe_allow_html=True)
    
    if charts.get('safety_overview'):
        st.markdown('<div class="simple-chart">', unsafe_allow_html=True)
        st.plotly_chart(charts['safety_overview'], use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="explanation-box">
            <div class="explanation-title">How to Read This</div>
            <div class="explanation-text">
                • <strong>Safe:</strong> Normal payments that look good<br>
                • <strong>Watch Closely:</strong> Slightly unusual but probably okay<br>
                • <strong>Needs Attention:</strong> Check these payments - they might be fraud
            </div>
        </div>
        """, unsafe_allow_html=True)

def display_action_items(df_analyzed, needs_attention):
    """Display clear action items for SMB owners"""
    
    st.markdown("## 🎯 What Should You Do Now?")
    
    if needs_attention > 0:
        # Show urgent button
        st.markdown(f"""
        <button class="urgent-button">
            🚨 Review {needs_attention} Suspicious Payment{"s" if needs_attention > 1 else ""} Now
        </button>
        """, unsafe_allow_html=True)
        
        # Enhanced Payments That Need Your Attention section
        display_enhanced_risky_transactions(df_analyzed, needs_attention)
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown('<button class="action-button">📞 Call Customers</button>', unsafe_allow_html=True)
        with col2:
            st.markdown('<button class="action-button">✅ Mark as Safe</button>', unsafe_allow_html=True)
        with col3:
            st.markdown('<button class="action-button">🚫 Block Payment</button>', unsafe_allow_html=True)
    
    else:
        # All good message
        st.markdown("""
        <div class="explanation-box" style="background: linear-gradient(135deg, var(--success-50) 0%, white 100%); border: 1px solid var(--success-200);">
            <div class="explanation-title" style="color: var(--success-700);">🎉 Great News!</div>
            <div class="explanation-text" style="color: var(--success-800);">All your payments look normal and safe. Keep up the good work! We'll continue monitoring your transactions automatically.</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<button class="action-button">📊 View Detailed Report</button>', unsafe_allow_html=True)

def display_enhanced_risky_transactions(df_analyzed, needs_attention):
    """Enhanced display for risky transactions with summary and detailed views"""
    
    st.markdown("### 🔍 Payments That Need Your Attention")
    
    # Get all risky transactions
    if 'safety_level' in df_analyzed.columns:
        risky_transactions = df_analyzed[df_analyzed['safety_level'] == 'Needs Your Attention'].copy()
    else:
        risky_transactions = df_analyzed[df_analyzed['risk_score'] > 70].copy()
    
    if risky_transactions.empty:
        st.info("No high-risk transactions found.")
        return
    
    # Add tabs for different views
    tab1, tab2, tab3 = st.tabs(["📊 Summary Overview", "🔍 Detailed View", "📈 Risk Analysis"])
    
    with tab1:
        # Summary Overview Tab
        st.markdown("#### 📊 Quick Summary")
        
        # Risk summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        total_amount_at_risk = risky_transactions['amount'].sum()
        avg_risk_score = risky_transactions['risk_score'].mean()
        highest_risk_score = risky_transactions['risk_score'].max()
        unique_customers = risky_transactions['customer_id'].nunique()
        
        with col1:
            st.metric("💰 Total Amount at Risk", f"${total_amount_at_risk:,.2f}")
        with col2:
            st.metric("📊 Average Risk Score", f"{avg_risk_score:.1f}/100")
        with col3:
            st.metric("🚨 Highest Risk Score", f"{highest_risk_score}/100")
        with col4:
            st.metric("👥 Affected Customers", str(unique_customers))
        
        # Risk categories breakdown
        st.markdown("#### 🏷️ Risk Categories")
        
        # Analyze risk patterns
        risk_categories = {}
        for _, row in risky_transactions.iterrows():
            anomalies = str(row.get('anomaly_flags', ''))
            amount = row.get('amount', 0)
            
            # Categorize risks
            if 'geographical' in anomalies.lower() or 'zip' in anomalies.lower() or 'ip' in anomalies.lower():
                risk_categories['Geographic Mismatch'] = risk_categories.get('Geographic Mismatch', 0) + 1
            if 'multiple transactions' in anomalies.lower() or 'velocity' in anomalies.lower():
                risk_categories['High Velocity'] = risk_categories.get('High Velocity', 0) + 1
            if 'large' in anomalies.lower() or amount > 1000:
                risk_categories['Large Amount'] = risk_categories.get('Large Amount', 0) + 1
            if 'late night' in anomalies.lower() or 'early morning' in anomalies.lower():
                risk_categories['Unusual Hours'] = risk_categories.get('Unusual Hours', 0) + 1
            if 'card' in anomalies.lower() or 'payment' in anomalies.lower():
                risk_categories['Payment Issues'] = risk_categories.get('Payment Issues', 0) + 1
            if 'emulator' in anomalies.lower() or 'device' in anomalies.lower():
                risk_categories['Device Fraud'] = risk_categories.get('Device Fraud', 0) + 1
        
        # Display risk categories
        for category, count in sorted(risk_categories.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / len(risky_transactions)) * 100
            st.markdown(f"""
            <div class="risk-category-item" style="border-left-color: var(--error-500);">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <strong style="color: var(--gray-900);">{category}</strong>
                    <span style="background: linear-gradient(135deg, var(--error-500), var(--error-600)); color: white; padding: 0.375rem 0.875rem; border-radius: var(--radius-xl); font-size: var(--text-sm); font-weight: 600; box-shadow: var(--shadow-sm);">{count} times</span>
                </div>
                <div style="background: var(--error-100); height: 6px; border-radius: var(--radius-sm); margin-top: 0.75rem; overflow: hidden;">
                    <div style="background: linear-gradient(90deg, var(--error-500), var(--error-600)); height: 6px; border-radius: var(--radius-sm); width: {min(percentage, 100)}%; transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);"></div>
                </div>
                <div style="font-size: var(--text-xs); color: var(--gray-600); margin-top: 0.5rem; font-weight: 500;">{percentage:.1f}% of risky transactions</div>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        # Detailed View Tab
        st.markdown("#### 🔍 All Risky Transactions")
        
        # Simple filter dropdowns
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Risk level filter (simplified categories)
            st.markdown("**🚨 Risk Level**")
            risk_level_options = {
                "All Risk Levels": 0,
                "🔵 Mildly Concerning & Up": 50,
                "🟡 Somewhat Risky & Up": 60,
                "🔴 Very Suspicious Only": 80
            }
            selected_risk_level = st.selectbox(
                "Choose risk level:",
                options=list(risk_level_options.keys()),
                index=2,  # Default to "Somewhat Risky & Up"
                help="Filter by how suspicious the transactions are",
                label_visibility="collapsed"
            )
            min_risk_score = risk_level_options[selected_risk_level]
            filtered_transactions = risky_transactions[risky_transactions['risk_score'] >= min_risk_score]
        
        with col2:
            # Amount range filter (business-friendly ranges)
            st.markdown("**💰 Transaction Size**")
            amount_options = {
                "All Amounts": 0,
                "Small ($1 - $99)": (1, 99),
                "Medium ($100 - $499)": (100, 499),
                "Large ($500 - $999)": (500, 999),
                "Very Large ($1,000+)": (1000, float('inf'))
            }
            selected_amount_range = st.selectbox(
                "Choose transaction size:",
                options=list(amount_options.keys()),
                index=0,  # Default to "All Amounts"
                help="Filter by transaction size",
                label_visibility="collapsed"
            )
            
            if selected_amount_range != "All Amounts":
                min_amt, max_amt = amount_options[selected_amount_range]
                if max_amt == float('inf'):
                    filtered_transactions = filtered_transactions[filtered_transactions['amount'] >= min_amt]
                else:
                    filtered_transactions = filtered_transactions[
                        (filtered_transactions['amount'] >= min_amt) & 
                        (filtered_transactions['amount'] <= max_amt)
                    ]
        
        with col3:
            # Enhanced date filter with business-friendly options
            st.markdown("**📅 Date Range**")
            if 'transaction_date' in risky_transactions.columns:
                # Convert string dates to datetime for easier manipulation
                try:
                    risky_transactions['transaction_date_dt'] = pd.to_datetime(risky_transactions['transaction_date'])
                    filtered_transactions['transaction_date_dt'] = pd.to_datetime(filtered_transactions['transaction_date'])
                    
                    # Get date range from data
                    min_date = risky_transactions['transaction_date_dt'].min().date()
                    max_date = risky_transactions['transaction_date_dt'].max().date()
                    
                    # Calculate business-friendly date ranges
                    today = pd.Timestamp.now().date()
                    
                    # Create smart date filter options
                    date_filter_options = [
                        "All Dates",
                        "📊 Last 7 Days", 
                        "� Last 30 Days",
                        "📋 Last 90 Days",
                        "📅 Year to Date",
                        "�️ Custom Date Range"
                    ]
                    
                    selected_date_option = st.selectbox(
                        "Choose time period:",
                        options=date_filter_options,
                        index=0,  # Default to "All Dates"
                        help="Filter transactions by date range",
                        label_visibility="collapsed"
                    )
                    
                    # Apply date filters based on selection
                    if selected_date_option == "� Last 7 Days":
                        cutoff_date = today - pd.Timedelta(days=7)
                        filtered_transactions = filtered_transactions[filtered_transactions['transaction_date_dt'].dt.date >= cutoff_date]
                    elif selected_date_option == "� Last 30 Days":
                        cutoff_date = today - pd.Timedelta(days=30)
                        filtered_transactions = filtered_transactions[filtered_transactions['transaction_date_dt'].dt.date >= cutoff_date]
                    elif selected_date_option == "📋 Last 90 Days":
                        cutoff_date = today - pd.Timedelta(days=90)
                        filtered_transactions = filtered_transactions[filtered_transactions['transaction_date_dt'].dt.date >= cutoff_date]
                    elif selected_date_option == "📅 Year to Date":
                        year_start = pd.Timestamp(today.year, 1, 1).date()
                        filtered_transactions = filtered_transactions[filtered_transactions['transaction_date_dt'].dt.date >= year_start]
                    elif selected_date_option == "🗓️ Custom Date Range":
                        # Show date range picker
                        st.markdown("**Select Custom Date Range:**")
                        col_start, col_end = st.columns(2)
                        
                        with col_start:
                            start_date = st.date_input(
                                "From:",
                                value=min_date,
                                min_value=min_date,
                                max_value=max_date,
                                help="Start date for filtering"
                            )
                        
                        with col_end:
                            end_date = st.date_input(
                                "To:",
                                value=max_date,
                                min_value=min_date,
                                max_value=max_date,
                                help="End date for filtering"
                            )
                        
                        # Apply custom date range
                        if start_date <= end_date:
                            filtered_transactions = filtered_transactions[
                                (filtered_transactions['transaction_date_dt'].dt.date >= start_date) &
                                (filtered_transactions['transaction_date_dt'].dt.date <= end_date)
                            ]
                        else:
                            st.error("Start date must be before or equal to end date")
                    
                    # Drop the temporary datetime column
                    if 'transaction_date_dt' in filtered_transactions.columns:
                        filtered_transactions = filtered_transactions.drop('transaction_date_dt', axis=1)
                        
                except Exception as e:
                    # Fallback to simple date filter if datetime conversion fails
                    st.selectbox(
                        "Choose date range:",
                        options=["All Dates (Date format issue)"],
                        disabled=True,
                        help="Date filtering unavailable due to format issues",
                        label_visibility="collapsed"
                    )
            else:
                st.selectbox(
                    "Choose date range:",
                    options=["Date info not available"],
                    disabled=True,
                    label_visibility="collapsed"
                )
        
        # Results summary with better styling
        result_count = len(filtered_transactions)
        total_count = len(risky_transactions)
        
        if result_count < total_count:
            st.markdown(f"""
            <div style="background: #EFF6FF; padding: 1rem; border-radius: 6px; margin: 1rem 0; border-left: 4px solid #3B82F6;">
                <p style="margin: 0; color: #1E40AF; font-weight: 600;">
                    🔍 Showing <strong>{result_count}</strong> of <strong>{total_count}</strong> risky transactions
                </p>
                <p style="margin: 0.25rem 0 0 0; color: #1D4ED8; font-size: 0.9rem;">
                    {total_count - result_count} transactions filtered out
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background: #F0FDF4; padding: 1rem; border-radius: 6px; margin: 1rem 0; border-left: 4px solid #10B981;">
                <p style="margin: 0; color: #166534; font-weight: 600;">
                    📋 Showing all <strong>{result_count}</strong> risky transactions
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        # Display filtered transactions with pagination
        transactions_per_page = 10
        total_pages = max(1, (len(filtered_transactions) + transactions_per_page - 1) // transactions_per_page)
        
        if total_pages > 1:
            page = st.selectbox("Page", range(1, total_pages + 1), help=f"Navigate through {total_pages} pages")
            start_idx = (page - 1) * transactions_per_page
            end_idx = start_idx + transactions_per_page
            page_transactions = filtered_transactions.iloc[start_idx:end_idx]
        else:
            page_transactions = filtered_transactions
        
        # Display transactions
        for idx, (_, row) in enumerate(page_transactions.iterrows()):
            amount = row.get('amount', 0)
            date = row.get('transaction_date', 'Unknown')
            time = row.get('transaction_time', 'Unknown')
            customer = row.get('customer_id', 'Unknown')
            customer_name = row.get('customer_name', 'Unknown Customer')
            risk_score = row.get('risk_score', 0)
            anomalies = row.get('anomaly_flags', 'Unknown patterns')
            
            # Create expandable transaction details
            with st.expander(f"💰 ${amount:,.2f} - {customer_name} (Risk: {risk_score}/100)", expanded=False):
                
                col_a, col_b = st.columns(2)
                
                with col_a:
                    st.markdown("**Transaction Details:**")
                    st.write(f"• **Date & Time:** {date} at {time}")
                    st.write(f"• **Customer ID:** {customer}")
                    st.write(f"• **Customer Name:** {customer_name}")
                    if 'customer_email' in row:
                        st.write(f"• **Email:** {row.get('customer_email', 'N/A')}")
                    if 'customer_phone' in row:
                        st.write(f"• **Phone:** {row.get('customer_phone', 'N/A')}")
                
                with col_b:
                    st.markdown("**Location Information:**")
                    if 'customer_city' in row and 'customer_state' in row:
                        st.write(f"• **Location:** {row.get('customer_city', '')}, {row.get('customer_state', '')} {row.get('customer_zip_code', '')}")
                    if 'customer_ip_address' in row:
                        st.write(f"• **IP Address:** {row.get('customer_ip_address', '')}")
                    if 'industry_type' in row:
                        st.write(f"• **Industry:** {row.get('industry_type', 'General').title()}")
                
                # Risk factors
                st.markdown("**🚨 Risk Factors:**")
                if anomalies and anomalies != 'None detected':
                    risk_factors = [factor.strip() for factor in anomalies.split(';')]
                    for factor in risk_factors:
                        if factor:
                            st.write(f"⚠️ {factor}")
                else:
                    st.write("⚠️ General risk pattern detected")
                
                # Action buttons for individual transaction
                btn_col1, btn_col2, btn_col3 = st.columns(3)
                with btn_col1:
                    if st.button(f"✅ Mark Safe", key=f"safe_{idx}"):
                        st.success(f"Transaction marked as safe")
                with btn_col2:
                    if st.button(f"📞 Call Customer", key=f"call_{idx}"):
                        st.info(f"Calling customer at {row.get('customer_phone', 'N/A')}")
                with btn_col3:
                    if st.button(f"🚫 Block", key=f"block_{idx}"):
                        st.error(f"Transaction blocked")
    
    with tab3:
        # Risk Analysis Tab - Simplified for Small Business Owners
        st.markdown("#### 📈 Understanding Your Risk Patterns")
        
        # Simple risk level breakdown
        st.markdown("**🚦 How Risky Are These Transactions?**")
        
        # Create simple risk categories
        high_risk = len(risky_transactions[risky_transactions['risk_score'] >= 80])
        medium_risk = len(risky_transactions[(risky_transactions['risk_score'] >= 60) & (risky_transactions['risk_score'] < 80)])
        low_risk = len(risky_transactions[risky_transactions['risk_score'] < 60])
        
        # Simple traffic light display
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, var(--error-50) 0%, white 100%); padding: 2rem; border-radius: var(--radius-2xl); text-align: center; border: 1px solid var(--error-200); box-shadow: var(--shadow-lg); position: relative; overflow: hidden;">
                <div style="position: absolute; top: 0; left: 0; right: 0; height: 4px; background: linear-gradient(90deg, var(--error-500), var(--error-600));"></div>
                <h2 style="color: var(--error-600); margin: 0; font-size: var(--text-4xl); font-weight: 800; font-family: Inter, sans-serif;">{high_risk}</h2>
                <p style="margin: 0.5rem 0; font-weight: 600; color: var(--error-700); font-size: var(--text-lg);">🔴 Very Suspicious</p>
                <p style="margin: 0; font-size: var(--text-sm); color: var(--error-600); font-weight: 500;">Check these first!</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, var(--warning-50) 0%, white 100%); padding: 2rem; border-radius: var(--radius-2xl); text-align: center; border: 1px solid var(--warning-200); box-shadow: var(--shadow-lg); position: relative; overflow: hidden;">
                <div style="position: absolute; top: 0; left: 0; right: 0; height: 4px; background: linear-gradient(90deg, var(--warning-500), var(--warning-600));"></div>
                <h2 style="color: var(--warning-600); margin: 0; font-size: var(--text-4xl); font-weight: 800; font-family: Inter, sans-serif;">{medium_risk}</h2>
                <p style="margin: 0.5rem 0; font-weight: 600; color: var(--warning-700); font-size: var(--text-lg);">🟡 Somewhat Risky</p>
                <p style="margin: 0; font-size: var(--text-sm); color: var(--warning-600); font-weight: 500;">Review when you can</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, var(--primary-50) 0%, white 100%); padding: 2rem; border-radius: var(--radius-2xl); text-align: center; border: 1px solid var(--primary-200); box-shadow: var(--shadow-lg); position: relative; overflow: hidden;">
                <div style="position: absolute; top: 0; left: 0; right: 0; height: 4px; background: linear-gradient(90deg, var(--primary-500), var(--primary-600));"></div>
                <h2 style="color: var(--primary-600); margin: 0; font-size: var(--text-4xl); font-weight: 800; font-family: Inter, sans-serif;">{low_risk}</h2>
                <p style="margin: 0.5rem 0; font-weight: 600; color: var(--primary-700); font-size: var(--text-lg);">🔵 Mildly Concerning</p>
                <p style="margin: 0; font-size: var(--text-sm); color: var(--primary-600); font-weight: 500;">Keep an eye on these</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Simple explanation
        st.markdown("""
        <div style="background: linear-gradient(135deg, var(--gray-50) 0%, white 100%); padding: 2rem; border-radius: var(--radius-xl); margin: 2rem 0; border: 1px solid var(--gray-200); box-shadow: var(--shadow-md); position: relative;">
            <div style="position: absolute; top: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg, var(--success-500), var(--success-600));"></div>
            <p style="margin: 0; color: var(--gray-900); font-weight: 600; font-size: var(--text-lg); margin-bottom: 0.75rem;">💡 What This Means:</p>
            <p style="margin: 0; color: var(--gray-700); line-height: 1.6;">Start with the <span style="color: var(--error-600); font-weight: 600;">Very Suspicious (Red)</span> transactions - these are most likely to be fraud. The <span style="color: var(--warning-600); font-weight: 600;">Somewhat Risky (Yellow)</span> ones can wait until you have time, and the <span style="color: var(--primary-600); font-weight: 600;">Mildly Concerning (Blue)</span> ones are probably fine but worth a quick look.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Simple transaction size breakdown
        st.markdown("**💰 What Size Transactions Are Risky?**")
        
        # Create simple amount categories
        small_amounts = len(risky_transactions[risky_transactions['amount'] < 100])
        medium_amounts = len(risky_transactions[(risky_transactions['amount'] >= 100) & (risky_transactions['amount'] < 500)])
        large_amounts = len(risky_transactions[risky_transactions['amount'] >= 500])
        
        # Simple bar chart data
        amounts_data = pd.DataFrame({
            'Amount Range': ['Under $100', '$100 - $500', 'Over $500'],
            'Count': [small_amounts, medium_amounts, large_amounts],
            'Description': ['Small purchases', 'Medium purchases', 'Large purchases']
        })
        
        # Create simple bar chart
        fig_amounts = px.bar(
            amounts_data,
            x='Amount Range',
            y='Count',
            title="How Many Risky Transactions by Purchase Size",
            color_discrete_sequence=['#22c55e'],  # Professional green
            text='Count'
        )
        fig_amounts.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font_family="Open Sans, Arial, sans-serif",
            font_size=14,
            title_font_size=18,
            title_font_color='#0f172a',
            title_font_family="Open Sans, Arial, sans-serif",
            height=400,
            showlegend=False,
            xaxis_title="Purchase Size",
            yaxis_title="Number of Risky Transactions",
            margin=dict(t=60, b=60, l=60, r=60),
            title_x=0.5
        )
        fig_amounts.update_traces(
            textposition='outside',
            marker_line_width=1.5,
            marker_line_color='#16a34a',
            hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>'
        )
        fig_amounts.update_xaxes(
            title_font_size=16,
            title_font_color='#374151',
            tickfont_size=12,
            tickfont_color='#6b7280'
        )
        fig_amounts.update_yaxes(
            title_font_size=16,
            title_font_color='#374151',
            tickfont_size=12,
            tickfont_color='#6b7280'
        )
        st.plotly_chart(fig_amounts, use_container_width=True)
        
        # Simple explanation for amounts
        st.markdown("""
        <div style="background: #F0F9FF; padding: 1.5rem; border-radius: 8px; margin: 1rem 0; border-left: 4px solid #3B82F6;">
            <p style="margin: 0; color: #374151;"><strong>💡 Why This Matters:</strong></p>
            <p style="margin: 0.5rem 0; color: #6B7280;">
                • <strong>Large purchases</strong> from new customers are often fraud<br>
                • <strong>Small purchases</strong> might be criminals testing stolen cards<br>
                • <strong>Medium purchases</strong> are usually the safest range
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Simple time pattern (when fraud happens)
        if 'hour' in risky_transactions.columns:
            st.markdown("**🕐 When Do Risky Transactions Happen?**")
            
            # Simplify hours into business-friendly periods
            risky_with_periods = risky_transactions.copy()
            
            def get_time_period(hour):
                if pd.isna(hour):
                    return 'Unknown'
                hour = int(hour)
                if 6 <= hour <= 11:
                    return 'Morning (6am-12pm)'
                elif 12 <= hour <= 17:
                    return 'Afternoon (12pm-6pm)'
                elif 18 <= hour <= 21:
                    return 'Evening (6pm-10pm)'
                else:
                    return 'Late Night (10pm-6am)'
            
            risky_with_periods['time_period'] = risky_with_periods['hour'].apply(get_time_period)
            time_counts = risky_with_periods['time_period'].value_counts()
            
            # Create simple time chart
            time_data = pd.DataFrame({
                'Time Period': time_counts.index,
                'Count': time_counts.values
            })
            
            fig_time = px.pie(
                time_data,
                values='Count',
                names='Time Period',
                title="When Do Risky Transactions Occur?",
                color_discrete_sequence=['#ef4444', '#f59e0b', '#22c55e', '#0ea5e9']  # Professional colors
            )
            fig_time.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                font_family="Open Sans, Arial, sans-serif",
                font_size=14,
                title_font_size=18,
                title_font_color='#0f172a',
                title_font_family="Open Sans, Arial, sans-serif",
                height=400,
                margin=dict(t=60, b=60, l=60, r=60),
                title_x=0.5
            )
            fig_time.update_traces(
                textinfo='label+percent',
                textfont_size=12,
                hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
            )
            st.plotly_chart(fig_time, use_container_width=True)
            
            # Simple explanation for timing
            st.markdown("""
            <div style="background: linear-gradient(135deg, var(--error-50) 0%, white 100%); padding: 2rem; border-radius: var(--radius-xl); margin: 1.5rem 0; border: 1px solid var(--error-200); box-shadow: var(--shadow-md); position: relative;">
                <div style="position: absolute; top: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg, var(--error-500), var(--error-600));"></div>
                <p style="margin: 0; color: var(--gray-900); font-weight: 600; font-size: var(--text-lg); margin-bottom: 0.75rem;">⚠️ Fraud Timing Tip:</p>
                <p style="margin: 0; color: var(--gray-700); line-height: 1.6;">Criminals often work <strong>late at night</strong> when businesses are closed and can't verify purchases. If you see many late-night transactions, that's a red flag!</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Top risk factors in plain English
        st.markdown("**🚨 Most Common Warning Signs**")
        
        # Analyze and simplify risk factors
        all_risk_factors = []
        for _, row in risky_transactions.iterrows():
            anomalies = str(row.get('anomaly_flags', ''))
            if anomalies and anomalies != 'None detected':
                factors = [factor.strip() for factor in anomalies.split(';')]
                all_risk_factors.extend(factors)
        
        # Count and simplify risk factors
        risk_factor_counts = {}
        for factor in all_risk_factors:
            if factor:
                # Simplify technical language
                simplified_factor = factor.lower()
                if 'geographical' in simplified_factor or 'zip' in simplified_factor:
                    key = '📍 Address doesn\'t match location'
                elif 'multiple transaction' in simplified_factor or 'velocity' in simplified_factor:
                    key = '⚡ Too many purchases too fast'
                elif 'large' in simplified_factor:
                    key = '💰 Unusually large purchase'
                elif 'late night' in simplified_factor or 'early morning' in simplified_factor:
                    key = '🌙 Purchase made very late/early'
                elif 'email' in simplified_factor:
                    key = '📧 Suspicious email address'
                elif 'card' in simplified_factor or 'payment' in simplified_factor:
                    key = '💳 Payment method issues'
                elif 'emulator' in simplified_factor or 'device' in simplified_factor:
                    key = '📱 Suspicious device/software'
                else:
                    key = f'⚠️ {factor[:50]}...' if len(factor) > 50 else f'⚠️ {factor}'
                
                risk_factor_counts[key] = risk_factor_counts.get(key, 0) + 1
        
        # Show top 5 risk factors
        sorted_factors = sorted(risk_factor_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        for factor, count in sorted_factors:
            percentage = (count / len(risky_transactions)) * 100
            st.markdown(f"""
            <div style="background: white; padding: 1rem; margin: 0.5rem 0; border-radius: 8px; border-left: 4px solid #EF4444; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <strong style="color: #374151;">{factor}</strong>
                    <span style="background: #EF4444; color: white; padding: 0.25rem 0.75rem; border-radius: 12px; font-size: 0.9rem; font-weight: 600;">{count} times</span>
                </div>
                <div style="background: #FEE2E2; height: 6px; border-radius: 3px; margin-top: 8px;">
                    <div style="background: #EF4444; height: 6px; border-radius: 3px; width: {min(percentage, 100)}%;"></div>
                </div>
                <div style="font-size: 0.8rem; color: #6B7280; margin-top: 4px;">{percentage:.1f}% of risky transactions</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Action-oriented summary
        st.markdown("""
        <div style="background: linear-gradient(135deg, var(--success-50) 0%, white 100%); padding: 2rem; border-radius: var(--radius-xl); margin: 2rem 0; border: 1px solid var(--success-200); box-shadow: var(--shadow-md); position: relative;">
            <div style="position: absolute; top: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg, var(--success-500), var(--success-600));"></div>
            <p style="margin: 0; color: var(--gray-900); font-weight: 600; font-size: var(--text-lg); margin-bottom: 1rem;">🎯 What You Should Do:</p>
            <p style="margin: 0; color: var(--gray-700); line-height: 1.8; font-size: var(--text-base);">
                1. <strong>Start with the red (very suspicious) transactions first</strong><br>
                2. <strong>Call customers for large purchases</strong> - real customers don't mind verification<br>
                3. <strong>Be extra careful with late-night orders</strong><br>
                4. <strong>Watch for customers making many small purchases quickly</strong><br>
                5. <strong>Trust your gut</strong> - if something feels wrong, ask questions!
            </p>
        </div>
        """, unsafe_allow_html=True)

def display_helpful_tips():
    """Display helpful tips for SMB owners"""
    
    st.markdown("## 💡 Fraud Prevention Tips")
    
    tips = [
        {
            "title": "Watch for Large Purchases from New Customers",
            "description": "If someone you've never seen before makes a big purchase, give them a quick call to verify.",
            "icon": "🛒"
        },
        {
            "title": "Be Careful with Late Night Transactions", 
            "description": "Fraudsters often work at night when businesses are closed and can't verify purchases.",
            "icon": "🌙"
        },
        {
            "title": "Check Address and ZIP Code Matches",
            "description": "If a customer's ZIP code doesn't match their state, or looks suspicious, ask for verification.",
            "icon": "📍"
        },
        {
            "title": "Watch for Suspicious IP Addresses",
            "description": "Transactions from VPNs, international IPs, or private networks with US addresses need extra verification.",
            "icon": "🌐"
        },
        {
            "title": "Multiple Small Purchases = Red Flag",
            "description": "If someone makes many small purchases quickly, they might be testing stolen card numbers.",
            "icon": "🔢"
        },
        {
            "title": "Trust Your Instincts",
            "description": "If a customer or purchase feels 'off' to you, it's okay to ask for additional verification.",
            "icon": "🤔"
        }
    ]
    
    cols = st.columns(2)
    for i, tip in enumerate(tips):
        with cols[i % 2]:
            st.markdown(f"""
            <div class="explanation-box">
                <div class="explanation-title">{tip['icon']} {tip['title']}</div>
                <div class="explanation-text">{tip['description']}</div>
            </div>
            """, unsafe_allow_html=True)

# Main app
def main():
    # Professional Enterprise Header
    st.markdown("""
    <div class="main-header">
        <h1>🛡️ FraudGuard Pro</h1>
        <p>Enterprise-Grade Fraud Detection for Growing Businesses</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Professional File Upload Section
    st.markdown("""
    <div class="upload-container">
        <h3 style="margin: 0 0 1rem 0; color: var(--gray-900); font-size: var(--text-2xl); font-weight: 600;">📊 Transaction Analysis</h3>
        <p style="margin: 0; color: var(--gray-700); font-size: var(--text-lg); line-height: 1.6;">Upload your payment data for comprehensive fraud analysis with actionable insights</p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose your transaction file (CSV)",
        type="csv",
        help="Upload a CSV file with your payment data. We'll make it easy to understand what's happening.",
        label_visibility="collapsed"
    )
    
    if uploaded_file is not None:
        try:
            # Load data
            with st.spinner("📊 Checking your payments for fraud..."):
                df = pd.read_csv(uploaded_file)
            
            # Validate data
            required_columns = ['transaction_id', 'amount', 
                              'transaction_date', 'transaction_time']
            missing_required = [col for col in required_columns if col not in df.columns]
            
            if missing_required:
                st.error(f"❌ Your file is missing these columns: {', '.join(missing_required)}")
                st.info("💡 Make sure your CSV file has columns for transaction_id, amount, transaction_date, and transaction_time")
                return
            
            # Add missing optional columns
            optional_columns = ['customer_id', 'response_code', 'merchant_name', 'merchant_category', 'state', 
                               'customer_state', 'customer_zip_code', 'customer_ip_address', 
                               'customer_city', 'customer_name', 'customer_email', 'customer_phone',
                               'payment_method', 'card_last4']
            for col in optional_columns:
                if col not in df.columns:
                    if col == 'customer_id':
                        df[col] = 'CUST_' + df.index.astype(str).str.zfill(6)
                    elif col == 'response_code':
                        df[col] = '00'
                    elif col == 'merchant_name':
                        df[col] = 'Your Business'
                    elif col in ['state', 'customer_state']:
                        df[col] = 'Unknown'
                    elif col == 'customer_zip_code':
                        df[col] = '00000'
                    elif col == 'customer_ip_address':
                        df[col] = '0.0.0.0'
                    elif col == 'customer_city':
                        df[col] = 'Unknown'
                    elif col == 'customer_name':
                        df[col] = 'Customer ' + df.index.astype(str)
                    elif col == 'customer_email':
                        df[col] = 'customer' + df.index.astype(str) + '@example.com'
                    elif col == 'customer_phone':
                        df[col] = '555-0000'
                    elif col == 'payment_method':
                        df[col] = 'card'
                    elif col == 'card_last4':
                        df[col] = '0000'
            
            st.success(f"✅ Loaded {len(df):,} payments from your business")
            
            # Run fraud detection
            with st.spinner("🔍 Looking for suspicious payments..."):
                fraud_model = SimpleFraudDetectionModel()
                df_analyzed = fraud_model.detect_fraud(df)
            
            # Display SMB-friendly results
            needs_attention, safe_payments, money_at_risk = display_smb_status(df_analyzed)
            
            # Create and display simple charts
            charts = create_smb_friendly_charts(df_analyzed)
            display_simple_charts(charts)
            
            # Display action items
            display_action_items(df_analyzed, needs_attention)
            
            # Display helpful tips
            display_helpful_tips()
            
            # Download button for detailed results
            if st.button("📥 Download Detailed Report"):
                csv = df_analyzed.to_csv(index=False)
                st.download_button(
                    label="Download Full Analysis",
                    data=csv,
                    file_name=f"fraud_check_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            
        except Exception as e:
            st.error(f"❌ Something went wrong: {str(e)}")
            st.info("💡 Please make sure your file is a properly formatted CSV with the required columns.")
    
    else:
        # Show requirements when no file is uploaded
        st.markdown("## 📋 What You Need")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="explanation-box">
                <div class="explanation-title">📄 Required Information</div>
                <div class="explanation-text">
                    Your CSV file should have these columns:<br>
                    • transaction_id (unique ID for each payment)<br>
                    • amount (payment amount)<br>
                    • transaction_date (when it happened)<br>
                    • transaction_time (what time)<br>
                    <br><strong>Optional for better fraud detection:</strong><br>
                    • merchant_category (type of business)<br>
                    • customer_state (customer's state)<br>
                    • customer_zip_code (customer's ZIP)<br>
                    • customer_ip_address (customer's IP)
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="explanation-box">
                <div class="explanation-title">🎯 What We'll Tell You</div>
                <div class="explanation-text">
                    After checking your payments, we'll show:<br>
                    • How many payments look suspicious<br>
                    • Which ones you should check<br>
                    • Simple steps to protect your business<br>
                    • Easy-to-understand charts and graphs
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Sample data preview
        st.markdown("## 📊 Example Data Format")
        
        sample_data = {
            'transaction_id': ['PAY_001', 'PAY_002', 'PAY_003'],
            'amount': [45.67, 1250.00, 23.50],
            'transaction_date': ['2024-01-15', '2024-01-15', '2024-01-16'],
            'transaction_time': ['14:30:00', '23:45:00', '08:15:00'],
            'customer_id': ['Customer_A', 'Customer_B', 'Customer_C'],
            'customer_state': ['CA', 'NY', 'TX'],
            'customer_zip_code': ['90210', '10001', '77001'],
            'customer_ip_address': ['192.168.1.1', '8.8.8.8', '1.1.1.1']
        }
        
        sample_df = pd.DataFrame(sample_data)
        st.dataframe(sample_df, use_container_width=True, hide_index=True)
        
        st.markdown("""
        <div class="explanation-box">
            <div class="explanation-title">💡 Pro Tip</div>
            <div class="explanation-text">Most payment processors (Square, PayPal, Stripe, etc.) can export your transaction data in CSV format. Look for "Export" or "Download" options in your payment dashboard. Don't worry if you don't have all the optional fields - we only need the 4 basic columns to get started!</div>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()