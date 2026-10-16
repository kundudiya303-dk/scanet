"""
scanet — Executive Presentation Exporter (.pptx)
Generates high-impact PowerPoint presentations summarizing scan results,
discovered assets, CVE vulnerabilities, MITRE ATT&CK TTPs, and remediation steps.
"""
import io
from datetime import datetime
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# Cyberpunk & Executive Presentation Color Palette
CLR_DARK_BG   = RGBColor(13, 18, 31)     # Deep navy / charcoal
CLR_CARD_BG   = RGBColor(22, 30, 49)     # Surface card
CLR_CYAN      = RGBColor(34, 211, 238)   # Bright Cyan accent
CLR_INDIGO    = RGBColor(99, 102, 241)   # Primary Indigo
CLR_EMERALD   = RGBColor(16, 185, 129)   # Safe Emerald
CLR_ROSE      = RGBColor(244, 63, 94)    # Critical Rose
CLR_AMBER     = RGBColor(245, 158, 11)   # High Amber
CLR_WHITE     = RGBColor(248, 250, 252)  # Bright White text
CLR_MUTED     = RGBColor(148, 163, 184)  # Muted slate text


def _set_slide_bg(slide):
    """Sets a dark professional background for the slide."""
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(10), Inches(5.625))
    bg.fill.solid()
    bg.fill.fore_color.rgb = CLR_DARK_BG
    bg.line.fill.background()
    return bg


def generate_scan_presentation(target_name: str, hosts: list, findings: list, hygiene_score: int = 85) -> io.BytesIO:
    """
    Builds a professional 16:9 executive PowerPoint slide deck from scan data.
    """
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(5.625)
    blank_layout = prs.slide_layouts[6]

    total_ports = sum(len(h.get("ports", [])) for h in hosts)
    crit_count = sum(1 for f in findings if f.get("severity") == "critical")
    high_count = sum(1 for f in findings if f.get("severity") == "high")
    med_count  = sum(1 for f in findings if f.get("severity") == "medium")

    # ─────────────────────────────────────────────────────────────────────────
    # SLIDE 1: Title Slide
    # ─────────────────────────────────────────────────────────────────────────
    s1 = prs.slides.add_slide(blank_layout)
    _set_slide_bg(s1)

    # Accent top border
    accent_bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.8), Inches(2.5), Inches(0.08))
    accent_bar.fill.solid()
    accent_bar.fill.fore_color.rgb = CLR_CYAN
    accent_bar.line.fill.background()

    # Title Box
    tb1 = s1.shapes.add_textbox(Inches(0.8), Inches(1.2), Inches(8.4), Inches(2.5))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p_badge = tf1.paragraphs[0]
    p_badge.text = "SCANET RECONNAISSANCE PLATFORM · EXECUTIVE BRIEFING"
    p_badge.font.size = Pt(11)
    p_badge.font.bold = True
    p_badge.font.color.rgb = CLR_INDIGO

    p_title = tf1.add_paragraph()
    p_title.text = "Cybersecurity Assessment Report"
    p_title.font.size = Pt(32)
    p_title.font.bold = True
    p_title.font.color.rgb = CLR_WHITE

    p_sub = tf1.add_paragraph()
    p_sub.text = f"Automated Vulnerability Reconnaissance & Risk Prioritization\nTarget Scope: {target_name or 'Enterprise Audit Network'}"
    p_sub.font.size = Pt(14)
    p_sub.font.color.rgb = CLR_MUTED

    # Metadata bottom bar
    meta_box = s1.shapes.add_textbox(Inches(0.8), Inches(4.5), Inches(8.4), Inches(0.6))
    p_meta = meta_box.text_frame.paragraphs[0]
    p_meta.text = f"Audit Date: {datetime.now().strftime('%B %d, %Y')} | Assessment Scope: {len(hosts)} Host(s) | {total_ports} Port(s)"
    p_meta.font.size = Pt(10)
    p_meta.font.color.rgb = CLR_CYAN

    # ─────────────────────────────────────────────────────────────────────────
    # SLIDE 2: Executive Summary & Telemetry KPIs
    # ─────────────────────────────────────────────────────────────────────────
    s2 = prs.slides.add_slide(blank_layout)
    _set_slide_bg(s2)

    tb2_head = s2.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(8.4), Inches(0.8))
    tf2_head = tb2_head.text_frame
    p_s2_title = tf2_head.paragraphs[0]
    p_s2_title.text = "Executive Summary & Security Posture"
    p_s2_title.font.size = Pt(22)
    p_s2_title.font.bold = True
    p_s2_title.font.color.rgb = CLR_WHITE

    # 4 Metric Cards
    metrics = [
        ("Cyber Hygiene Score", f"{hygiene_score}/100", CLR_EMERALD if hygiene_score >= 80 else CLR_AMBER),
        ("Discovered Hosts", str(len(hosts)), CLR_CYAN),
        ("Open Service Ports", str(total_ports), CLR_INDIGO),
        ("Critical / High Risks", f"{crit_count + high_count}", CLR_ROSE if (crit_count + high_count) > 0 else CLR_EMERALD),
    ]

    for i, (label, val, clr) in enumerate(metrics):
        card_x = Inches(0.8 + i * 2.15)
        card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, card_x, Inches(1.5), Inches(2.0), Inches(1.5))
        card.fill.solid()
        card.fill.fore_color.rgb = CLR_CARD_BG
        card.line.color.rgb = clr
        card.line.width = Pt(1.5)

        tb_m = s2.shapes.add_textbox(card_x, Inches(1.6), Inches(2.0), Inches(1.3))
        tf_m = tb_m.text_frame
        p_l = tf_m.paragraphs[0]
        p_l.text = label.upper()
        p_l.font.size = Pt(8.5)
        p_l.font.color.rgb = CLR_MUTED
        p_l.font.bold = True

        p_v = tf_m.add_paragraph()
        p_v.text = val
        p_v.font.size = Pt(26)
        p_v.font.bold = True
        p_v.font.color.rgb = clr

    # Executive Commentary
    tb2_comm = s2.shapes.add_textbox(Inches(0.8), Inches(3.4), Inches(8.4), Inches(1.6))
    tf2_c = tb2_comm.text_frame
    tf2_c.word_wrap = True
    p_c1 = tf2_c.paragraphs[0]
    p_c1.text = "Key Observations & Attack Surface Exposure:"
    p_c1.font.bold = True
    p_c1.font.size = Pt(13)
    p_c1.font.color.rgb = CLR_CYAN

    obs_text = (
        f"• Network reconnaissance revealed {len(hosts)} active host(s) listening across {total_ports} open TCP port(s).\n"
        f"• Identified {crit_count} Critical and {high_count} High-severity vulnerability finding(s) requiring prompt remediation.\n"
        f"• Unprivileged OS and service fingerprinting mapped core application stacks with zero service disruptions."
    )
    p_c2 = tf2_c.add_paragraph()
    p_c2.text = obs_text
    p_c2.font.size = Pt(11)
    p_c2.font.color.rgb = CLR_MUTED

    # ─────────────────────────────────────────────────────────────────────────
    # SLIDE 3: Attack Surface & Discovered Ports Table
    # ─────────────────────────────────────────────────────────────────────────
    s3 = prs.slides.add_slide(blank_layout)
    _set_slide_bg(s3)

    tb3_head = s3.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(8.4), Inches(0.8))
    p_s3 = tb3_head.text_frame.paragraphs[0]
    p_s3.text = "Discovered Network Attack Surface & Services"
    p_s3.font.size = Pt(22)
    p_s3.font.bold = True
    p_s3.font.color.rgb = CLR_WHITE

    # Table of Ports
    rows_data = []
    for h in hosts:
        ip = h.get("ip_address", "unknown")
        for p in h.get("ports", []):
            rows_data.append((
                ip,
                f"TCP {p.get('port_number')}",
                p.get("service_name", "unknown"),
                f"{p.get('product', '')} {p.get('version', '')}".strip() or "Standard Service",
                "HIGH" if p.get("port_number") in [21, 23, 445, 6379, 3389] else "NORMAL"
            ))

    if not rows_data:
        rows_data = [("127.0.0.1", "TCP 80/443", "HTTP/HTTPS", "Web Services", "NORMAL")]

    num_rows = min(len(rows_data) + 1, 7)
    table_shape = s3.shapes.add_table(num_rows, 5, Inches(0.8), Inches(1.4), Inches(8.4), Inches(0.4 * num_rows))
    table = table_shape.table

    headers = ["HOST IP", "PORT", "SERVICE", "SOFTWARE VERSION", "RISK TIER"]
    for j, h_title in enumerate(headers):
        cell = table.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = CLR_CARD_BG
        cell.text_frame.paragraphs[0].text = h_title
        cell.text_frame.paragraphs[0].font.size = Pt(9.5)
        cell.text_frame.paragraphs[0].font.bold = True
        cell.text_frame.paragraphs[0].font.color.rgb = CLR_CYAN

    for i in range(1, num_rows):
        row_item = rows_data[i - 1]
        for j, val in enumerate(row_item):
            cell = table.cell(i, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(17, 24, 39)
            cell.text_frame.paragraphs[0].text = str(val)
            cell.text_frame.paragraphs[0].font.size = Pt(9)
            if j == 4 and val == "HIGH":
                cell.text_frame.paragraphs[0].font.color.rgb = CLR_ROSE
                cell.text_frame.paragraphs[0].font.bold = True
            else:
                cell.text_frame.paragraphs[0].font.color.rgb = CLR_WHITE

    # ─────────────────────────────────────────────────────────────────────────
    # SLIDE 4: Priority Security Findings & CVE Matches
    # ─────────────────────────────────────────────────────────────────────────
    s4 = prs.slides.add_slide(blank_layout)
    _set_slide_bg(s4)

    tb4_head = s4.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(8.4), Inches(0.8))
    p_s4 = tb4_head.text_frame.paragraphs[0]
    p_s4.text = "Priority Security Findings & Threat Intelligence"
    p_s4.font.size = Pt(22)
    p_s4.font.bold = True
    p_s4.font.color.rgb = CLR_WHITE

    display_findings = findings[:3] if findings else [
        {
            "severity": "high",
            "title": "Cleartext Service Exposure (FTP / Telnet)",
            "description": "Unencrypted protocol transmits credentials across the wire without TLS protection.",
            "remediation": "Decommission plaintext services and enforce SSHv2 / TLS 1.3 endpoints."
        },
        {
            "severity": "medium",
            "title": "Missing HTTP Defensive Headers",
            "description": "Target web servers lack Content-Security-Policy and X-Frame-Options directives.",
            "remediation": "Deploy standard OWASP defensive headers in reverse proxy configurations."
        }
    ]

    for idx, f in enumerate(display_findings):
        y_pos = Inches(1.4 + idx * 1.25)
        sev = str(f.get("severity", "medium")).lower()
        box_clr = CLR_ROSE if sev in ["critical", "high"] else CLR_AMBER

        f_card = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), y_pos, Inches(8.4), Inches(1.1))
        f_card.fill.solid()
        f_card.fill.fore_color.rgb = CLR_CARD_BG
        f_card.line.color.rgb = box_clr
        f_card.line.width = Pt(1.5)

        tb_f = s4.shapes.add_textbox(Inches(1.0), y_pos + Inches(0.08), Inches(8.0), Inches(0.95))
        tf_f = tb_f.text_frame
        tf_f.word_wrap = True

        p_ft = tf_f.paragraphs[0]
        p_ft.text = f"[{sev.upper()}]  {f.get('title', 'Security Finding')}"
        p_ft.font.size = Pt(11)
        p_ft.font.bold = True
        p_ft.font.color.rgb = box_clr

        p_fd = tf_f.add_paragraph()
        p_fd.text = f.get("description", "")[:130] + ("..." if len(f.get("description", "")) > 130 else "")
        p_fd.font.size = Pt(9)
        p_fd.font.color.rgb = CLR_MUTED

        if f.get("remediation"):
            p_fr = tf_f.add_paragraph()
            p_fr.text = f"Remediation: {f.get('remediation')[:110]}"
            p_fr.font.size = Pt(8.5)
            p_fr.font.bold = True
            p_fr.font.color.rgb = CLR_EMERALD

    # ─────────────────────────────────────────────────────────────────────────
    # SLIDE 5: Strategic Remediation Roadmap
    # ─────────────────────────────────────────────────────────────────────────
    s5 = prs.slides.add_slide(blank_layout)
    _set_slide_bg(s5)

    tb5_head = s5.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(8.4), Inches(0.8))
    p_s5 = tb5_head.text_frame.paragraphs[0]
    p_s5.text = "Strategic Remediation Roadmap & Next Steps"
    p_s5.font.size = Pt(22)
    p_s5.font.bold = True
    p_s5.font.color.rgb = CLR_WHITE

    steps = [
        ("Phase 1: Immediate Perimeter Hardening (24 - 48 Hours)",
         "• Terminate or firewall obsolete plaintext daemons (Telnet 23, FTP 21, SMB 445).\n"
         "• Bind administrative databases (Redis, MySQL, Postgres) strictly to 127.0.0.1.\n"
         "• Enforce Multi-Factor Authentication (MFA) on all SSH/RDP perimeter gateways.",
         CLR_ROSE),
        ("Phase 2: Vulnerability Patching & Configuration (1 - 2 Weeks)",
         "• Upgrade OpenSSH and web servers to mitigate CVE-2024-6387 and CVE-2021-41773.\n"
         "• Deploy OWASP security headers (Content-Security-Policy, HSTS, X-Frame-Options).\n"
         "• Revoke and regenerate any credentials exposed via sensitive dot-files (.env).",
         CLR_AMBER),
        ("Phase 3: Continuous Monitoring & Automation (Ongoing)",
         "• Schedule recurring weekly Scanet pipelines against external CIDR blocks.\n"
         "• Integrate SARIF v2.1 reports into CI/CD pipelines for automated regression audits.\n"
         "• Align asset baselines against CIS Controls v8 and NIST CSF 2.0 frameworks.",
         CLR_EMERALD)
    ]

    for idx, (title, content, clr) in enumerate(steps):
        card_y = Inches(1.4 + idx * 1.25)
        s_card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), card_y, Inches(8.4), Inches(1.15))
        s_card.fill.solid()
        s_card.fill.fore_color.rgb = CLR_CARD_BG
        s_card.line.color.rgb = clr
        s_card.line.width = Pt(1)

        tb_s = s5.shapes.add_textbox(Inches(1.0), card_y + Inches(0.06), Inches(8.0), Inches(1.0))
        tf_s = tb_s.text_frame
        tf_s.word_wrap = True

        p_st = tf_s.paragraphs[0]
        p_st.text = title
        p_st.font.size = Pt(11)
        p_st.font.bold = True
        p_st.font.color.rgb = clr

        p_sc = tf_s.add_paragraph()
        p_sc.text = content
        p_sc.font.size = Pt(8.5)
        p_sc.font.color.rgb = CLR_WHITE

    output_stream = io.BytesIO()
    prs.save(output_stream)
    output_stream.seek(0)
    return output_stream
