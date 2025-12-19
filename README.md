# QuLab: SmolDocling - An Ultra-Compact Vision-Language Model for Multi-Modal Document Conversion

![SmolDocling Logo](https://www.quantuniversity.com/assets/img/logo5.jpg)

## 🌟 Project Overview

This project, **QuLab: SmolDocling**, presents a Streamlit application designed as a prototype for automating financial data extraction from unstructured PDF documents. It simulates the capabilities of `SmolDocling`, an ultra-compact vision-language model, to convert multi-modal document content into a structured, machine-readable format called `DocTags` (XML).

As a software developer, the goal is to streamline the laborious and error-prone manual process of extracting critical financial metrics from reports. This application demonstrates an end-to-end workflow: from ingesting a PDF, simulating its processing by SmolDocling, visualizing the detected elements, extracting key financial data, and finally providing this data in easily consumable formats like CSV and JSON.

This lab project emphasizes the power of vision-language models in transforming unstructured documents into actionable intelligence, empowering financial analysts to focus on higher-value tasks rather than manual data entry.

## ✨ Features

This application offers a range of functionalities to showcase the SmolDocling workflow:

*   **PDF Document Upload**: Users can upload their own PDF financial reports for processing.
*   **Sample Document Generation**: A built-in feature to generate a sample financial report PDF on the fly, allowing immediate testing without external files.
*   **SmolDocling Simulation**: Simulates the core functionality of the SmolDocling vision-language model, demonstrating how it processes document pages.
*   **DocTags XML Output**: Generates a simulated `DocTags` XML output, a structured representation that includes content, layout, and precise bounding box (`bbox`) spatial coordinates for identified elements.
*   **Visual Document Analysis**: Overlays detected elements (text blocks, tables, key metrics) with bounding boxes and labels directly onto the document image, providing clear visual feedback of the extraction process.
*   **Structured Data Parsing**: Parses the `DocTags` XML to extract and structure content, specifically identifying tables and text blocks.
*   **Financial Metric Extraction**: Implements rule-based logic to extract key financial metrics (e.g., Total Revenue, Net Income, EPS) from the parsed tables.
*   **Interactive Data Review**: Presents extracted financial metrics and tables in an organized, interactive format within the Streamlit interface.
*   **Data Export**: Allows users to download all extracted structured data (key metrics and tables) in both CSV and JSON formats for further analysis or integration with other systems.

## 🚀 Getting Started

Follow these instructions to set up and run the application on your local machine.

### Prerequisites

*   Python 3.8+
*   `pip` (Python package installer)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/quolab-smoldocling-app.git
    cd quolab-smoldocling-app
    ```
    *(Note: Replace `your-username/quolab-smoldocling-app` with the actual repository path if it's hosted.)*

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    Create a `requirements.txt` file in the project root with the following content:
    ```
    streamlit
    pandas
    numpy
    Pillow
    beautifulsoup4
    pypdf
    reportlab
    ```
    Then install them:
    ```bash
    pip install -r requirements.txt
    ```

## 🖥️ Usage

1.  **Run the Streamlit application:**
    ```bash
    streamlit run app.py
    ```
    This command will open the application in your default web browser.

2.  **Navigate the Application:**
    *   **Introduction**: Read about the project's goals and the concept of DocTags.
    *   **Upload Document**:
        *   Either click "Use Sample Financial Report" to quickly load a pre-generated PDF.
        *   Or click "Upload PDF Financial Report" and select a PDF file from your computer.
        *   Select the page number you wish to process (default is 1).
        *   Click "Process Document". The application will simulate SmolDocling, generate DocTags, parse the content, extract metrics, and display a visual overlay on the document. You can also view the raw `DocTags` XML and extracted tables below the visualization.
    *   **Review & Export**:
        *   Here you will see the extracted key financial metrics and all identified tables in a structured format.
        *   Use the "Download Data as CSV" or "Download Data as JSON" buttons to export the extracted information.

## 📁 Project Structure

```
quolab-smoldocling-app/
├── app.py                  # Main Streamlit application file
├── requirements.txt        # Python dependencies
└── README.md               # Project README file
```

## ⚙️ Technology Stack

*   **Streamlit**: For building the interactive web application user interface.
*   **Pandas**: For data manipulation and structuring extracted table data.
*   **NumPy**: Used internally by pandas and other libraries for numerical operations.
*   **Pillow (PIL)**: For image processing, particularly for rendering PDF pages as images and drawing bounding box overlays.
*   **BeautifulSoup4 (`bs4`)**: For parsing the simulated `DocTags` XML output and navigating its structure.
*   **PyPDF (`pypdf`)**: Used for basic PDF file handling (e.g., reading page count, though actual rendering is simulated).
*   **ReportLab**: For programmatically generating the sample PDF financial report.

## 🤝 Contributing

Contributions are welcome! If you have suggestions for improvements, bug fixes, or new features, please follow these steps:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature-name`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'Add new feature'`).
5.  Push to the branch (`git push origin feature/your-feature-name`).
6.  Open a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the `LICENSE` file for details (if you have one, otherwise you might want to create one).

## 📧 Contact

For any questions or inquiries, please reach out:

*   **QuantUniversity:** [https://www.quantuniversity.com](https://www.quantuniversity.com)
*   **Your Name/Email (Optional):** [your.email@example.com](mailto:your.email@example.com)
*   **GitHub Profile (Optional):** [https://github.com/your-username](https://github.com/your-username)


## License

## QuantUniversity License

© QuantUniversity 2025  
This notebook was created for **educational purposes only** and is **not intended for commercial use**.  

- You **may not copy, share, or redistribute** this notebook **without explicit permission** from QuantUniversity.  
- You **may not delete or modify this license cell** without authorization.  
- This notebook was generated using **QuCreate**, an AI-powered assistant.  
- Content generated by AI may contain **hallucinated or incorrect information**. Please **verify before using**.  

All rights reserved. For permissions or commercial licensing, contact: [info@quantuniversity.com](mailto:info@quantuniversity.com)
