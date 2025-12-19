id: 6945a5a0313de3de69bd8a19_documentation
summary: SmolDocling: An ultra-compact vision-language model for end-to-end multi-modal document conversion Documentation
feedback link: https://docs.google.com/forms/d/e/1FAIpQLSfWkOK-in_bMMoHSZfcIvAeO58PAH9wrDqcxnJABHaxiDqhSA/viewform?usp=sf_link
environments: Web
status: Published
# QuLab: Developing a Multi-modal Document Conversion Tool with SmolDocling

## 1. Introduction: Automating Financial Data Extraction with SmolDocling
Duration: 0:05:00

<aside class="positive">
This step provides crucial context. Understanding <b>why</b> this application is important and the core technologies involved will help you grasp the subsequent technical details more effectively.
</aside>

As a Software Developer in a FinTech firm, you're tasked with building a robust tool to automate the extraction of critical financial data from unstructured documents like earnings reports and 10-K filings. Manual data entry is time-consuming and error-prone, creating a bottleneck for financial analysts. This application addresses this challenge by demonstrating how to ingest PDF financial reports, automatically identify key metrics, and present them in a structured, actionable format.

This codelab will guide you through developing a prototype using **SmolDocling**, an ultra-compact vision-language model designed for end-to-end multi-modal document conversion. SmolDocling's unique `DocTags` output provides a rich, structured representation of document content, layout, and spatial location, enabling precise extraction of financial data from unstructured PDFs.

### Why SmolDocling and DocTags are Important

Traditional OCR (Optical Character Recognition) often extracts text without understanding its context, layout, or relationship to other elements. SmolDocling, as a vision-language model, goes beyond simple text recognition. It understands the *structure* of a document by simultaneously analyzing its visual layout (vision) and textual content (language).

The `DocTags` output is SmolDocling's structured XML representation of the document. It segments the document into logical elements (paragraphs, tables, headings, figures), identifies their content, and crucially, provides their **bounding box** coordinates. This allows for:
*   **Semantic Understanding**: Knowing if text is part of a heading, a paragraph, or a table cell.
*   **Layout Preservation**: Understanding where elements are spatially located on the page.
*   **Precise Data Extraction**: Using bounding boxes to visually verify extracted data and target specific areas.

### Core Concept: Bounding Boxes

The `DocTags` output provides spatial coordinates for every identified element. Each element includes bounding box coordinates represented as:

$$ <loc_{x1}><loc_{y1}><loc_{x2}><loc_{y2}> $$

where $x_1$ and $y_1$ are the coordinates of the top-left corner, and $x_2$ and $y_2$ are the coordinates of the bottom-right corner. These coordinates are essential for visually highlighting extracted information and confirming its location on the original document.

### Application Architecture Overview

The Streamlit application simulates a workflow where a PDF document is processed by SmolDocling, its `DocTags` output is parsed, key financial metrics are extracted, and the results are visualized and made available for export.

Here's a high-level flow:

1.  **Input**: A PDF financial report is uploaded.
2.  **Image Conversion (Simulated)**: The PDF page is converted into an image for visual display.
3.  **SmolDocling Processing (Simulated)**: The document page is fed to the simulated SmolDocling model, which returns `DocTags` (an XML representation).
4.  **DocTags Parsing**: The XML is parsed to extract structured elements like text blocks and tables, along with their bounding box coordinates.
5.  **Data Extraction**: Rule-based logic is applied to the parsed tables and text to identify specific financial metrics (e.g., Revenue, Net Income, EPS).
6.  **Visualization**: The extracted elements (tables, metrics) are overlaid with bounding boxes and labels on the original document image.
7.  **Output**: Extracted key metrics and structured tables are displayed and can be exported as CSV or JSON.

This entire process is handled within a Streamlit application, making it interactive and user-friendly for demonstration and prototyping.

## 2. Setting up the Application Environment and Core Logic
Duration: 0:15:00

This application is built with Streamlit, a Python library for creating data apps. The core logic is encapsulated in several helper functions that simulate the behavior of a real SmolDocling client and subsequent data processing steps.

### Streamlit Page Configuration

The application starts by configuring the Streamlit page and initializing session state variables. Session state is crucial for Streamlit apps to maintain data across user interactions.

```python
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image, ImageDraw, ImageFont # Pillow for image manipulation
import io # For in-memory file operations
import re # Regular expressions (not heavily used in this specific app, but good for text parsing)
import json # For JSON output
from bs4 import BeautifulSoup # For parsing DocTags XML
from pypdf import PdfReader # For basic PDF reading (used to check validity, not for rendering)
from reportlab.lib.pagesizes import letter # For sample PDF generation
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

# --
# PAGE CONFIGURATION
# --
st.set_page_config(
    page_title="QuLab: SmolDocling: An ultra-compact vision-language model for end-to-end multi-modal document conversion",
    layout="wide"
)

# --
# SIDEBAR & HEADER
# --
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

# --
# SESSION STATE INITIALIZATION
# --
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
```

### Helper Functions (Backend Logic)

These functions simulate the core functionalities of the SmolDocling service and the subsequent data processing. All functions are decorated with `@st.cache_data` to improve performance by caching their outputs, preventing re-computation on every rerun.

#### `create_sample_financial_report_bytes()`
Generates a sample PDF financial report in-memory using `ReportLab`. This function is crucial for demonstrating the application without requiring a user to upload a document.

```python
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
```

#### `display_pdf_page_as_image()`
Simulates converting a PDF page to an image. In a real application, a library like `pdf2image` would be used. Here, `Pillow` is used to draw a placeholder image with document-like features, ensuring the visualization steps have an image to work with.

```python
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
```

#### `SmolDoclingClient` Class
This class simulates the interaction with the SmolDocling vision-language model. Its `process_document_page` method returns a pre-defined `DocTags` XML string. Critically, this XML includes `bbox` attributes for each element, providing the spatial coordinates for later visualization.

```python
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
```

#### `parse_doctags()`
This function uses `BeautifulSoup` to parse the `DocTags` XML, extracting text blocks and structured tables. It stores the content along with their respective bounding box coordinates. This step converts the raw XML into a more Python-friendly dictionary structure.

```python
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
```

#### `extract_financial_metrics()`
This function implements rule-based extraction. It iterates through the parsed tables, looking for specific keywords (e.g., "Revenue", "Net Income") to identify and extract key financial metrics. It also prepares elements for visualization, assigning bounding boxes and colors.

```python
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
```

#### `visualize_extracted_data()`
Takes an image of the document page and a list of extracted elements (with bounding boxes) and draws rectangles and labels on the image. This provides a visual verification of the extraction process.

```python
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
```

#### `export_financial_data()`
Prepares the extracted metrics and tables into CSV and JSON formats, ready for download. This demonstrates how to structure the output for further analysis or integration with other systems.

```python
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
```

## 3. Navigating the Introduction Page
Duration: 0:03:00

The application's navigation is controlled by the `st.sidebar.radio` widget, which allows users to switch between different views. The `Introduction` page is the default view and provides an overview of the application's purpose, the technologies used, and the problem it aims to solve.

```python
# Navigation in sidebar
page = st.sidebar.radio(
    "Navigation",
    ["Introduction", "Upload Document", "Review & Export"],
    index=0
)

# --
# PAGE 1: INTRODUCTION
# --
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
```

**Functionality:**
*   **Purpose**: This page provides the initial context and problem statement for the application.
*   **Technical Explanation**: It introduces the core concepts of SmolDocling, DocTags, and bounding boxes, including the mathematical notation for bounding box coordinates.
*   **User Persona**: It sets up a scenario for "Alex, a Software Developer at a FinTech firm," to make the problem relatable.

## 4. Uploading and Processing Financial Documents
Duration: 0:10:00

This is the central part of the application where users interact with the simulated SmolDocling model. On this page, users can upload a PDF or generate a sample document, initiate the processing, and view the intermediate and final results of the extraction.

```python
# --
# PAGE 2: UPLOAD DOCUMENT
# --
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
        page_num = st.number_input("Select Page Number", min_value=1, max_value=5, value=1) - 1
        
        if st.session_state.uploaded_pdf_file:
            if st.button("Process Document"):
                with st.spinner("Running SmolDocling Simulation..."):
                    # 1. Image Preview
                    preview_img = display_pdf_page_as_image(st.session_state.uploaded_pdf_file, page_num)
                    st.session_state.processed_image = preview_img
                    
                    # 2. Simulate DocTags Generation
                    client = SmolDoclingClient()
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
```

**Functionality Breakdown:**

1.  **File Input (`col1`)**:
    *   `st.file_uploader`: Allows users to upload a PDF file. The uploaded file's bytes are stored in `st.session_state.uploaded_pdf_file`.
    *   `st.button("Use Sample Financial Report")`: Triggers the `create_sample_financial_report_bytes()` helper function to load a pre-generated PDF, providing a quick way to test the application.
    *   `st.number_input("Select Page Number")`: A placeholder for selecting a page, though the current simulation primarily focuses on the first page.

2.  **Processing Trigger**:
    *   `st.button("Process Document")`: This button initiates the entire processing pipeline, which is wrapped in `st.spinner` for user feedback.
    *   The `if st.session_state.uploaded_pdf_file:` condition ensures processing only happens if a document is available.

3.  **Processing Steps (within the `Process Document` block)**:
    *   **Image Preview**: `display_pdf_page_as_image()` creates a visual representation of the selected PDF page.
    *   **SmolDocling Simulation**: An instance of `SmolDoclingClient` is created, and its `process_document_page()` method is called to get the simulated `DocTags` XML.
    *   **DocTags Parsing**: The `parse_doctags()` function takes the XML and converts it into a structured Python dictionary containing dataframes for tables and text blocks.
    *   **Metric Extraction**: `extract_financial_metrics()` applies rule-based logic to identify key financial metrics from the parsed data. It also generates visualization elements (bounding boxes and labels).
    *   **Visualization Generation**: `visualize_extracted_data()` takes the initial image and the visualization elements to draw bounding boxes and labels directly on the document image, showing what was extracted and where.
    *   **Export Preparation**: `export_financial_data()` formats the extracted metrics and tables into CSV and JSON strings for later download.

4.  **Document Visualization (`col2`)**:
    *   `st.image(st.session_state.processed_image)`: Displays the document image, now overlaid with bounding boxes and labels, providing visual verification of the extraction.

5.  **Displayed Results (below columns)**:
    *   **DocTags Output**: The raw `DocTags` XML is displayed in a collapsible `st.code` block, allowing developers to inspect the output structure generated by SmolDocling. The importance of the `bbox` attribute is highlighted.
    *   **Extracted Tables**: Any tables identified by `parse_doctags` are rendered as interactive Streamlit dataframes using `st.dataframe`. This allows users to review the structured data extracted.

## 5. Reviewing and Exporting Extracted Data
Duration: 0:07:00

The `Review & Export` page allows users to examine the key financial metrics and structured tables that have been extracted from the document and provides options to download this data in standard formats.

```python
# --
# PAGE 3: REVIEW & EXPORT
# --
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
```

**Functionality Breakdown:**

1.  **Data Availability Check**:
    *   The page first checks if `st.session_state.financial_metrics` is populated. If not, it displays a warning, prompting the user to process a document first, ensuring a smooth user experience.

2.  **Displaying Key Metrics (`col_a`)**:
    *   `st.subheader("Key Financial Metrics")`: A clear heading for this section.
    *   `metrics_df = pd.DataFrame(list(st.session_state.financial_metrics.items()), columns=['Metric', 'Value'])`: Converts the dictionary of extracted metrics into a Pandas DataFrame.
    *   `st.dataframe(metrics_df, hide_index=True)`: Displays the key financial metrics in an easy-to-read table format.

3.  **Displaying Extracted Tables (`col_b`)**:
    *   `st.subheader("Extracted Tables")`: A heading for the tables.
    *   It iterates through `st.session_state.parsed_document["tables"]` and displays each extracted table using `st.dataframe`, making it scrollable if the table is large (`height=150`).

4.  **Export Options**:
    *   `st.subheader("Export Options")` and descriptive markdown guide the user.
    *   `st.download_button`: Streamlit's download button widget is used to provide files for download.
        *   **CSV Export**: `Download Data as CSV` button uses `st.session_state.extracted_df_csv_content` (generated by `export_financial_data()`) to allow downloading the combined metrics and table data in CSV format.
        *   **JSON Export**: `Download Data as JSON` button uses `st.session_state.extracted_json_content` to download the structured data in JSON format, ideal for programmatic consumption.

<aside class="positive">
Providing both CSV and JSON export options is a <b>best practice</b> for data applications, catering to different downstream uses and integration needs.
</aside>

## 6. Extending and Customizing the SmolDocling Application
Duration: 0:05:00

This codelab provided a foundational understanding of building a multi-modal document conversion application using a simulated SmolDocling model and Streamlit. The architecture demonstrated covers input, processing, visualization, and export, crucial steps in any document intelligence pipeline.

### Recap of Key Learnings:

*   **SmolDocling & DocTags**: Understood the concept of vision-language models for structured document understanding and the rich XML output format with bounding box information.
*   **Streamlit Development**: Learned how to create an interactive web application, manage session state, display data, and handle file uploads and downloads.
*   **Data Parsing**: Used `BeautifulSoup` to parse complex XML structures into usable Python objects (Pandas DataFrames).
*   **Rule-Based Extraction**: Implemented simple logic to extract specific data (financial metrics) from structured tables.
*   **Visual Verification**: Integrated image processing with `Pillow` to overlay extracted information directly onto the document image, crucial for debugging and user trust.

### Potential Enhancements and Customizations:

This prototype can be extended in numerous ways to build a more robust and production-ready system:

1.  **Real SmolDocling Integration**: Replace the `SmolDoclingClient` simulation with actual API calls to a deployed SmolDocling model or similar document AI service.
2.  **Multi-page Document Processing**: Extend the application to process all pages of a PDF, aggregate data across pages, and handle navigation between visualized pages.
3.  **Advanced Extraction Rules**: Implement more sophisticated parsing and extraction logic, potentially using machine learning models (e.g., named entity recognition for text blocks) for more complex data points beyond simple table lookups.
4.  **Customizable Extraction Templates**: Allow users to define their own extraction rules or templates for different types of financial reports.
5.  **Database Integration**: Store extracted data in a database (SQL, NoSQL) for historical analysis, reporting, and integration with other enterprise systems.
6.  **Error Handling and Logging**: Implement robust error handling for PDF parsing, SmolDocling API calls, and data extraction, along with comprehensive logging.
7.  **User Authentication and Authorization**: For production use cases, secure the application with user login and role-based access control.
8.  **Interactive Data Visualization**: Beyond simple bounding boxes, integrate libraries like Plotly or Matplotlib to generate interactive charts and graphs from the extracted financial data.
9.  **Feedback Loop for Model Improvement**: Allow users to correct extraction errors, which can then be used to fine-tune the underlying SmolDocling model or refine extraction rules.
10. **Different Output Formats**: Support additional export formats like Excel workbooks, or direct integration with business intelligence tools.

By understanding the principles demonstrated in this codelab, you are well-equipped to tackle real-world challenges in automated document processing and build powerful FinTech applications.

<aside class="positive">
Consider exploring these enhancements to deepen your understanding and build a more comprehensive solution. The modular design of the application makes it easy to integrate new functionalities.
</aside>
