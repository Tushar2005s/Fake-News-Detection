import streamlit as st
import joblib
import re
import string
import os
from pathlib import Path


# Set page configuration
st.set_page_config(
    page_title="Fake News Detector",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for modern styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .main {
        padding: 0rem 0rem;
    }
    
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        min-height: 100vh;
    }
    
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .header {
        text-align: center;
        background: linear-gradient(135deg, rgba(100, 200, 255, 0.2) 0%, rgba(150, 100, 255, 0.2) 100%);
        backdrop-filter: blur(20px);
        color: #ffffff;
        padding: 3rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    }
    
    .header h1 {
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        background: linear-gradient(135deg, #64c8ff, #9664ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .header p {
        font-size: 1.1rem;
        color: rgba(255, 255, 255, 0.9);
        margin-top: 0.5rem;
    }
    
    .card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        margin-bottom: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.15);
    }
    
    .card h2 {
        color: #64c8ff;
        font-weight: 600;
        font-size: 1.5rem;
    }
    
    .card h3 {
        color: #9664ff;
        font-weight: 600;
    }
    
    .result-box {
        padding: 2rem;
        border-radius: 15px;
        font-size: 1.5rem;
        font-weight: 700;
        text-align: center;
        margin-top: 1rem;
        backdrop-filter: blur(10px);
        border: 2px solid;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        animation: slideIn 0.5s ease-out;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(-10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .fake-news {
        background: linear-gradient(135deg, rgba(198, 40, 40, 0.3) 0%, rgba(244, 67, 54, 0.2) 100%);
        color: #ff6b6b;
        border-color: #ff6b6b;
    }
    
    .real-news {
        background: linear-gradient(135deg, rgba(46, 125, 50, 0.3) 0%, rgba(76, 175, 80, 0.2) 100%);
        color: #51cf66;
        border-color: #51cf66;
    }
    
    .credit-box {
        background: linear-gradient(135deg, rgba(100, 200, 255, 0.15) 0%, rgba(150, 100, 255, 0.15) 100%);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        text-align: center;
        color: rgba(255, 255, 255, 0.95);
    }
    
    .credit-box .project-tag {
        display: inline-block;
        background: linear-gradient(135deg, #64c8ff, #9664ff);
        color: white;
        padding: 0.5rem 1.5rem;
        border-radius: 50px;
        font-size: 0.9rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    .credit-box .creator {
        font-size: 1.3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #64c8ff, #9664ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0.5rem 0;
    }
    
    .credit-box .details {
        font-size: 0.95rem;
        color: rgba(255, 255, 255, 0.85);
        line-height: 1.6;
    }
    
    textarea, input {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: #ffffff !important;
        border-color: rgba(255, 255, 255, 0.2) !important;
        border-radius: 10px !important;
    }
    
    textarea::placeholder, input::placeholder {
        color: rgba(255, 255, 255, 0.6) !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #64c8ff, #9664ff);
        color: white !important;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        font-size: 1rem;
        padding: 0.75rem 2rem;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(100, 200, 255, 0.4);
    }
    
    .stMetric {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.15);
    }
    
    .stMetric label {
        color: #64c8ff !important;
        font-weight: 600;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        color: #51cf66 !important;
        font-size: 2rem !important;
        font-weight: 700;
    }
    
    .stInfo {
        background: rgba(100, 200, 255, 0.15) !important;
        border-left: 4px solid #64c8ff !important;
        border-radius: 10px !important;
        color: rgba(255, 255, 255, 0.95) !important;
    }
    
    .stWarning {
        background: rgba(255, 193, 7, 0.15) !important;
        border-left: 4px solid #ffc107 !important;
        border-radius: 10px !important;
        color: rgba(255, 255, 255, 0.95) !important;
    }
    
    .stError {
        background: rgba(244, 67, 54, 0.15) !important;
        border-left: 4px solid #ff6b6b !important;
        border-radius: 10px !important;
        color: rgba(255, 255, 255, 0.95) !important;
    }
    
    .stExpander {
        background: rgba(255, 255, 255, 0.08);
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.15);
    }
    
    .project-section {
        background: linear-gradient(135deg, rgba(100, 200, 255, 0.1) 0%, rgba(150, 100, 255, 0.1) 100%);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 2.5rem;
        margin-top: 3rem;
        backdrop-filter: blur(20px);
    }
    
    .project-section h2 {
        color: #64c8ff;
        font-size: 2rem;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    
    .project-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 2rem;
        margin-top: 2rem;
    }
    
    @media (max-width: 900px) {
        .project-grid {
            grid-template-columns: 1fr;
        }
    }
    
    .project-item {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 1.5rem;
    }
    
    .project-item h3 {
        color: #9664ff;
        margin-top: 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .project-item p, .project-item li {
        color: rgba(255, 255, 255, 0.85);
        line-height: 1.7;
        margin: 0.5rem 0;
    }
    
    .project-item ul {
        margin-left: 1.5rem;
    }
    
    .features-list {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin-top: 1rem;
    }
    
    .feature-badge {
        background: rgba(81, 207, 102, 0.2);
        border-left: 3px solid #51cf66;
        padding: 1rem;
        border-radius: 8px;
        color: rgba(255, 255, 255, 0.9);
        font-weight: 500;
    }
    
    """, unsafe_allow_html=True)


def clean_text(text):
    """Clean and preprocess text using the same method as training"""
    text = text.lower()
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(f"[{string.punctuation}]", "", text)
    text = re.sub(r'\w*\d\w*', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


@st.cache_resource
def load_models():
    """Load the pre-trained model and vectorizer"""
    try:
        # Try multiple paths to find the model files
        possible_paths = [
            Path("fake_news_model.pkl"),
            Path(__file__).parent / "fake_news_model.pkl",
            Path.cwd() / "fake_news_model.pkl",
        ]
        
        model_path = None
        vectorizer_path = None
        
        # Find model file
        for path in possible_paths:
            if path.exists():
                model_path = path
                break
        
        # Find vectorizer file
        possible_vectorizer_paths = [
            Path("vectorizer.pkl"),
            Path(__file__).parent / "vectorizer.pkl" if model_path else Path("vectorizer.pkl"),
            Path.cwd() / "vectorizer.pkl",
        ]
        
        for path in possible_vectorizer_paths:
            if path.exists():
                vectorizer_path = path
                break
        
        if model_path is None or vectorizer_path is None:
            st.error("❌ Model files not found!")
            st.error(f"Looking for files in:")
            st.error(f"  - {Path.cwd() / 'fake_news_model.pkl'}")
            st.error(f"  - {Path.cwd() / 'vectorizer.pkl'}")
            st.stop()
        
        model = joblib.load(str(model_path))
        vectorizer = joblib.load(str(vectorizer_path))
        return model, vectorizer
    except Exception as e:
        st.error(f"❌ Error loading models: {str(e)}")
        import traceback
        st.error(traceback.format_exc())
        st.stop()


def predict_news(text, model, vectorizer):
    """Predict if the news is fake or real"""
    try:
        # Clean the text
        cleaned_text = clean_text(text)
        
        # Vectorize the text
        text_vectorized = vectorizer.transform([cleaned_text])
        
        # Make prediction
        prediction = model.predict(text_vectorized)[0]
        probabilities = model.predict_proba(text_vectorized)[0]
        
        return prediction, probabilities
    except Exception as e:
        st.error(f"❌ Error during prediction: {str(e)}")
        return None, None


# Load models
model, vectorizer = load_models()

# Header
st.markdown("""
    <div class="header">
        <h1>📰 Fake News Detector</h1>
        <p>Advanced AI-Powered Detection System</p>
    </div>
    """, unsafe_allow_html=True)

# Project Credit
st.markdown("""
    <div class="credit-box">
        <div class="project-tag">✨ PROJECT</div>
        <div class="creator">✨ Created by Tushar Sharma ✨</div>
        <div class="details">
            BSc (Data Science and Artificial Intelligence)<br>
            IIT Guwahati
        </div>
    </div>
    """, unsafe_allow_html=True)

# Main content
st.markdown('<div class="card">', unsafe_allow_html=True)

st.markdown('### 📝 Enter News Article for Analysis', unsafe_allow_html=True)

# Create tabs for better organization
tab1, tab2 = st.tabs(["🚀 Analyze", "ℹ️ How It Works"])

with tab1:
    # Text input options
    col_input, col_method = st.columns([4, 1])
    
    with col_method:
        input_method = st.selectbox("Input Method:", ["Paste Text", "Type Text"], label_visibility="collapsed")
    
    if input_method == "Paste Text":
        news_text = st.text_area(
            "Paste your news article here:",
            height=250,
            placeholder="📋 Paste the complete news article here and click 'ANALYZE NEWS' to detect if it's fake or real...",
            label_visibility="collapsed",
            key="paste_input"
        )
    else:
        news_text = st.text_area(
            "Type your news article here:",
            height=250,
            placeholder="✍️ Type the news article here and click 'ANALYZE NEWS' to detect if it's fake or real...",
            label_visibility="collapsed",
            key="type_input"
        )
    
    # Text stats while typing
    if news_text:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.caption(f"📝 Words: {len(news_text.split())}")
        with col2:
            st.caption(f"🔤 Characters: {len(news_text)}")
        with col3:
            st.caption(f"✂️ Readability: {'Good ✅' if len(news_text.split()) > 50 else 'Add more text ⬆️'}")

with tab2:
    st.markdown("#### 🤖 How Our Detection System Works")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Algorithm Used:**")
        st.write("""
        - **Model:** Multinomial Naive Bayes
        - **Feature Extraction:** TF-IDF Vectorizer
        - **Training Data:** 30,000+ news articles
        - **Accuracy:** High confidence predictions
        """)
    
    with col2:
        st.markdown("**What We Analyze:**")
        st.write("""
        - Linguistic patterns
        - Semantic relationships
        - Keyword frequency
        - Text structure
        """)
    
    st.markdown("**Tips for Best Results:**")
    st.write("""
    ✓ Use complete, full articles (not headlines)  
    ✓ Longer articles = more accurate predictions  
    ✓ System auto-cleans formatting issues  
    ✓ Confidence scores show prediction reliability  
    """)

st.markdown('</div>', unsafe_allow_html=True)

# Analyze button and results
st.markdown('<div class="card">', unsafe_allow_html=True)

col_btn = st.columns([1, 2, 1])
with col_btn[1]:
    analyze_btn = st.button("🚀 ANALYZE NEWS", use_container_width=True, type="primary")

if analyze_btn:
    if not news_text.strip():
        st.warning("⚠️ Please enter some text to analyze!")
    else:
        with st.spinner("🔄 Analyzing your news article..."):
            prediction, probabilities = predict_news(news_text, model, vectorizer)
        
        if prediction is not None:
            # Get class labels and their probabilities
            classes = model.classes_
            prob_dict = {cls: prob for cls, prob in zip(classes, probabilities)}
            
            # Determine prediction result
            is_fake = prediction.lower() == 'fake'
            
            # Display results with animation
            if is_fake:
                st.markdown(
                    f"""
                    <div class="result-box fake-news">
                        🚨 LIKELY FAKE NEWS 🚨
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"""
                    <div class="result-box real-news">
                        ✅ LIKELY REAL NEWS ✅
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            st.divider()
            
            # Confidence scores
            st.markdown('### 📊 Confidence Analysis', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric(
                    label="🔴 Fake News Probability",
                    value=f"{prob_dict.get('FAKE', prob_dict.get('fake', 0))*100:.2f}%"
                )
            
            with col2:
                st.metric(
                    label="🟢 Real News Probability",
                    value=f"{prob_dict.get('REAL', prob_dict.get('real', 0))*100:.2f}%"
                )
            
            # Confidence visualization
            st.markdown('### 📈 Prediction Confidence Distribution', unsafe_allow_html=True)
            
            chart_data = {
                "FAKE": [prob_dict.get('FAKE', prob_dict.get('fake', 0))*100],
                "REAL": [prob_dict.get('REAL', prob_dict.get('real', 0))*100]
            }
            
            st.bar_chart(chart_data, height=300)
            
            st.divider()
            
            # Additional analysis
            with st.expander("📈 Detailed Analysis & Statistics"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("📝 Word Count", len(news_text.split()))
                
                with col2:
                    st.metric("🔤 Character Count", len(news_text))
                
                with col3:
                    cleaned = clean_text(news_text)
                    st.metric("✂️ Cleaned Words", len(cleaned.split()))
                
                st.divider()
                
                st.write("**🎯 Prediction Details:**")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write(f"**Predicted Class:** {prediction.upper()}")
                
                with col2:
                    st.write(f"**Confidence Level:** {max(probabilities)*100:.2f}%")
                
                with col3:
                    confidence_level = "High ✅" if max(probabilities) > 0.75 else "Medium ⚠️" if max(probabilities) > 0.6 else "Low ❌"
                    st.write(f"**Reliability:** {confidence_level}")
                
                st.divider()
                
                st.write("**🧠 Model Information:**")
                st.write(f"- **Algorithm:** Multinomial Naive Bayes")
                st.write(f"- **Feature Extraction:** TF-IDF Vectorizer")
                st.write(f"- **Training Data:** Balanced fake & real news articles")
                st.write(f"- **Text Preprocessing:** Lowercase, punctuation removal, normalization")

st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# PROJECT INFORMATION SECTION
# ============================================

st.markdown("""
    <div class="project-section">
        <h2>✨ Project Information</h2>
    </div>
    """, unsafe_allow_html=True)

# Creator and Institution
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("""
    <div class="project-item">
        <h3>👨‍💼 Creator</h3>
        <p><strong>Tushar Sharma</strong></p>
        <p>BSc (Data Science and Artificial Intelligence)</p>
        <p><em>IIT Guwahati</em></p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="project-item">
        <h3>📚 Education</h3>
        <p><strong>Indian Institute of Technology</strong></p>
        <p>Guwahati, Assam, India</p>
        <p>Department of Data Science</p>
    </div>
    """, unsafe_allow_html=True)

# Project Features and Technologies
st.markdown("<h3 style='color: #64c8ff; margin-top: 2rem;'>🚀 Key Features</h3>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

features = [
    ("⚡ Real-time Detection", "Instant predictions with confidence scores"),
    ("🔐 Secure & Private", "No data storage or external submissions"),
    ("📊 Detailed Analytics", "Comprehensive text analysis and statistics"),
    ("🤖 ML Powered", "Advanced machine learning algorithms"),
    ("💻 User Friendly", "Intuitive interface for easy usage"),
    ("🎯 High Accuracy", "Trained on 30,000+ verified news articles")
]

for idx, (title, desc) in enumerate(features):
    with [col1, col2, col3][idx % 3]:
        st.markdown(f"""
        <div class="project-item">
            <h4 style='color: #51cf66; margin: 0;'>{title}</h4>
            <p style='margin: 0.5rem 0 0 0; font-size: 0.9rem;'>{desc}</p>
        </div>
        """, unsafe_allow_html=True)

# Technical Details
st.markdown("<h3 style='color: #64c8ff; margin-top: 2rem;'>🔧 Technical Stack</h3>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="project-item">
        <h3>🏗️ Architecture</h3>
        <ul>
            <li><strong>Backend:</strong> Python 3.14+</li>
            <li><strong>Frontend:</strong> Streamlit</li>
            <li><strong>ML Framework:</strong> Scikit-learn</li>
            <li><strong>Data Processing:</strong> Pandas & NumPy</li>
            <li><strong>Model Serialization:</strong> Joblib</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="project-item">
        <h3>📐 Model Details</h3>
        <ul>
            <li><strong>Algorithm:</strong> Multinomial Naive Bayes</li>
            <li><strong>Vectorizer:</strong> TF-IDF</li>
            <li><strong>Training Samples:</strong> ~30,000 articles</li>
            <li><strong>Test Accuracy:</strong> High confidence</li>
            <li><strong>Features:</strong> Text preprocessing & cleaning</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Project Statistics
st.markdown("<h3 style='color: #64c8ff; margin-top: 2rem;'>📊 Project Statistics</h3>", unsafe_allow_html=True)

stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)

with stat_col1:
    st.metric("Dataset Size", "30,000+", "News Articles")

with stat_col2:
    st.metric("Model Type", "Naive Bayes", "Classification")

with stat_col3:
    st.metric("Feature Method", "TF-IDF", "Vectorization")

with stat_col4:
    st.metric("Response Time", "<1s", "Average")

# Use Cases and Applications
st.markdown("<h3 style='color: #64c8ff; margin-top: 2rem;'>🎯 Use Cases</h3>", unsafe_allow_html=True)

use_cases = [
    "📰 News Verification",
    "🔍 Content Analysis",
    "📱 Social Media Monitoring",
    "🏢 Organizational Security",
    "🎓 Educational Research",
    "📊 Data Journalism",
    "⚖️ Misinformation Detection",
    "🌐 Web Content Filtering"
]

use_case_cols = st.columns(4)
for idx, use_case in enumerate(use_cases):
    with use_case_cols[idx % 4]:
        st.markdown(f"""
        <div class="feature-badge">
            {use_case}
        </div>
        """, unsafe_allow_html=True)

# How to Use Guide
st.markdown("<h3 style='color: #64c8ff; margin-top: 2rem;'>📖 How to Use</h3>", unsafe_allow_html=True)

steps = [
    ("1️⃣", "Enter Text", "Paste or type a news article in the input area"),
    ("2️⃣", "Click Analyze", "Press the 'ANALYZE NEWS' button"),
    ("3️⃣", "View Results", "Get instant fake/real prediction with confidence"),
    ("4️⃣", "Review Details", "Check detailed analysis and statistics")
]

for step_num, step_title, step_desc in steps:
    st.markdown(f"""
    <div style='display: flex; align-items: flex-start; gap: 1.5rem; margin-bottom: 1rem;'>
        <div style='font-size: 2rem; min-width: 50px;'>{step_num}</div>
        <div>
            <h4 style='margin: 0; color: #64c8ff;'>{step_title}</h4>
            <p style='margin: 0.5rem 0 0 0; color: rgba(255,255,255,0.8);'>{step_desc}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Research and References
st.markdown("<h3 style='color: #64c8ff; margin-top: 2rem;'>📚 Research Background</h3>", unsafe_allow_html=True)

st.markdown("""
<div class="project-item">
    <p><strong>This project is based on advanced NLP and Machine Learning techniques:</strong></p>
    <ul>
        <li>Text Classification using Naive Bayes algorithms</li>
        <li>Feature extraction using TF-IDF (Term Frequency-Inverse Document Frequency)</li>
        <li>Rigorous text preprocessing and cleaning pipelines</li>
        <li>Trained on authentic fake/real news datasets</li>
        <li>Validated with comprehensive metrics and cross-validation</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: rgba(255, 255, 255, 0.8); padding: 2rem 1rem; margin-top: 2rem;">
        <div style="margin-bottom: 1.5rem;">
            <p style="font-size: 1rem; font-weight: 600; margin: 0;">
                🌟 Built with passion by <span style="color: #64c8ff;">Tushar Sharma</span> 🌟
            </p>
        </div>
        <p style="font-size: 0.95rem; margin: 0.5rem 0;">
            🚀 Built with <span style="color: #64c8ff; font-weight: 600;">Streamlit</span> | 
            Powered by <span style="color: #9664ff; font-weight: 600;">Machine Learning</span>
        </p>
        <p style="font-size: 0.9rem; color: rgba(255, 255, 255, 0.7); margin: 0.5rem 0;">
            © 2026 Fake News Detection System | IIT Guwahati
        </p>
        <p style="font-size: 0.85rem; color: rgba(255, 255, 255, 0.6); margin: 1rem 0 0 0;">
            Advanced AI-powered fake news detection using Natural Language Processing & Machine Learning
        </p>
    </div>
    """, unsafe_allow_html=True)
