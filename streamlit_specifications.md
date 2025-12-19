# Streamlit Application Specification: Automated Financial Report Data Extraction

## Application Overview

This Streamlit application provides a user-friendly interface for automating the extraction of key financial data from PDF financial reports. Leveraging a simulated SmolDocling model, it processes unstructured documents, identifies critical metrics, and presents them in a structured, verifiable format. The application is designed to assist "Software Developer" personas, like Alex, in building robust tools for FinTech firms, reducing manual effort and improving data consistency in financial analysis.

### Learning Goals

*   Understand the workflow of financial report data extraction using a vision-language model.
*   Learn to integrate `DocTags` output, an XML-like representation with spatial information, for precise data pinpointing.
*   Apply rule-based logic and pattern matching for extracting structured financial metrics from `DocTags`.
*   Visualize extracted data (tables, key-value pairs) on the original document for verification.
*   Provide functionality to export processed data in standard formats (CSV, JSON).
*   Simulate a multi-page Streamlit application structure within a single `app.py` file.

## User Interface Requirements

The application will be structured as a multi-page application simulated within `app.py` using a sidebar for navigation.

### Layout and Navigation Structure

The application will feature a sidebar for navigation and main content area for displaying components.

*   **Sidebar**:
    *   Application Title: "Automated Financial Report Data Extraction"
    *   Navigation Menu:
        *   "Introduction" (Home Page)
        *   "Upload Document"
        *   "Review & Export"
    *   Model Information (e.g., "Simulating SmolDocling Model")
*   **Main Content Area**: Dynamically renders content based on sidebar selection.

### Input Widgets and Controls

*   **"Upload Document" Page**:
    *   `st.file_uploader`: For uploading PDF financial reports. Accepts `application/pdf` files.
    *   `st.number_input` (optional): To select a specific page number for processing if the PDF has multiple pages (default to 0 or 1, depending on 0/1-indexing).
    *   `st.button`: "Process Document" to trigger the SmolDocling simulation and data extraction.
*   **"Review & Export" Page**:
    *   No direct input widgets on this page, as it displays processed results from the "Upload Document" page.

### Visualization Components

*   **"Upload Document" Page**:
    *   After upload, before processing: `st.image` displaying a preview of the first page of the uploaded PDF (or selected page).
    *   After processing:
        *   `st.subheader`: "DocTags Output (Excerpt)" with `st.code` displaying a snippet of the simulated XML.
        *   `st.dataframe`: For displaying parsed tables from `DocTags`.
        *   `st.dataframe` or `st.table`: For displaying extracted key financial metrics.
        *   `st.image`: Visualizing extracted data overlaid on the PDF page (bounding boxes, labels).
*   **"Review & Export" Page**:
    *   `st.subheader`: "Extracted Financial Metrics" with `st.dataframe` or `st.table` showing the key metrics.
    *   `st.subheader`: "Extracted Tables" with multiple `st.dataframe` components for each identified table.
    *   `st.download_button`: "Download Data as CSV" (for `output/financial_data.csv`).
    *   `st.download_button`: "Download Data as JSON" (for `output/financial_data.json`).

### Interactive Elements and Feedback Mechanisms

*   **File Upload Status**: Messages indicating successful upload or upload errors.
*   **Processing Status**: `st.spinner` or `st.status` to show "Processing document...", "Extracting metrics...", "Generating visualizations...".
*   **Error Handling**: `st.error` messages for invalid PDF files, processing failures, or no data found.
*   **Data Display**: Dynamic updates of `st.dataframe`, `st.table`, and `st.image` components as data is extracted and visualized.
*   **Export Confirmation**: `st.success` message upon successful download (optional, as `st.download_button` handles this implicitly).

## Additional Requirements

### Annotation and Tooltip Specifications

*   **Bounding Boxes on PDF Image**:
    *   Each bounding box will have a distinct color:
        *   Tables: Purple
        *   Key Financial Metrics (from tables): Blue
        *   Key Financial Metrics (from text blocks): Green
    *   Labels will be displayed near the bounding box, e.g., "Table 1", "Revenue: \$1234.56 (Table)", "EPS: 0.52 (Text)".
    *   The labels should be clear and concise, indicating the extracted metric and its source (table or text).
    *   Tooltips are not directly supported by `st.image` for overlaid drawings, but the labels serve a similar purpose.

### Save the States of the Fields Properly

*   The application will leverage `st.session_state` to persist data across re-runs and "page" navigations.
*   **Key state variables**:
    *   `st.session_state.uploaded_pdf_file`: Stores the `UploadedFile` object.
    *   `st.session_state.processed_image`: Stores the `PIL.Image` of the displayed PDF page.
    *   `st.session_state.doctags_xml`: Stores the simulated `DocTags` XML string.
    *   `st.session_state.parsed_document`: Stores the dictionary output from `parse_doctags`.
    *   `st.session_state.financial_metrics`: Stores the dictionary of extracted key metrics.
    *   `st.session_state.visualization_elements`: Stores the list of elements (bbox, label, color) for visualization.
    *   `st.session_state.all_elements_for_viz`: Combined list for visualization.
    *   `st.session_state.extracted_df_csv_content`: Stores the CSV content for download.
    *   `st.session_state.extracted_json_content`: Stores the JSON content for download.

## Notebook Content and Code Requirements

The Streamlit application will integrate the core logic from the Jupyter Notebook, presenting the steps interactively. All markdown content will be rendered using `st.markdown` and code snippets will be adapted for the Streamlit environment.

### 1. Application Introduction and Setup

*   **Markdown**:
    ```python
    st.markdown("# Automated Financial Report Data Extraction with SmolDocling")
    st.markdown("## Introduction")
    st.markdown("""
    As a Software Developer at a fast-paced FinTech firm, you, Alex, are constantly looking for ways to streamline operations and empower financial analysts. A significant bottleneck in financial analysis is the manual extraction of key data from unstructured financial documents like earnings reports, 10-K filings, and prospectuses. This process is not only time-consuming but also prone to human error, leading to delays and inconsistencies.

    Your task is to build a robust tool that automates this data extraction. The goal is to ingest PDF financial reports, automatically identify critical financial metrics (e.g., revenue, net income, EPS, balance sheet items), and present them in a structured, easily consumable format. This will free up analysts to focus on deeper insights rather than data entry.

    This application will guide you through developing a prototype using **SmolDocling**, an ultra-compact vision-language model designed for end-to-end multi-modal document conversion. We'll leverage SmolDocling's unique `DocTags` output, which provides a rich, structured representation of document content, layout, and spatial location. This will allow us to precisely pinpoint and extract the required financial data, transforming unstructured PDFs into actionable intelligence.
    """)
    ```
*   **Dependencies**: The `pip install` command will be noted in a `requirements.txt` file.

### 2. Environment Setup and Data Preparation

*   **Code**:
    ```python
    # Import required dependencies (Streamlit specific imports will be added)
    import os
    from pypdf import PdfReader
    from PIL import Image, ImageDraw, ImageFont
    import pandas as pd
    # import matplotlib.pyplot as plt # Streamlit uses st.image for display
    import io
    from bs4 import BeautifulSoup
    import re
    import json
    import streamlit as st

    # No need to create directories directly in Streamlit app; outputs will be in memory or temp files.
    # os.makedirs('data', exist_ok=True)
    # os.makedirs('output', exist_ok=True)
    ```
*   **Markdown**:
    ```python
    st.markdown("## 1. Environment Setup and Dependency Installation")
    st.markdown("""
    To begin, we need to import all the necessary libraries. This includes tools for PDF processing, image manipulation, XML parsing, and data handling.
    """)
    ```
*   **Sample Financial Report Generation**: The `create_sample_financial_report` function will be used internally to generate a default PDF if no file is uploaded.
    ```python
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib import colors
    from reportlab.lib.units import inch

    @st.cache_data # Cache the function output
    def create_sample_financial_report_bytes():
        # ... (function body from notebook, adjusted to return bytes) ...
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        # ... (add content as in notebook) ...
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()
    ```
*   **Visualizing Document Page**:
    ```python
    @st.cache_data
    def display_pdf_page_as_image(pdf_file_bytes, page_number=0, width=612, height=792):
        reader = PdfReader(io.BytesIO(pdf_file_bytes))
        if page_number >= len(reader.pages):
            st.warning(f"Error: Page {page_number} not found. Document has {len(reader.pages)} pages.")
            return Image.new('RGB', (width, height), 'gray') # Return a placeholder image

        # For a true PDF to image conversion, a library like pdf2image would be needed.
        # For simulation, we create a blank image as in the notebook.
        image = Image.new('RGB', (int(width), int(height)), 'white')
        draw = ImageDraw.Draw(image)
        try:
            font = ImageFont.truetype("arial.ttf", 16) # Use a common font if available
        except IOError:
            font = ImageFont.load_default()

        draw.text((50, 50), f"Simulated content for Page {page_number + 1}", fill=(0,0,0), font=font)
        draw.text((50, 80), "See generated PDF for actual content.", fill=(0,0,0), font=font)
        return image
    ```

### 3. Simulating SmolDocling and Understanding DocTags Output

*   **Markdown**:
    ```python
    st.markdown("## 3. Simulating SmolDocling and Understanding DocTags Output")
    st.markdown("""
    Alex's core task involves integrating SmolDocling. Since SmolDocling is a specialized model (available on Hugging Face), we'll simulate its output. In a production environment, this would involve calling the actual SmolDocling API. The critical aspect is understanding its `DocTags` output format, which is an XML-like representation that captures content, structure, and crucial spatial location information for all document elements.

    Each element in `DocTags` includes bounding box coordinates, represented as $ <loc_x1><loc_y1><loc_x2><loc_y2>$. Here, $x_1$ and $y_1$ are the coordinates of the top-left corner, and $x_2$ and $y_2$ are the coordinates of the bottom-right corner of the bounding box.
    """)
    ```
*   **Code**:
    ```python
    class SmolDoclingClient:
        # ... (class definition from notebook) ...
        def process_document_page(self, pdf_file_bytes, page_number):
            # ... (function body from notebook, receives bytes) ...
            return simulated_doctags_output # Return the hardcoded XML

    # Initialize client and process (triggered by button in Streamlit)
    # smoldocling_client = SmolDoclingClient()
    # doctags_xml = smoldocling_client.process_document_page(pdf_file_bytes, page_number)
    # st.code(doctags_xml[:1000])
    ```

### 4. Parsing DocTags for Structural Elements

*   **Markdown**:
    ```python
    st.markdown("## 4. Parsing DocTags for Structural Elements")
    st.markdown("""
    The `DocTags` output is an XML-like format. Alex needs to parse this into a more manageable structure, specifically identifying tables (`otsl` tags) and general text blocks (`text` tags). We'll use `BeautifulSoup` for robust XML parsing. The bounding box information associated with each tag will be crucial for subsequent steps.
    """)
    ```
*   **Code**:
    ```python
    @st.cache_data
    def parse_doctags(doctags_xml):
        # ... (function body from notebook) ...
        return extracted_data

    # parsed_document = parse_doctags(doctags_xml)
    # if parsed_document["tables"]:
    #     st.write(f"Found {len(parsed_document['tables'])} table(s).")
    #     for i, table_info in enumerate(parsed_document["tables"]):
    #         st.dataframe(table_info["dataframe"])
    # ... (similar display for text blocks) ...
    ```

### 5. Rule-Based Extraction of Key Financial Metrics

*   **Markdown**:
    ```python
    st.markdown("## 5. Rule-Based Extraction of Key Financial Metrics")
    st.markdown("""
    Now, Alex will apply conceptual pattern matching and rule-based logic to identify and extract specific financial metrics. This involves searching for keywords and patterns within the extracted text blocks and table cells, leveraging the bounding box information for context and verification.

    For instance, to extract "Revenue," Alex might look for the word "Revenue" and its associated numerical value in the same text block or an adjacent table cell. The spatial information from `DocTags` (e.g., $ <loc_x1><loc_y1><loc_x2><loc_y2>$ for accurate data pinpointing) is vital here to ensure we are extracting the *correct* value associated with the metric.
    """)
    ```
*   **Code**:
    ```python
    @st.cache_data
    def extract_financial_metrics(parsed_document):
        # ... (function body from notebook) ...
        return extracted_metrics, extracted_elements_for_viz

    # financial_metrics, visualization_elements = extract_financial_metrics(parsed_document)
    # st.subheader("Extracted Financial Metrics")
    # st.table(pd.DataFrame([financial_metrics]))
    ```

### 6. Visualizing Extracted Data on the Document

*   **Markdown**:
    ```python
    st.markdown("## 6. Visualizing Extracted Data on the Document")
    st.markdown("""
    To provide immediate feedback and allow analysts to verify the extraction, Alex needs to visualize the extracted information directly on the original document page. This involves drawing bounding boxes around the identified tables, text blocks, and key-value pairs.

    The coordinates for these bounding boxes are obtained directly from the `DocTags` output and are crucial for correctly overlaying information on the image.
    """)
    ```
*   **Code**:
    ```python
    @st.cache_data
    def visualize_extracted_data(page_image, extracted_elements, page_width=612, page_height=792):
        # ... (function body from notebook, adjusted to receive PIL Image directly) ...
        # Ensure page_image is mutable for drawing
        if page_image.mode == 'RGB':
            draw_image = page_image.copy()
        else:
            draw_image = page_image.convert('RGB')
        
        draw = ImageDraw.Draw(draw_image)
        try:
            font = ImageFont.truetype("arial.ttf", 14)
        except IOError:
            font = ImageFont.load_default()

        # ... (draw elements as in notebook) ...
        return draw_image

    # all_elements_for_viz = []
    # ... (populate all_elements_for_viz) ...
    # visualized_image = visualize_extracted_data(page_image, all_elements_for_viz)
    # st.image(visualized_image, caption=f"Extracted Financial Data Overlay on Page {page_number + 1}")
    ```

### 7. Exporting Structured Financial Data

*   **Markdown**:
    ```python
    st.markdown("## 7. Exporting Structured Financial Data")
    st.markdown("""
    The final step for Alex's tool is to export the extracted financial data into common, machine-readable formats. This allows financial analysts to easily integrate the data into spreadsheets, databases, or other analytical tools. CSV and JSON are ideal formats for this purpose.
    """)
    ```
*   **Code**:
    ```python
    @st.cache_data
    def export_financial_data(extracted_metrics, parsed_tables):
        # ... (function body from notebook, adjusted to return string/bytes for download) ...
        # For CSV
        metrics_df = pd.DataFrame([extracted_metrics])
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

        # For JSON
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

    # csv_content, json_content = export_financial_data(financial_metrics, parsed_document["tables"])
    # st.download_button("Download CSV", csv_content, "financial_data.csv", "text/csv")
    # st.download_button("Download JSON", json_content, "financial_data.json", "application/json")
    ```

### 8. Conclusion and Future Outlook

*   **Markdown**:
    ```python
    st.markdown("## 8. Conclusion and Future Outlook")
    st.markdown("""
    Through this application, Alex has successfully developed a prototype for automated financial report data extraction using a simulated SmolDocling model. The workflow demonstrated involves:
    -   Loading and visualizing PDF financial documents.
    -   Utilizing SmolDocling's `DocTags` output to obtain a rich, multi-modal representation of document content, structure, and spatial information, including precise bounding box coordinates ($ <loc_x1><loc_y1><loc_x2><loc_y2>$).
    -   Parsing the `DocTags` to identify and structure tables and text blocks.
    -   Applying rule-based pattern matching, enhanced by spatial awareness from bounding boxes, to accurately extract key financial metrics.
    -   Visualizing the extracted data directly on the document page for verification.
    -   Exporting the structured financial data into CSV and JSON formats for downstream analysis.

    This tool significantly reduces the manual effort and potential for error in financial data extraction, allowing analysts to focus on higher-value tasks.
    """)
    ```