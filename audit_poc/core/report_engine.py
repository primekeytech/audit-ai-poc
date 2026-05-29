# ============================================
# AUDIT POC - Report Generation Engine
# ============================================
# This file generates the branded PDF report
# from the populated workbook findings.
#
# Process:
# 1. Read findings from populated workbook
# 2. Load HTML report template
# 3. Inject findings into template
# 4. Convert HTML to PDF using WeasyPrint
#
# Branding: Genesis GV70 aesthetic
# - Deep navy background: #0A0F1E
# - Blood orange accent: #FF6B23
# - Premium, trustworthy, modern
# ============================================

import os
from pathlib import Path
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

# ============================================
# MAIN REPORT GENERATION FUNCTION
# ============================================

def generate_report(findings: list, bank_info: dict, config: dict) -> str:
    """
    Main function - generates complete branded PDF report.
    
    Args:
        findings: List of finding dictionaries from workbook_engine
        bank_info: {
            "bank_name": "Sample Community Bank",
            "auditor_name": "Benjamin Caruso",
            "audit_date": "2026-05-26",
            "report_title": "IT Audit Report"
        }
        config: Configuration dictionary
        
    Returns:
        str: Path to generated PDF file
    """
    
    print(f"Generating report for: {bank_info.get('bank_name')}")
    print(f"Total findings: {len(findings)}")
    
    # Step 1 - Calculate risk rating from findings
    risk_rating = calculate_risk_rating(findings)
    
    # Step 2 - Load HTML template
    html_content = render_html_template(
        findings=findings,
        bank_info=bank_info,
        risk_rating=risk_rating,
        config=config
    )
    
    # Step 3 - Convert HTML to PDF
    output_path = html_to_pdf(html_content, bank_info, config)
    
    print(f"Report generated: {output_path}")
    return output_path

# ============================================
# RISK RATING CALCULATION
# ============================================

def calculate_risk_rating(findings: list) -> dict:
    """
    Calculates overall risk rating based on findings.
    Uses weighted scoring - more critical findings = worse rating.
    
    Rating Scale (Benjamin's system):
    - Good: 0-2 findings
    - Satisfactory: 3-5 findings  
    - Moderate: 6-9 findings
    - Unsatisfactory: 10-14 findings
    - Poor: 15+ findings
    
    Args:
        findings: List of score 4 finding dictionaries
        
    Returns:
        dict: {
            "rating": "Satisfactory",
            "color": "#1D9E75",
            "finding_count": 4,
            "description": "Minor improvements needed"
        }
    """
    
    # Count total findings
    finding_count = len(findings)
    
    # Determine rating based on finding count
    if finding_count <= 2:
        return {
            "rating": "Good",
            "color": "#1D9E75",
            "finding_count": finding_count,
            "description": "Only a few minor issues identified"
        }
    elif finding_count <= 5:
        return {
            "rating": "Satisfactory",
            "color": "#FFB703",
            "finding_count": finding_count,
            "description": "Minor improvements needed"
        }
    elif finding_count <= 9:
        return {
            "rating": "Moderate",
            "color": "#F29E4C",
            "finding_count": finding_count,
            "description": "Several issues require attention"
        }
    elif finding_count <= 14:
        return {
            "rating": "Unsatisfactory",
            "color": "#E24B4A",
            "finding_count": finding_count,
            "description": "Significant remediation is required"
        }
    else:
        return {
            "rating": "Poor",
            "color": "#8B0000",
            "finding_count": finding_count,
            "description": "Critical control failures detected"
        }

# ============================================
# HTML TEMPLATE RENDERING
# ============================================

def render_html_template(findings: list, bank_info: dict, risk_rating: dict, config: dict) -> str:
    """
    Renders the Jinja2 HTML template with report data.
    
    Args:
        findings: List of findings
        bank_info: Bank and audit information
        risk_rating: Calculated risk rating
        config: Configuration dictionary
        
    Returns:
        str: Complete rendered HTML string
    """
    
    # Set up Jinja2 template environment
    templates_folder = config["paths"]["templates_folder"]
    env = Environment(
        loader=FileSystemLoader(templates_folder)
    )
    
    # Load the report template
    template = env.get_template("report.html")
    
    # Render template with all data
    html_content = template.render(
        # Bank information
        bank_name=bank_info.get("bank_name", "Bank Name"),
        auditor_name=bank_info.get("auditor_name", "Auditor"),
        audit_date=bank_info.get("audit_date", datetime.now().strftime("%B %d, %Y")),
        report_title=bank_info.get("report_title", "IT Audit Report"),
        
        # Findings data
        findings=findings,
        finding_count=len(findings),
        
        # Risk rating
        risk_rating=risk_rating,
        
        # Branding from config
        accent_color=config["report"]["accent_color"],
        dark_background=config["report"]["dark_background"],
        company_name=config["report"]["company_name"],
        
        # Generation timestamp
        generated_date=datetime.now().strftime("%B %d, %Y at %I:%M %p")
    )
    
    return html_content

# ============================================
# HTML TO PDF CONVERSION
# ============================================

def html_to_pdf(html_content: str, bank_info: dict, config: dict) -> str:
    """
    Converts rendered HTML to a branded PDF file.
    Uses WeasyPrint for high quality PDF generation.
    
    Args:
        html_content: Rendered HTML string
        bank_info: Bank information for filename
        config: Configuration dictionary
        
    Returns:
        str: Path to generated PDF file
    """
    
    try:
        # Import WeasyPrint
        from weasyprint import HTML, CSS
        
        # Create output directory if needed
        output_folder = config["paths"]["outputs_folder"]
        Path(output_folder).mkdir(parents=True, exist_ok=True)
        
        # Build output filename
        bank_name = bank_info.get("bank_name", "bank").replace(" ", "_")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"{output_folder}{bank_name}_audit_report_{timestamp}.pdf"
        
        # Convert HTML to PDF
        HTML(string=html_content).write_pdf(output_path)
        
        print(f"PDF saved to: {output_path}")
        return output_path
        
    except ImportError:
        raise ImportError(
            "WeasyPrint not installed! "
            "Run: pip install weasyprint"
        )
    except Exception as e:
        raise Exception(f"PDF generation failed: {str(e)}")

# ============================================
# HELPER - SAVE HTML FOR DEBUGGING
# ============================================

def save_html_debug(html_content: str, config: dict) -> str:
    """
    Saves rendered HTML to file for debugging.
    Open in browser to preview report before PDF.
    
    Args:
        html_content: Rendered HTML string
        config: Configuration dictionary
        
    Returns:
        str: Path to saved HTML file
    """
    
    output_folder = config["paths"]["outputs_folder"]
    Path(output_folder).mkdir(parents=True, exist_ok=True)
    
    html_path = f"{output_folder}report_preview.html"
    
    with open(html_path, "w") as f:
        f.write(html_content)
    
    print(f"HTML preview saved: {html_path}")
    print("Open in browser to preview report!")
    
    return html_path
