import os
import inspect
import datetime
import gradio as gr
from crew import run_procurement_crew

# Wrapper: Run Crew + Save Report as Downloadable File 
def run_and_save(company_name, industry, budget, purpose, requirements):
    if len(inspect.signature(run_procurement_crew).parameters) >= 6:
        status, report_html = run_procurement_crew(
            company_name, industry, budget, purpose, requirements, ""
        )
    else:
        status, report_html = run_procurement_crew(
            company_name, industry, budget, purpose, requirements
        )

    os.makedirs("reports", exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join("reports", f"Procurement_Report_{timestamp}.html")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(report_html)

    return status, file_path

# Navy & Gold 
custom_css = """
.gradio-container {
    font-family: 'Inter', system-ui, sans-serif !important;
}

/* ===== Animated Hero Header ===== */
.hero-header {
    text-align: center;
    padding: 32px 0 20px;
}

/* ===== Navy Box with Gold Border ===== */
.hero-box {
    display: inline-flex;
    align-items: center;
    gap: 24px;
    background: linear-gradient(135deg, #0B2545 0%, #13315C 55%, #1D4E89 100%);
    color: #ffffff;
    padding: 36px 64px;
    border-radius: 24px;
    border: 1px solid rgba(212, 175, 55, 0.5);
    box-shadow: 0 16px 36px rgba(11, 37, 69, 0.4);
    animation: float 3.5s ease-in-out infinite;
}
@keyframes float {
    0%, 100% { transform: translateY(0); }
    50%      { transform: translateY(-12px); }
}

/* ===== Emoji Inside the Box (Gold Glow) ===== */
.hero-icon {
    font-size: 3.4em;
    display: inline-block;
    animation: wiggle 2.5s ease-in-out infinite;
    filter: drop-shadow(0 6px 14px rgba(212, 175, 55, 0.45));
}
@keyframes wiggle {
    0%, 100% { transform: translateY(0) rotate(0deg); }
    25%      { transform: translateY(-6px) rotate(-8deg); }
    75%      { transform: translateY(-2px) rotate(8deg); }
}

.hero-title {
    font-size: 2.5em;
    font-weight: 900;
    letter-spacing: -0.5px;
    color: #ffffff;
}

.hero-subtitle {
    color: #64748b;
    font-size: 1.05em;
    max-width: 620px;
    margin: 20px auto 0;
    line-height: 1.6;
}

/* ===== Section Titles (EXTRA BOLD) ===== */
.section-title,
.section-title p,
.section-title strong {
    font-size: 1em !important;
    font-weight: 900 !important;
    color: #13315C !important;
    margin-bottom: 10px !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    -webkit-text-stroke: 0.4px #13315C;
}

/* ===== Field Labels (Company Name, Industry, ...) ===== */
.label-text,
.block label > span {
    color: #13315C !important;
    font-weight: 600 !important;
}

/* ===== CheckboxGroup Label (Key Requirements) - FORCED NAVY ===== */
.checkbox-group fieldset > legend,
.checkbox-group fieldset > legend > span,
.checkbox-group legend,
.checkbox-group legend span,
.checkbox-group .label-text,
div.checkbox-group span.label-text {
    color: #13315C !important;
    font-weight: 700 !important;
    -webkit-text-stroke: 0.2px #13315C !important;
}

/* ===== Checkbox Items (Text + Box) unified with Navy ===== */
.checkbox-group span,
.checkbox-group label {
    color: #13315C !important;
}
.checkbox-group input[type="checkbox"] {
    accent-color: #13315C !important;
}

/* ===== Status Box ===== */
.status-box textarea {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.8em !important;
    background: var(--background-fill-secondary) !important;
}

/* ===== Generate Button (Navy Gradient) ===== */
#generate-btn {
    background: linear-gradient(135deg, #13315C 0%, #1D4E89 100%) !important;
    border: none !important;
    font-weight: 700 !important;
    letter-spacing: 0.3px;
    box-shadow: 0 6px 18px rgba(11, 37, 69, 0.35) !important;
}
#generate-btn:hover {
    background: linear-gradient(135deg, #0B2545 0%, #13315C 100%) !important;
}

/* ===== Download Button (Gold Accent) ===== */
#download-btn {
    background: #ffffff !important;
    color: #0B2545 !important;
    border: 2px solid #D4AF37 !important;
    font-weight: 700 !important;
}
#download-btn:hover {
    background: #D4AF37 !important;
    color: #0B2545 !important;
}
"""

with gr.Blocks(
    theme=gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="slate",
        neutral_hue="slate",
        font=[gr.themes.GoogleFont("Inter"), "system-ui"]
    ),
    css=custom_css,
    title="Multi Agent Procurement Assistant"
) as demo:

    gr.HTML("""
    <div class="hero-header">
        <div class="hero-box">
            <span class="hero-icon">🤖</span>
            <span class="hero-title">Multi Agent Procurement Assistant</span>
        </div>
        <div class="hero-subtitle">
            AI-powered multi-agent system that researches smartphones, compares options, 
            and generates professional procurement reports tailored to your business.
        </div>
    </div>
    """)

    gr.Markdown("---")

    # Form Section: Two Balanced Columns 
    with gr.Row(equal_height=False):
        with gr.Column(scale=1, min_width=300):
            gr.Markdown("🏢 **Company Information**", elem_classes="section-title")
            
            company_name = gr.Textbox(
                label="Company Name", 
                placeholder="e.g. ABC Technology"
            )
            
            industry = gr.Textbox(
                label="Industry", 
                placeholder="e.g. Software Development"
            )
            
            budget = gr.Number(
                label="Budget ($)", 
                minimum=100, 
                step=50,
                placeholder="700"
            )
            
            purpose = gr.Textbox(
                label="Purpose",
                placeholder="e.g. Purchase smartphones for the engineering team",
                lines=2
            )

        # Right Column: Requirements
        with gr.Column(scale=1, min_width=300):
            gr.Markdown("📱 **Device Requirements**", elem_classes="section-title")
            
            requirements = gr.CheckboxGroup(
                label="Key Requirements",
                choices=[
                    "8GB RAM or more",
                    "256GB Storage or more",
                    "Long battery life",
                    "High-quality camera",
                    "5G connectivity",
                    "Premium brand"
                ],
                value=[],
                info="Select all mandatory specifications"
            )

    # Generate Button
    with gr.Row():
        with gr.Column(scale=1):
            pass
        with gr.Column(scale=2):
            generate_btn = gr.Button(
                "🚀 Generate Procurement Report",
                variant="primary",
                size="lg",
                elem_id="generate-btn"
            )
        with gr.Column(scale=1):
            pass

    # Output Section: Status + Download Button 
    gr.Markdown("---")
    
    gr.Markdown("📊 **Live Status**", elem_classes="section-title")
    status_output = gr.Textbox(
        label="Agent Activity",
        interactive=False,
        placeholder="Waiting to start analysis...",
        max_lines=12,
        elem_classes="status-box"
    )

    with gr.Row():
        with gr.Column(scale=2):
            pass
        with gr.Column(scale=1, min_width=180):
            download_btn = gr.DownloadButton(
                "Download Report",
                variant="secondary",
                size="sm",
                elem_id="download-btn"
            )
        with gr.Column(scale=2):
            pass

    # Quick Examples 
    gr.Markdown("---")
    gr.Markdown("⚡ **Quick Examples** — Click to auto-fill", elem_classes="section-title")
    
    with gr.Row():
        example_buttons = [
            ("🏢 Tech Company", ["ABC Technology", "Software Development", 700, 
             "Purchase smartphones for engineering team", 
             ["8GB RAM or more", "256GB Storage or more", "Long battery life"]]),
            ("🎥 Content Team", ["Nova Media", "Digital Marketing", 500, 
             "Content creation team devices", 
             ["High-quality camera", "256GB Storage or more", "5G connectivity"]]),
            ("💼 Executives", ["Vertex Finance", "Financial Services", 1000, 
             "Flagship phones for executives", 
             ["Premium brand", "8GB RAM or more", "5G connectivity", "High-quality camera"]])
        ]
        
        for label, data in example_buttons:
            gr.Button(label, size="sm").click(
                fn=lambda d=data: d,
                outputs=[company_name, industry, budget, purpose, requirements]
            )

    # Footer 
    gr.Markdown(
        "<div style='text-align:center; font-size:0.75em; opacity:0.5; margin-top:20px; padding-bottom:10px;'>"
        "Powered by CrewAI · Groq · Tavily | Multi-Agent Procurement System"
        "</div>"
    )

    # Event Handler 
    generate_btn.click(
        fn=run_and_save,
        inputs=[company_name, industry, budget, purpose, requirements],
        outputs=[status_output, download_btn],
        api_name="generate_report"
    )

if __name__ == "__main__":
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        show_error=True
    )

    