

import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import io
import re
import json
from bs4 import BeautifulSoup
from pypdf import PdfReader
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="QuLab: SmolDocling: An ultra-compact vision-language model for end-to-end multi-modal document conversion",
    layout="wide"
)

# -----------------------------------------------------------------------------
# SIDEBAR & HEADER
# -----------------------------------------------------------------------------
st.sidebar.image("https://www.quantuniversity.com/assets/img/logo5.jpg")
st.sidebar.divider()

# Navigation
page = st.sidebar.radio(
    "Navigation",
    ["Introduction", "Upload Document", "Review & Export"],
    index=0
)

st.sidebar.info(
    "**Model Info**\n\n"
    "Simulating: SmolDocling\n"
    "Task: Multi-modal Doc Conversion\n"
    "Output: DocTags (XML)"
)

st.title("QuLab: SmolDocling: An ultra-compact vision-language model for end-to-end multi-modal document conversion")
st.divider()

# -----------------------------------------------------------------------------
# SESSION STATE INITIALIZATION
# -----------------------------------------------------------------------------
if "uploaded_pdf_file" not in st.session_state:
    st.session_state.uploaded_pdf_file = None
if "processed_image" not in st.session_state:
    st.session_state.processed_image = None
if "doctags_xml" not in st.session_state:
    st.session_state.doctags_xml = None
if "parsed_document" not in st.session_state:
    st.session_state.parsed_document = None
if "financial_metrics" not in st.session_state:
    st.session_state.financial_metrics = None
if "visualization_elements" not in st.session_state:
    st.session_state.visualization_elements = None
if "all_elements_for_viz" not in st.session_state:
    st.session_state.all_elements_for_viz = None
if "extracted_df_csv_content" not in st.session_state:
    st.session_state.extracted_df_csv_content = None
if "extracted_json_content" not in st.session_state:
    st.session_state.extracted_json_content = None

# -----------------------------------------------------------------------------
# HELPER FUNCTIONS (BACKEND LOGIC)
# -----------------------------------------------------------------------------

@st.cache_data
def create_sample_financial_report_bytes():
    """Generates a sample PDF financial report using ReportLab."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title
    story.append(Paragraph("Fiscal Year 2023 Financial Highlights", styles['Title']))
    story.append(Spacer(1, 12))

    # Text Body
    text_content = """
    FinTech Corp delivered robust performance in fiscal year 2023. 
    Despite global economic headwinds, our diversified portfolio ensured stability.
    Our primary focus on digital transformation has yielded significant operational efficiencies.
    Below are the key financial metrics for the period ending December 31, 2023.
    """
    story.append(Paragraph(text_content, styles['Normal']))
    story.append(Spacer(1, 20))

    # Table Data
    data = [
        ['Metric', '2023 (in Millions)', '2022 (in Millions)'],
        ['Total Revenue', '$1234.56', '$1100.20'],
        ['Operating Expenses', '$850.00', '$820.50'],
        ['Net Income', '$384.56', '$279.70'],
        ['Earnings Per Share (EPS)', '0.52', '0.45']
    ]
    
    t = Table(data)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(t)
    
    story.append(Spacer(1, 20))
    story.append(Paragraph("Management expects continued growth of 5-7% in the upcoming fiscal year.", styles['Normal']))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

@st.cache_data
def display_pdf_page_as_image(pdf_file_bytes, page_number=0, width=612, height=792):
    """Simulates converting a PDF page to an image for display."""
    # In a real app, we would use pdf2image. Here we create a visual placeholder.
    # Using the bytes to verify it's a valid PDF, but drawing a simulated representation.
    try:
        reader = PdfReader(io.BytesIO(pdf_file_bytes))
        if page_number >= len(reader.pages):
            return Image.new('RGB', (width, height), 'gray')
    except:
        pass

    image = Image.new('RGB', (int(width), int(height)), 'white')
    draw = ImageDraw.Draw(image)
    
    # Draw some "document-like" lines to simulate text
    draw.rectangle([40, 40, width-40, height-40], outline="black", width=1)
    
    # Title placeholder
    draw.rectangle([60, 60, 400, 90], fill="#e0e0e0")
    draw.text((70, 70), "FinTech Corp Financial Report 2023", fill="black")
    
    # Text block placeholder
    draw.rectangle([60, 110, 550, 180], fill="#f5f5f5")
    draw.text((70, 120), "(Text Body: FinTech Corp delivered robust performance...)", fill="black")

    # Table placeholder
    draw.rectangle([60, 200, 550, 350], outline="black")
    draw.line([60, 230, 550, 230], fill="black", width=1)
    draw.line([250, 200, 250, 350], fill="black", width=1)
    draw.text((70, 210), "Metric", fill="black")
    draw.text((260, 210), "2023 Values", fill="black")
    
    # Rows
    y = 240
    rows = ["Total Revenue: $1234.56", "Op Expenses: $850.00", "Net Income: $384.56", "EPS: 0.52"]
    for row in rows:
        draw.text((70, y), row, fill="black")
        y += 25

    draw.text((60, 750), f"Page {page_number + 1}", fill="black")
    return image

class SmolDoclingClient:
    """Simulates the SmolDocling Vision-Language Model client."""
    def process_document_page(self, pdf_file_bytes, page_number):
        """
        Returns a simulated DocTags XML string.
        Includes bounding box coordinates in format <loc_x1><loc_y1><loc_x2><loc_y2>.
        Note: Coordinates are simulated to match the 'display_pdf_page_as_image' placeholder.
        """
        xml_output = """
        <root>
            <document_meta>
                <title bbox="60 60 400 90">FinTech Corp Financial Report 2023</title>
                <page_num>1</page_num>
            </document_meta>
            <content>
                <text bbox="60 110 550 180">
                    FinTech Corp delivered robust performance in fiscal year 2023. 
                    Despite global economic headwinds, our diversified portfolio ensured stability.
                    Our primary focus on digital transformation has yielded significant operational efficiencies.
                </text>
                <otsl bbox="60 200 550 350">
                    <header>
                        <cell bbox="60 200 250 230">Metric</cell>
                        <cell bbox="250 200 550 230">2023 (in Millions)</cell>
                    </header>
                    <row>
                        <cell bbox="60 230 250 255">Total Revenue</cell>
                        <cell bbox="250 230 550 255">$1234.56</cell>
                    </row>
                    <row>
                        <cell bbox="60 255 250 280">Operating Expenses</cell>
                        <cell bbox="250 255 550 280">$850.00</cell>
                    </row>
                    <row>
                        <cell bbox="60 280 250 305">Net Income</cell>
                        <cell bbox="250 280 550 305">$384.56</cell>
                    </row>
                    <row>
                        <cell bbox="60 305 250 330">Earnings Per Share (EPS)</cell>
                        <cell bbox="250 305 550 330">0.52</cell>
                    </row>
                </otsl>
                <text bbox="60 360 550 380">
                    Management expects continued growth of 5-7% in the upcoming fiscal year.
                </text>
            </content>
        </root>
        """
        return xml_output.strip()

@st.cache_data
def parse_doctags(doctags_xml):
    """Parses the DocTags XML to extract structured data and text blocks."""
    soup = BeautifulSoup(doctags_xml, 'xml')
    
    # Parse Tables (otsl tags)
    tables = []
    otsl_tags = soup.find_all('otsl')
    for otsl in otsl_tags:
        table_data = []
        headers = [cell.text.strip() for cell in otsl.find('header').find_all('cell')]
        rows = otsl.find_all('row')
        for row in rows:
            cells = [cell.text.strip() for cell in row.find_all('cell')]
            if len(cells) == len(headers):
                table_data.append(cells)
        
        if table_data:
            df = pd.DataFrame(table_data, columns=headers)
            # Store metadata including bounding box
            bbox = [float(x) for x in otsl['bbox'].split()]
            tables.append({"dataframe": df, "bbox": bbox, "raw_tag": str(otsl)})

    # Parse Text
    text_blocks = []
    text_tags = soup.find_all('text')
    for txt in text_tags:
        content = txt.text.strip()
        if content:
            bbox = [float(x) for x in txt['bbox'].split()]
            text_blocks.append({"content": content, "bbox": bbox})
            
    return {"tables": tables, "text_blocks": text_blocks}

@st.cache_data
def extract_financial_metrics(parsed_document):
    """Rule-based extraction of key metrics from parsed tables and text."""
    metrics = {}
    viz_elements = []

    # 1. Extract from Tables
    # Look for specific keywords in the first column of identified tables
    target_metrics = ["Revenue", "Net Income", "EPS", "Earnings Per Share"]
    
    for table_info in parsed_document["tables"]:
        df = table_info["dataframe"]
        # Assuming first column is Metric name
        metric_col = df.columns[0]
        value_col = df.columns[1] # Assuming second column is current year value
        
        for index, row in df.iterrows():
            label = row[metric_col]
            val = row[value_col]
            
            # Check if any target metric is in the label
            if any(tm.lower() in label.lower() for tm in target_metrics):
                clean_key = label.split('(')[0].strip() # Clean "Earnings (EPS)" -> "Earnings"
                metrics[clean_key] = val
                
                # For visualization, we simulate the cell bbox based on table bbox logic
                # In a real scenario, we'd have exact cell bbox from XML. 
                # Here we approximate for the visual effect based on the row index.
                tbl_bbox = table_info['bbox']
                # Approx row height calculation
                row_height = 25
                header_height = 30
                y1 = tbl_bbox[1] + header_height + (index * row_height)
                y2 = y1 + row_height
                # Box covering the whole row
                viz_elements.append({
                    "bbox": [tbl_bbox[0], y1, tbl_bbox[2], y2],
                    "label": f"{clean_key}: {val}",
                    "type": "metric_table",
                    "color": "blue"
                })

    # Add Table Bounding Boxes
    for table_info in parsed_document["tables"]:
        viz_elements.append({
            "bbox": table_info['bbox'],
            "label": "Detected Table",
            "type": "table",
            "color": "purple"
        })
        
    return metrics, viz_elements

@st.cache_data
def visualize_extracted_data(page_image, extracted_elements):
    """Draws bounding boxes and labels on the PDF page image."""
    if page_image.mode == 'RGB':
        draw_image = page_image.copy()
    else:
        draw_image = page_image.convert('RGB')
    
    draw = ImageDraw.Draw(draw_image)
    try:
        # Try loading a standard font
        # The error "cannot import name 'is_directory' from 'PIL._util'"
        # occurs internally within PIL.ImageFont during its module import,
        # not during the call to truetype or load_default.
        # This typically indicates an issue with the Pillow library installation
        # or a version incompatibility, not an error in the application's code.
        # Assuming a corrected Pillow installation or compatible environment,
        # this line would function as intended.
        font = ImageFont.truetype("arial.ttf", 14)
    except IOError:
        # Fallback to default font if arial.ttf is not found
        font = ImageFont.load_default()
    except Exception as e:
        # Catch any other unexpected errors during font loading
        st.error(f"Error loading font for visualization: {e}. Using default font.")
        font = ImageFont.load_default()

    for elem in extracted_elements:
        bbox = elem['bbox'] # [x1, y1, x2, y2]
        color = elem['color']
        label = elem['label']
        
        # Draw Rectangle
        draw.rectangle(bbox, outline=color, width=3)
        
        # Draw Text Label Background
        # textbbox requires font.
        try:
            text_bbox_coords = draw.textbbox((bbox[0], bbox[1] - 20), label, font=font)
            draw.rectangle(text_bbox_coords, fill=color)
            
            # Draw Text
            draw.text((bbox[0], bbox[1] - 20), label, fill="white", font=font)
        except Exception as e:
            # If textbbox or text drawing fails (e.g., due to font issues),
            # just draw the rectangle without text.
            st.warning(f"Could not draw text label for bbox {bbox}: {e}")

    return draw_image

@st.cache_data
def export_financial_data(extracted_metrics, parsed_tables):
    """Prepares CSV and JSON data for export."""
    # CSV Preparation
    metrics_df = pd.DataFrame(list(extracted_metrics.items()), columns=['Metric', 'Value'])
    metrics_df.insert(0, 'Data_Type', 'Key Metrics')
    
    all_tables_df_list = []
    for i, table_info in enumerate(parsed_tables):
        df = table_info["dataframe"].copy()
        if not df.empty:
            df.insert(0, 'Data_Type', f'Table_{i+1}')
            all_tables_df_list.append(df)
            
    final_df_list = [metrics_df] + all_tables_df_list
    combined_df = pd.concat(final_df_list, ignore_index=True, sort=False)
    
    csv_buffer = io.StringIO()
    combined_df.to_csv(csv_buffer, index=False)
    csv_content = csv_buffer.getvalue()

    # JSON Preparation
    json_output = {
        "key_metrics": extracted_metrics,
        "tables": []
    }
    for i, table_info in enumerate(parsed_tables):
        if not table_info["dataframe"].empty:
            json_output["tables"].append({
                f"table_{i+1}": table_info["dataframe"].to_dict(orient="records")
            })
    json_content = json.dumps(json_output, indent=4)
    
    return csv_content, json_content

# -----------------------------------------------------------------------------
# PAGE 1: INTRODUCTION
# -----------------------------------------------------------------------------
if page == "Introduction":
    st.markdown("# Automated Financial Report Data Extraction with SmolDocling")
    st.markdown("## Introduction")
    st.markdown("""
    As a Software Developer at a fast-paced FinTech firm, you, Alex, are constantly looking for ways to streamline operations and empower financial analysts. A significant bottleneck in financial analysis is the manual extraction of key data from unstructured financial documents like earnings reports, 10-K filings, and prospectuses. This process is not only time-consuming but also prone to human error, leading to delays and inconsistencies.

    Your task is to build a robust tool that automates this data extraction. The goal is to ingest PDF financial reports, automatically identify critical financial metrics (e.g., revenue, net income, EPS, balance sheet items), and present them in a structured, easily consumable format. This will free up analysts to focus on deeper insights rather than data entry.

    This application will guide you through developing a prototype using **SmolDocling**, an ultra-compact vision-language model designed for end-to-end multi-modal document conversion. We'll leverage SmolDocling's unique `DocTags` output, which provides a rich, structured representation of document content, layout, and spatial location. This will allow us to precisely pinpoint and extract the required financial data, transforming unstructured PDFs into actionable intelligence.
    """)
    
    st.markdown("### The Math Behind Bounding Boxes")
    st.markdown("""
    The `DocTags` output provides spatial coordinates for every identified element. 
    Each element includes bounding box coordinates represented as:
    """)
    st.markdown(r"$$ <loc_{x1}><loc_{y1}><loc_{x2}><loc_{y2}> $$")
    st.markdown(f"where $x_1$ and $y_1$ are the coordinates of the top-left corner, and $x_2$ and $y_2$ are the coordinates of the bottom-right corner.")

# -----------------------------------------------------------------------------
# PAGE 2: UPLOAD DOCUMENT
# -----------------------------------------------------------------------------
elif page == "Upload Document":
    st.markdown("## 2. Upload and Process Financial Report")
    st.info("Upload a PDF or use the sample generation tool to simulate the workflow.")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Input")
        uploaded_file = st.file_uploader("Upload PDF Financial Report", type=["pdf"])
        
        if st.button("Use Sample Financial Report"):
            sample_bytes = create_sample_financial_report_bytes()
            st.session_state.uploaded_pdf_file = sample_bytes
            st.success("Sample PDF loaded!")
            
        if uploaded_file is not None:
            st.session_state.uploaded_pdf_file = uploaded_file.getvalue()
            st.success("File uploaded successfully.")

        # Page selection (Simulated for 1 page)
        # Note: If a real PDF is uploaded with more pages, this would need to reflect reader.pages length
        # For simulation, it's fine.
        page_num = st.number_input("Select Page Number", min_value=1, max_value=5, value=1) - 1
        
        if st.session_state.uploaded_pdf_file:
            if st.button("Process Document"):
                with st.spinner("Running SmolDocling Simulation..."):
                    # 1. Image Preview
                    preview_img = display_pdf_page_as_image(st.session_state.uploaded_pdf_file, page_num)
                    st.session_state.processed_image = preview_img
                    
                    # 2. Simulate DocTags Generation
                    client = SmolDoclingClient()
                    # Passing bytes
                    xml_out = client.process_document_page(st.session_state.uploaded_pdf_file, page_num)
                    st.session_state.doctags_xml = xml_out
                    
                    # 3. Parse Data
                    parsed = parse_doctags(xml_out)
                    st.session_state.parsed_document = parsed
                    
                    # 4. Extract Metrics
                    metrics, viz_elems = extract_financial_metrics(parsed)
                    st.session_state.financial_metrics = metrics
                    st.session_state.visualization_elements = viz_elems
                    st.session_state.all_elements_for_viz = viz_elems
                    
                    # 5. Generate Visualization
                    viz_img = visualize_extracted_data(preview_img, viz_elems)
                    st.session_state.processed_image = viz_img # Update with overlays

                    # 6. Prepare Export
                    csv_d, json_d = export_financial_data(metrics, parsed["tables"])
                    st.session_state.extracted_df_csv_content = csv_d
                    st.session_state.extracted_json_content = json_d
                    
                    st.success("Processing Complete! Go to 'Review & Export' or scroll down.")

    with col2:
        st.subheader("Document Visualization")
        if st.session_state.processed_image:
            st.image(st.session_state.processed_image, caption="Document Analysis Overlay", use_container_width=True)
        else:
            st.markdown("*No document processed yet.*")

    # Display Results below if processed
    if st.session_state.doctags_xml:
        st.divider()
        st.markdown("### DocTags Output (Excerpt)")
        st.markdown("""
        SmolDocling generates an XML representation. Note the `bbox` attributes which allow us to map data back to the image.
        """)
        st.code(st.session_state.doctags_xml, language='xml')
        
        st.divider()
        st.markdown("### Extracted Tables")
        if st.session_state.parsed_document and st.session_state.parsed_document["tables"]:
            for i, tbl in enumerate(st.session_state.parsed_document["tables"]):
                st.write(f"**Table {i+1}**")
                st.dataframe(tbl["dataframe"])
        else:
            st.warning("No tables detected.")

# -----------------------------------------------------------------------------
# PAGE 3: REVIEW & EXPORT
# -----------------------------------------------------------------------------
elif page == "Review & Export":
    st.markdown("## 3. Review & Export Data")
    
    if not st.session_state.financial_metrics:
        st.warning("No data processed yet. Please go to 'Upload Document' and process a file first.")
    else:
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.subheader("Key Financial Metrics")
            metrics_df = pd.DataFrame(list(st.session_state.financial_metrics.items()), columns=['Metric', 'Value'])
            st.dataframe(metrics_df, hide_index=True)

        with col_b:
            st.subheader("Extracted Tables")
            if st.session_state.parsed_document and st.session_state.parsed_document["tables"]:
                for i, tbl in enumerate(st.session_state.parsed_document["tables"]):
                    st.write(f"**Table {i+1} Data**")
                    st.dataframe(tbl["dataframe"], height=150)

        st.divider()
        st.subheader("Export Options")
        st.markdown("Download the structured data for downstream analysis.")
        
        c1, c2 = st.columns(2)
        with c1:
            st.download_button(
                label="Download Data as CSV",
                data=st.session_state.extracted_df_csv_content,
                file_name="financial_data.csv",
                mime="text/csv"
            )
        with c2:
            st.download_button(
                label="Download Data as JSON",
                data=st.session_state.extracted_json_content,
                file_name="financial_data.json",
                mime="application/json"
            )

# -----------------------------------------------------------------------------
# FOOTER
# -----------------------------------------------------------------------------
st.divider()
st.markdown("**QuLab** - Simulated Environment for SmolDocling")

