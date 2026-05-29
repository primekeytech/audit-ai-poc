# ============================================
# AUDIT POC - Main Streamlit Application
# ============================================
# This is the main entry point for the app.
# Run with: streamlit run app.py
# ============================================

import streamlit as st
import os
import yaml
from pathlib import Path

# --------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------
# Must be the first Streamlit command
st.set_page_config(
    page_title="Audit AI — POC",
    page_icon="🔑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------
# LOAD CONFIGURATION
# --------------------------------------------
# Read settings from config.yaml
def load_config():
    """Load configuration from config.yaml file"""
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

config = load_config()

# --------------------------------------------
# CUSTOM STYLING
# --------------------------------------------
# Apply premium dark theme matching Genesis GV70 aesthetic
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=DM+Sans:wght@400;500;600;700&display=swap');

/* ── GLOBAL ── */
html, body, .stApp {
    background-color: #0D1117 !important;
    font-family: 'Inter', sans-serif !important;
    color: #C9D1D9 !important;
}

/* Kill the white block Streamlit injects */
.block-container {
    background-color: #0D1117 !important;
    padding: 2rem 2.5rem !important;
    max-width: 1100px !important;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background-color: #0D1117 !important;
    border-right: 1px solid #21262D !important;
}
[data-testid="stSidebar"] * {
    color: #8B949E !important;
    font-family: 'Inter', sans-serif !important;
}
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #E6EDF3 !important;
    font-size: 0.7rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
}

/* ── RADIO NAV ITEMS ── */
[data-testid="stSidebar"] label {
    color: #8B949E !important;
    font-size: 0.875rem !important;
    padding: 6px 12px !important;
    border-radius: 6px !important;
    transition: all 0.15s ease !important;
}
[data-testid="stSidebar"] label:hover {
    color: #E6EDF3 !important;
    background: #161B22 !important;
}
[data-testid="stSidebar"] [aria-checked="true"] + div label,
[data-testid="stSidebar"] input[type="radio"]:checked ~ label {
    color: #58A6FF !important;
    background: rgba(88,166,255,0.1) !important;
}

/* ── HEADINGS ── */
h1 {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 2rem !important;
    font-weight: 700 !important;
    color: #E6EDF3 !important;
    letter-spacing: -0.02em !important;
}
h2, h3 {
    font-family: 'DM Sans', sans-serif !important;
    color: #E6EDF3 !important;
    font-weight: 600 !important;
}

/* ── METRIC CARDS ── */
[data-testid="stMetric"] {
    background: #161B22 !important;
    border: 1px solid #21262D !important;
    border-radius: 12px !important;
    padding: 1.2rem 1.5rem !important;
}
[data-testid="stMetricLabel"] {
    font-size: 0.7rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    color: #8B949E !important;
}
[data-testid="stMetricValue"] {
    font-size: 2rem !important;
    font-weight: 700 !important;
    color: #E6EDF3 !important;
    font-family: 'DM Sans', sans-serif !important;
}
[data-testid="stMetricDelta"] {
    font-size: 0.75rem !important;
    color: #F85149 !important;
}

/* ── BUTTONS ── */
.stButton > button {
    background: #238636 !important;
    color: #ffffff !important;
    border: 1px solid #2EA043 !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.875rem !important;
    padding: 0.5rem 1.25rem !important;
    transition: all 0.15s ease !important;
}
.stButton > button:hover {
    background: #2EA043 !important;
    border-color: #3FB950 !important;
}

/* Run Analysis big button */
.stButton > button[kind="primary"] {
    background: #1F6FEB !important;
    border-color: #388BFD !important;
    font-size: 1rem !important;
    padding: 0.75rem 1.5rem !important;
}

/* ── DIVIDERS ── */
hr {
    border-color: #21262D !important;
    margin: 1.5rem 0 !important;
}

/* ── FILE UPLOADER ── */
[data-testid="stFileUploader"] {
    background: #161B22 !important;
    border: 1px dashed #30363D !important;
    border-radius: 12px !important;
    padding: 1rem !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: #58A6FF !important;
}
[data-testid="stFileUploadDropzone"] {
    background: #161B22 !important;
    border: 1px dashed #30363D !important;
    border-radius: 8px !important;
}
[data-testid="stFileUploadDropzone"] button {
    background: #21262D !important;
    color: #C9D1D9 !important;
    border: 1px solid #30363D !important;
    border-radius: 6px !important;
}
[data-testid="stFileUploadDropzone"] span {
    color: #8B949E !important;
}

/* ── SUCCESS / WARNING / INFO BOXES ── */
[data-testid="stAlert"] {
    border-radius: 8px !important;
    border-width: 1px !important;
    font-size: 0.875rem !important;
}

/* ── EXPANDER (findings) ── */
[data-testid="stExpander"] {
    background: #161B22 !important;
    border: 1px solid #21262D !important;
    border-radius: 10px !important;
    margin-bottom: 0.5rem !important;
}
[data-testid="stExpander"]:hover {
    border-color: #F85149 !important;
}

/* ── TEXT INPUTS ── */
[data-testid="stTextInput"] input,
[data-testid="stDateInput"] input {
    background: #161B22 !important;
    border: 1px solid #30363D !important;
    border-radius: 8px !important;
    color: #C9D1D9 !important;
    font-family: 'Inter', sans-serif !important;
}

/* ── CODE / BADGE TAGS ── */
code {
    background: #161B22 !important;
    color: #79C0FF !important;
    border: 1px solid #30363D !important;
    border-radius: 4px !important;
    padding: 2px 6px !important;
    font-size: 0.8rem !important;
}

/* ── PROGRESS BAR ── */
[data-testid="stProgress"] > div > div {
    background: #1F6FEB !important;
    border-radius: 4px !important;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0D1117; }
::-webkit-scrollbar-thumb { background: #30363D; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #58A6FF; }

/* Hide Streamlit top toolbar and header */
[data-testid="stToolbar"],
[data-testid="stToolbarActions"],
header[data-testid="stHeader"],
[data-testid="stAppDeployButton"],
.stDeployButton,
#MainMenu,
[data-testid="stMainMenu"],
[data-testid="stMainMenuButton"],
[data-testid="stHeaderActionElements"],
button[data-testid="stBaseButton-header"] {
    display: none !important;
}

footer {
    display: none !important;
}

/* Hide sidebar collapse/expand button (Streamlit 1.38+) */
[data-testid="collapsedControl"],
[data-testid="stSidebarCollapseButton"],
[data-testid="stBaseButton-headerNoPadding"] {
    display: none !important;
}

/* Fix top padding since header is gone */
.block-container {
    padding-top: 1.5rem !important;
}

/* ── SIDEBAR FOOTER / LOGO ── */
.sidebar-footer {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.25rem 0;
}
.sidebar-built-by {
    font-size: 0.85rem;
    color: #8B949E !important;
    font-style: italic;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------
with st.sidebar:
    # Logo and title
    st.markdown("## 🔑 Audit AI")
    st.markdown("*Phase 1 POC*")
    st.divider()
    
    # Navigation menu
    st.markdown("### Navigation")
    page = st.radio(
        "Go to",
        ["🏠 Dashboard", "📁 Upload Documents", "⚙️ Run Analysis", "📊 Review Results", "📄 Generate Report"],
        label_visibility="collapsed"
    )
    
    st.divider()
    
    # Show current AI provider
    st.markdown("### Settings")
    st.markdown(f"**AI Provider:** `{config['ai']['provider']}`")
    st.markdown(f"**Model:** `{config['ai']['model']}`")

    # AI Status indicator
    import subprocess
    try:
        result = subprocess.run(
            ["curl", "-s", "http://localhost:11434/api/tags"],
            capture_output=True, timeout=2
        )
        if result.returncode == 0:
            st.markdown("🟢 **AI Online** — llama3 ready")
        else:
            st.markdown("🔴 **AI Offline** — start Ollama")
    except:
        st.markdown("🔴 **AI Offline** — start Ollama")

    st.markdown("**Built by Prime Key Tech**")

# --------------------------------------------
# PAGE: DASHBOARD
# --------------------------------------------
if page == "🏠 Dashboard":
    # Main header
    st.title("🔑 Bank Audit Automation")
    st.markdown("#### AI-powered audit workflow — Phase 1 POC")
    st.divider()
    
    # How it works - step by step
    st.markdown("### How it works")
    
    # 4 step columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("**Step 1**")
        st.markdown("📁 Upload bank documents and questionnaire responses")
    
    with col2:
        st.markdown("**Step 2**")
        st.markdown("🤖 AI reads and extracts relevant information")
    
    with col3:
        st.markdown("**Step 3**")
        st.markdown("📊 Work program auto-populated (columns F, G, H)")
    
    with col4:
        st.markdown("**Step 4**")
        st.markdown("📄 Branded PDF report generated automatically")
    
    st.divider()
    
    # Quick stats
    st.markdown("### Session Summary")
    
    metric1, metric2, metric3, metric4 = st.columns(4)
    
    # Check session state for stats
    # Session state stores data between page changes
    docs_uploaded = len(st.session_state.get("uploaded_docs", []))
    controls_reviewed = st.session_state.get("controls_reviewed", 0)
    findings_count = st.session_state.get("findings_count", 0)
    
    with metric1:
        st.metric("Documents uploaded", docs_uploaded)
    with metric2:
        st.metric("Controls reviewed", controls_reviewed)
    with metric3:
        st.metric("Findings found", findings_count)
    with metric4:
        st.metric("Status", "Ready" if docs_uploaded == 0 else "In Progress")

# --------------------------------------------
# PAGE: UPLOAD DOCUMENTS
# --------------------------------------------
elif page == "📁 Upload Documents":
    st.title("📁 Upload Documents")
    st.markdown("Upload all bank documents and questionnaire responses here.")
    st.divider()
    
    # Two columns - bank docs and questionnaire
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Bank Documents")
        st.markdown("Upload policies, procedures, evidence files, network diagrams etc.")
        
        # File uploader - accepts PDF, DOCX, XLSX
        bank_docs = st.file_uploader(
            "Drop files here",
            type=["pdf", "docx", "xlsx"],          # Accepted file types
            accept_multiple_files=True,              # Allow multiple files
            key="bank_docs_uploader",
            help="Accepted formats: PDF, Word documents, Excel files"
        )
        
        # Show uploaded files
        if bank_docs:
            st.success(f"✅ {len(bank_docs)} file(s) uploaded")
            for doc in bank_docs:
                st.markdown(f"📄 `{doc.name}` ({round(doc.size/1024, 1)} KB)")
            
            # Save to session state so other pages can access
            st.session_state["uploaded_docs"] = bank_docs
    
    with col2:
        st.markdown("### Questionnaire / Technical Worksheet")
        st.markdown("Upload the completed technical information worksheet from the bank.")
        
        # Single file uploader for questionnaire
        questionnaire = st.file_uploader(
            "Drop questionnaire here",
            type=["pdf", "docx", "xlsx"],
            accept_multiple_files=False,             # Single file only
            key="questionnaire_uploader",
            help="The technical information worksheet filled by the bank"
        )
        
        # Show uploaded questionnaire
        if questionnaire:
            st.success(f"✅ Questionnaire uploaded: `{questionnaire.name}`")
            
            # Save to session state
            st.session_state["questionnaire"] = questionnaire
    
    st.divider()
    
    # Next step button
    if bank_docs and questionnaire:
        st.success("✅ All files uploaded! Use the sidebar to go to Run Analysis.")
    else:
        st.info("ℹ️ Please upload both bank documents AND questionnaire to proceed.")

# --------------------------------------------
# PAGE: RUN ANALYSIS
# --------------------------------------------
elif page == "⚙️ Run Analysis":
    st.title("⚙️ Run Analysis")
    st.markdown("AI will read all uploaded documents and populate the work program.")
    st.divider()
    
    # Check if files were uploaded
    uploaded_docs = st.session_state.get("uploaded_docs", [])
    questionnaire = st.session_state.get("questionnaire", None)
    
    if not uploaded_docs or not questionnaire:
        # No files uploaded yet - show warning
        st.warning("⚠️ No files uploaded yet. Please go to **Upload Documents** first.")
    else:
        # Files are ready - show run button
        st.success(f"✅ {len(uploaded_docs)} document(s) and questionnaire ready for analysis")
        
        st.markdown("### Ready to analyse")
        st.markdown(f"- **AI Provider:** `{config['ai']['provider']}`")
        st.markdown(f"- **Model:** `{config['ai']['model']}`")
        st.markdown(f"- **Documents:** {len(uploaded_docs)} files")
        
        st.divider()
        
        # Big run button
        if st.button("🚀 Run AI Analysis", use_container_width=True):
            
            # Progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Step 1 - Extract text from documents
            status_text.markdown("**Step 1/4** — Extracting text from documents...")
            progress_bar.progress(25)
            
            from core.extractor import DocumentExtractor
            extractor = DocumentExtractor()
            
            import time
            time.sleep(1)  # Simulating processing time
            
            # Step 2 - Send to AI
            status_text.markdown("**Step 2/4** — AI reading documents...")
            progress_bar.progress(50)
            time.sleep(1)
            
            # Step 3 - Populate workbook
            status_text.markdown("**Step 3/4** — Populating work program...")
            progress_bar.progress(75)
            time.sleep(1)
            
            # Step 4 - Done
            status_text.markdown("**Step 4/4** — Analysis complete!")
            progress_bar.progress(100)
            
            # Save mock results to session state for now
            # These will be replaced with real AI results
            st.session_state["controls_reviewed"] = 24
            st.session_state["findings_count"] = 6
            st.session_state["analysis_done"] = True
            
            st.success("✅ Analysis complete! Go to **Review Results** to see findings.")

# --------------------------------------------
# PAGE: REVIEW RESULTS
# --------------------------------------------
elif page == "📊 Review Results":
    st.title("📊 Review Results")
    st.markdown("Review AI-populated work program results and findings.")
    st.divider()
    
    # Check if analysis was run
    if not st.session_state.get("analysis_done", False):
        st.warning("⚠️ Please run analysis first.")
    else:
        # Summary metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total controls", st.session_state.get("controls_reviewed", 0))
        with col2:
            st.metric("Findings (Score 4)", st.session_state.get("findings_count", 0), delta="Needs attention")
        with col3:
            st.metric("Passed (Score 1-2)", 
                     st.session_state.get("controls_reviewed", 0) - st.session_state.get("findings_count", 0))
        
        st.divider()
        
        # Mock findings table - will be replaced with real data
        st.markdown("### Findings (Score 4)")
        
        # Sample findings for demonstration
        # These will come from real AI analysis later
        mock_findings = [
            {"control": "2.9", "name": "Security Exception Policy", "score": 4, "notes": "Policy does not include exception tracking"},
            {"control": "5.1", "name": "Password Expiry Policy", "score": 4, "notes": "Password expiry not enforced on all accounts"},
            {"control": "7.3", "name": "Vendor Management", "score": 4, "notes": "No formal vendor risk assessment process found"},
        ]
        
        for finding in mock_findings:
            with st.expander(f"🔴 Control {finding['control']} — {finding['name']}"):
                st.markdown(f"**Score:** 4 — Finding")
                st.markdown(f"**Notes:** {finding['notes']}")
                st.markdown(f"**Control ID:** {finding['control']}")

# --------------------------------------------
# PAGE: GENERATE REPORT
# --------------------------------------------
elif page == "📄 Generate Report":
    st.title("📄 Generate Report")
    st.markdown("Generate a branded PDF audit report from the analysis results.")
    st.divider()
    
    # Check if analysis was run
    if not st.session_state.get("analysis_done", False):
        st.warning("⚠️ Please run analysis first.")
    else:
        # Report settings
        st.markdown("### Report Settings")
        
        col1, col2 = st.columns(2)
        with col1:
            # Bank name input
            bank_name = st.text_input(
                "Bank Name",
                value="Sample Community Bank",
                help="Name of the bank being audited"
            )
            auditor_name = st.text_input(
                "Auditor Name", 
                value=config["report"]["auditor_name"]
            )
        
        with col2:
            # Audit date
            import datetime
            audit_date = st.date_input(
                "Audit Date",
                value=datetime.date.today()
            )
            report_title = st.text_input(
                "Report Title",
                value=config["report"]["report_title"]
            )
        
        st.divider()
        
        # Generate button
        if st.button("📄 Generate PDF Report", use_container_width=True):
            with st.spinner("Generating branded report..."):
                import time
                time.sleep(2)  # Simulating report generation
                
                # TODO: Call report_engine.py here when ready
                # from core.report_engine import generate_report
                # report_path = generate_report(findings, bank_name, audit_date)
                
                st.success("✅ Report generated successfully!")
                
                # Download button placeholder
                st.markdown("### Download")
                st.download_button(
                    label="Download PDF Report",
                    data=b"dummy audit report PDF content",
                    file_name="audit_report.pdf",
                    mime="application/pdf"
                )
