def get_custom_css():
    return """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
        
        html, body, [class*="css"]  {
            font-family: 'Inter', sans-serif;
        }
        
        :root {
            --bg-color: #0f1116;
            --card-bg: #161b22;
            --accent: #238636;
            --text-primary: #e6edf3;
            --text-secondary: #8b949e;
            --border-color: #30363d;
        }

        [data-testid="stAppViewContainer"] {
            background-color: var(--bg-color);
        }
        [data-testid="stHeader"] {
            background-color: rgba(15, 17, 22, 0.8);
            backpack-filter: blur(10px);
        }

        [data-testid="stSidebar"] {
            background-color: var(--card-bg);
            border-right: 1px solid var(--border-color);
        }

        h1 {
            font-weight: 700;
            color: var(--text-primary) !important;
            letter-spacing: -0.5px;
        }
        h2, h3 {
            font-weight: 600;
            color: var(--text-primary) !important;
        }
        p, label {
            color: var(--text-secondary) !important;
        }

        [data-testid="stMetric"] {
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s ease;
            min-height: 140px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        [data-testid="stMetric"]:hover {
            transform: translateY(-2px);
            border-color: var(--text-secondary);
        }
        [data-testid="stMetricValue"] {
            font-size: 2rem !important;
            font-weight: 700 !important;
            color: #58a6ff !important;
        }
        
        div[data-baseweb="select"] > div {
            cursor: pointer !important;
        }

        .stButton>button {
            background-color: var(--accent) !important;
            color: #ffffff !important;
            border: none;
            border-radius: 6px;
            padding: 0.6rem 1rem;
            font-weight: 700 !important;
            font-size: 1rem !important;
            box-shadow: 0 1px 0 rgba(27, 31, 35, 0.1);
            transition: all 0.2s ease;
            opacity: 1 !important;
        }
        .stButton>button p {
            color: #ffffff !important;
        }
        .stButton>button:hover {
            background-color: #2ea043 !important;
            box-shadow: 0 6px 12px rgba(0,0,0,0.3);
            transform: scale(1.02);
            color: #ffffff !important;
        }
        
        .stTextInput>div>div>input, .stSelectbox>div>div>div {
            background-color: #0d1117;
            color: var(--text-primary);
            border: 1px solid var(--border-color);
            border-radius: 6px;
        }
        
        .stTabs [data-baseweb="tab-list"] {
            gap: 20px;
            border-bottom: 1px solid var(--border-color);
            margin-bottom: 20px;
        }
        .stTabs [data-baseweb="tab"] {
            background-color: transparent;
            border-radius: 4px;
            color: var(--text-secondary);
            font-weight: 500;
            padding: 10px 20px;
            transition: color 0.2s;
        }
        .stTabs [data-baseweb="tab"]:hover {
            color: var(--text-primary);
            background-color: rgba(255,255,255,0.05);
        }
        .stTabs [aria-selected="true"] {
            background-color: transparent;
            color: var(--text-primary) !important;
            border-bottom: 3px solid #fd8c73 !important;
        }
        
        [data-testid="stMarkdownContainer"] h1 a, 
        [data-testid="stMarkdownContainer"] h2 a, 
        [data-testid="stMarkdownContainer"] h3 a {
            display: none !important;
        }
        
        .stButton > button {
            color: #ffffff !important;
        }
        .stButton > button * {
            color: #ffffff !important;
            opacity: 1 !important;
        }
    </style>
    """
