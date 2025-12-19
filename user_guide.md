id: 6945a5a0313de3de69bd8a19_user_guide
summary: SmolDocling: An ultra-compact vision-language model for end-to-end multi-modal document conversion User Guide
feedback link: https://docs.google.com/forms/d/e/1FAIpQLSfWkOK-in_bMMoHSZfcIvAeO58PAH9wrDqcxnJABHaxiDqhSA/viewform?usp=sf_link
environments: Web
status: Published
# Automating Financial Report Data Extraction with SmolDocling

## 1. Introduction to SmolDocling for Financial Data Extraction
Duration: 00:05:00

<aside class="positive">
Welcome to this Codelab! We'll explore how the SmolDocling application can revolutionize financial data extraction.
</aside>

As a Software Developer at a fast-paced FinTech firm, you understand the critical need for efficient and accurate data. Manually extracting key financial metrics from documents like earnings reports and 10-K filings is a significant bottleneck. It's time-consuming, prone to errors, and delays crucial analysis.

This application provides a powerful solution by automating this process. It takes unstructured PDF financial reports, intelligently identifies critical financial metrics (such as revenue, net income, and Earnings Per Share), and presents them in a structured, easily consumable format. This frees up financial analysts to focus on deeper insights rather than tedious data entry.

At the core of this application is **SmolDocling**, an ultra-compact vision-language model. SmolDocling is designed for end-to-end multi-modal document conversion. Its unique strength lies in generating `DocTags`, an output that provides a rich, structured representation of document content, layout, and crucially, spatial location. This allows us to precisely pinpoint and extract the required financial data, transforming unstructured PDFs into actionable intelligence.

### Understanding DocTags and Bounding Boxes

One of the most powerful features of `DocTags` is its ability to provide spatial coordinates for every identified element within the document. This is achieved through **bounding boxes**.

A bounding box is a rectangular coordinate that defines the location and size of an element (like a title, text block, or table) on a page. Each bounding box is represented by four values:

$$ <loc_{x1}><loc_{y1}><loc_{x2}><loc_{y2}> $$

Where:
*   $x_1$ and $y_1$ are the coordinates of the **top-left corner** of the bounding box.
*   $x_2$ and $y_2$ are the coordinates of the **bottom-right corner** of the bounding box.

These coordinates allow the application to visually highlight where specific information was found on the original document, providing a clear audit trail and enhancing user trust in the extracted data.

## 2. Upload and Process Financial Report
Duration: 00:07:00

On the "Upload Document" page, you can initiate the process of converting your unstructured financial report into structured data.

### Inputting Your Document

You have two options to provide a document to the application:

1.  **Upload PDF Financial Report**: Click the "Browse files" button (or similar, depending on your browser) to upload a PDF file from your local system. Once selected, the file will be uploaded.
2.  **Use Sample Financial Report**: If you don't have a specific PDF on hand or want to quickly see the application in action, click the "Use Sample Financial Report" button. This will load a pre-generated sample PDF directly into the application.

After either uploading your own file or loading the sample, you will see a success message indicating the file is ready for processing.

<aside class="negative">
If you encounter issues with a custom PDF, try using the sample report first to ensure the core functionality is working as expected. This application is a simulation, and it's optimized for the structure of its internal sample.
</aside>

### Processing the Document

Once a document is loaded (either uploaded or from the sample), follow these steps:

1.  **Select Page Number**: The application allows you to select a specific page from the document for processing. For this simulation, the default is page 1, which is where the relevant financial data is located in the sample report.
2.  **Process Document**: Click the "Process Document" button. The application will display a "Running SmolDocling Simulation..." spinner, indicating that the multi-modal document conversion is underway.

This "Process Document" step involves several crucial actions:

*   **Image Preview**: The application first converts the selected PDF page into a visual image. This image is displayed under "Document Visualization".
*   **DocTags Generation**: Next, the simulated SmolDocling model processes this image and generates the `DocTags` XML output. This XML describes all detected elements (text blocks, tables, titles) along with their content and precise bounding box coordinates.
*   **Data Parsing**: The `DocTags` XML is then parsed. This means the raw XML structure is converted into easily manageable data structures within the application, separating text blocks from tabular data.
*   **Metric Extraction**: Using rule-based logic, the application then scans the parsed tables and text to identify key financial metrics (like "Total Revenue", "Net Income", "EPS") and their corresponding values.
*   **Visualization**: The bounding box coordinates from the `DocTags` are used to overlay visual highlights (colored rectangles and labels) directly onto the document image, showing exactly where the extracted information was found. This helps verify the extraction.
*   **Export Preparation**: Finally, the extracted data is prepared for export in common formats like CSV and JSON.

After processing is complete, you will see a "Processing Complete!" message.

### Reviewing the Processed Output

Below the "Document Visualization" section, you'll find the raw and parsed outputs:

*   **DocTags Output (Excerpt)**: This section displays the simulated XML output generated by SmolDocling. Pay close attention to the `bbox` attributes for each element, as these are the bounding boxes we discussed earlier.
    ```xml
    <root>
        <document_meta>
            <title bbox="60 60 400 90">FinTech Corp Financial Report 2023</title>
            <page_num>1</page_num>
        </document_meta>
        <content>
            <text bbox="60 110 550 180">
                FinTech Corp delivered robust performance in fiscal year 2023.
                ...
            </text>
            <otsl bbox="60 200 550 350">
                <header>
                    <cell bbox="60 200 250 230">Metric</cell>
                    <cell bbox="250 200 550 230">2023 (in Millions)</cell>
                </header>
                ...
            </otsl>
            ...
        </content>
    </root>
    ```
    This XML structure is a direct result of SmolDocling's multi-modal analysis, combining visual layout (bounding boxes) with textual content.
*   **Extracted Tables**: Here, any tables identified and parsed from the `DocTags` XML are displayed in an interactive dataframe format. You can see how the raw tabular data from the PDF has been converted into a structured, usable format.

## 3. Review & Export Data
Duration: 00:03:00

Navigate to the "Review & Export" page using the sidebar. This page provides a clean summary of the extracted financial data and options to download it for further analysis.

<aside class="negative">
If you see a warning "No data processed yet," please go back to the "Upload Document" page and process a file first.
</aside>

### Reviewing Extracted Information

On this page, the application neatly presents the two main types of extracted financial data:

*   **Key Financial Metrics**: This section displays a table of the specific financial metrics (e.g., Total Revenue, Net Income, EPS) that were automatically identified and extracted by the application, along with their corresponding values. This is the "actionable intelligence" you wanted to derive.
*   **Extracted Tables**: Here, you'll find all the full tables that SmolDocling identified and parsed from the document. This allows you to review the complete tabular data, beyond just the key metrics, ensuring all relevant information is captured.

### Exporting Your Data

The ultimate goal of automated extraction is to get the data into a format that can be easily used by other tools or systems. This application provides two standard export formats:

*   **Download Data as CSV**: Click this button to download a Comma Separated Values (CSV) file. This format is ideal for importing into spreadsheets (like Excel or Google Sheets) or for use in basic data analysis scripts. The CSV will combine the key metrics and the contents of all extracted tables into a single, unified file.
*   **Download Data as JSON**: Click this button to download a JavaScript Object Notation (JSON) file. JSON is a lightweight, human-readable data interchange format often used in web applications, APIs, and more complex data processing pipelines. The JSON file will structure the key metrics and tables hierarchically.

<aside class="positive">
By leveraging SmolDocling and its `DocTags` output, this application transforms manual, error-prone data entry into a streamlined, automated process, providing financial analysts with structured data at their fingertips.
</aside>
