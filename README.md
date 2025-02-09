# Certificate Generator

A Flask-based web application for generating customizable certificates with dynamic text positioning and font styling.

## Features

- Upload and manage certificate templates (JPG/PDF)
- Drag-and-drop interface for text positioning
- Customizable font styles and sizes
- Bulk certificate generation using CSV upload
- Real-time certificate preview
- PDF certificate generation
- Multiple font family support (Cooper font family)
- Responsive design

## Prerequisites

- Python 3.7+
- Flask
- ReportLab
- PyPDF2
- Pandas
- Additional Python packages (see requirements.txt)

## Project Structure

```
certificate-generator/
├── static/
│   ├── templates/     # Certificate templates
│   └── fonts/         # Font files
├── templates/
│   ├── index.html            # Course selection page
│   ├── course_form.html      # Certificate details form
│   └── certificate_preview.html   # Preview and positioning
├── app.py                    # Main Flask application
├── courses.json             # Course data storage
└── positions.json           # Text position configurations
```

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd certificate-generator
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Set up the required directories:
```bash
mkdir -p static/templates static/fonts
```

5. Place your Cooper font family files in the `static/fonts` directory:
- CooperBlkBT-Italic.ttf
- CooperBlkBT-Regular.ttf
- CooperLtBT-Bold.ttf
- CooperLtBT-BoldItalic.ttf
- CooperLtBT-Italic.ttf
- CooperLtBT-Regular.ttf
- CooperMdBT-Regular.ttf

## Usage

1. Start the Flask application:
```bash
python app.py
```

2. Access the application at `http://localhost:5000`

3. Upload Certificate Templates:
   - Name your JPG template as `certificate-template.jpg`
   - Name your PDF template as `certificate-template.pdf`
   - Use the template upload form to upload both files

4. Generate Individual Certificates:
   - Enter certificate details (name, duration, ID)
   - Use the drag-and-drop interface to position text
   - Customize font styles and sizes
   - Preview the certificate
   - Download the generated PDF

5. Bulk Certificate Generation:
   - Prepare a CSV file with columns:
     - user_name
     - course_duration
     - certificate_id
   - Upload the CSV file
   - Download the ZIP file containing all generated certificates

## API Endpoints

- `GET /`: Home page with course selection
- `GET /course/<course_name>`: Course-specific certificate form
- `POST /upload-templates`: Upload certificate templates
- `POST /save-positions`: Save text element positions
- `GET /get-positions`: Retrieve current text positions
- `POST /download-pdf`: Generate and download certificate PDF
- `POST /upload-csv`: Bulk certificate generation
- `POST /delete-templates`: Delete existing templates
- `GET /check-templates`: Check template existence

## File Requirements

### Templates
- JPG Template: `certificate-template.jpg`
- PDF Template: `certificate-template.pdf`

### CSV Format for Bulk Generation
```csv
user_name,course_duration,certificate_id
John Doe,6 Months,CERT001
Jane Smith,3 Months,CERT002
```

## Configuration Files

### positions.json
Stores the position and styling information for certificate text elements:
```json
{
  "name": {
    "top": "280",
    "left": "442",
    "fontSize": "46",
    "fontStyle": "CooperBlkBT-Italic"
  },
  "certificate_id": {
    "top": "600",
    "left": "160",
    "fontSize": "16",
    "fontStyle": "CooperBlkBT-Italic"
  },
  "course_duration": {
    "top": "600",
    "left": "850",
    "fontSize": "16",
    "fontStyle": "CooperLtBT-Italic"
  }
}
```

## Error Handling

- Template validation for file types and names
- Error messages for upload failures
- Validation for CSV format and content
- Error handling for PDF generation

## Development

To run the application in debug mode:
```bash
export FLASK_ENV=development
export FLASK_DEBUG=1
python app.py
```

## Notes

- The application uses the Cooper font family for certificate text
- All positions are relative to the template dimensions (1084x799)
- Font sizes are automatically adjusted for the certificate name to fit within bounds
- The preview interface provides real-time visualization of text positioning

## Security Considerations

- Input validation for all form fields
- Secure file handling for uploads
- File type restrictions
- Error handling for malformed requests

## Browser Compatibility

Tested and supported on:
- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+

## License

This project is licensed under the MIT License - see the LICENSE file for details.