import streamlit as st


# Load background image
background_image_path = "Images/JWT_star_formation.jpg"
import base64

def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


img = get_img_as_base64(background_image_path)

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] {{
background-image: url("data:image/png;base64,{img}");
background-size: cover;
background-position: top left;
background-repeat: no-repeat;
background-attachment: local;
}}
[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}

</style>
"""

on_boarding_style = """
        <style>
            /* Completely hide structural UI components to lock user focus */
            [data-testid="stSidebar"] { display: none !important; }
            [data-testid="stHeader"] { display: none !important; }
            
            /* 1. BUTTON CONTAINER: Applies the neon gradient background, padding, and outer shadows */
            div.stButton > button {
                background: linear-gradient(45deg, #8A2387, #E94057, #F27121) !important;
                border: none !important;
                padding: 1.2rem 3rem !important; 
                border-radius: 12px !important;
                box-shadow: 0 6px 20px rgba(233, 64, 87, 0.5) !important;
                transition: transform 0.2s ease, box-shadow 0.2s ease !important;
                cursor: pointer !important;
            }
            
            /* 2. BUTTON TEXT: Forces giant font scaling in solid white, preventing overlapping gradient artifacts */
            div.stButton > button p, 
            div.stButton > button span {
                color: #FFFFFF !important;
                font-size: 32px !important; /* Clean, high-visibility maximized font size */
                font-weight: bold !important;
                background: none !important; /* Clears duplicate background repetitions on child tokens */
                -webkit-background-clip: unset !important;
                -webkit-text-fill-color: initial !important;
            }

            /* 3. HOVER ACTIONS: Smooth micro-interaction feedback when moving the cursor over the element */
            div.stButton > button:hover {
                transform: scale(1.03) !important;
                box-shadow: 0 8px 25px rgba(233, 64, 87, 0.7) !important;
            }

        </style>
    """

# --- BALANCED COLOR CONFIGURATION (CSS) ---
custom_styles = """
    <style>
        /* 1. MAIN APPLICATION TITLE: Cosmic Neon Gradient */
        .main-title {
            font-family: 'Helvetica Neue', sans-serif;
            font-size: 42px;
            font-weight: bold;
            background: linear-gradient(45deg, #8A2387, #E94057, #F27121);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 20px;
        }
        
        /* 2. ABOUT TEXT: Bright white for clean readability over the dark background */
        .about-text {
            color: #FFFFFF !important;
            font-family: 'Helvetica Neue', sans-serif;
            font-size: 16px;
        }

        /* 3. SIDEBAR HEADERS: White headers to stand out and create hierarchy */
        .stSidebar h2, .stSidebar h3, .stSidebar p {
            color: #FFFFFF !important;
            font-weight: bold;
        }

        /* 4. SIDEBAR CONTROLS: Soft light gray for labels, checkboxes, and sliders */
        .stSidebar label, .stSidebar .stCheckbox, .stSidebar .stSlider {
            color: #E0E0E0 !important; 
        }
        
        /* 5. GOLD AS AN ACCENT COLOR: Used only for dividers and copyright links */
        .stSidebar hr {
            border-color: #FFB03B !important;
        }
        .small-text a {
            color: #FFB03B !important;
            text-decoration: none;
        }
    </style>
"""

side_bar_styles = """
    <style>
        [data-testid="stSidebar"] {
            background-color: #0b0d19 !important; /* Azul espacio profundo */
            border-right: 5px solid #1e2235;      /* Línea sutil de división */
             }
    </style>
"""

header_styles = """
    <style>

        /* 7. RADICAL SPACE REDUCTION FOR MODERN STREAMLIT VERSIONS */
        /* Makes the header float over the content instead of pushing it down */
        [data-testid="stHeader"] {
            position: absolute !important;
            background-color: transparent !important;
            background: transparent !important;
        }

        /* Removes all top padding and margins from the main content wrappers */
        [data-testid="stMain"], 
        [data-testid="stMainBlockContainer"], 
        [data-testid="stAppViewBlockContainer"] {
            padding-top: 0rem !important;
            margin-top: 0rem !important;
            top: 0 !important;
        }

        /* Adjusts the block width to keep your full-size layout */
        [data-testid="stAppViewBlockContainer"] {
            max-width: 95% !important;
            padding-bottom: 1rem !important;
        }

    </style>
"""

def inject_on_boarding_styles():
    st.markdown(on_boarding_style, unsafe_allow_html=True)

def inject_custom_styles():
    st.markdown(custom_styles, unsafe_allow_html=True)

def inject_background_image():
    st.markdown(page_bg_img, unsafe_allow_html=True)

def inject_side_bar_styles():
    st.markdown(side_bar_styles, unsafe_allow_html=True)

def inject_header_styles():
    st.markdown(header_styles, unsafe_allow_html=True)