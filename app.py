from flask import Flask, render_template, request, send_file, jsonify
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import json
import os
import pandas as pd
from datetime import datetime
import uuid

app = Flask(__name__)

# Register fonts
def register_fonts():
    font_dir = os.path.join(app.root_path, 'static', 'fonts')
    fonts = {
        'CooperBlkBT-Italic': 'CooperBlkBT-Italic.ttf',
        'CooperBlkBT-Regular': 'CooperBlkBT-Regular.ttf',
        'CooperLtBT-Bold': 'CooperLtBT-Bold.ttf',
        'CooperLtBT-BoldItalic': 'CooperLtBT-BoldItalic.ttf',
        'CooperLtBT-Italic': 'CooperLtBT-Italic.ttf',
        'CooperLtBT-Regular': 'CooperLtBT-Regular.ttf',
        'CooperMdBT-Regular': 'CooperMdBT-Regular.ttf'
    }
    
    for font_name, font_file in fonts.items():
        font_path = os.path.join(font_dir, font_file)
        try:
            pdfmetrics.registerFont(TTFont(font_name, font_path))
        except Exception as e:
            print(f"Error registering font {font_name}: {e}")

# Load font mapping
FONT_MAPPING = {
    'Arial': 'Helvetica',
    'Times New Roman': 'Times-Roman',
    'CooperBlkBT-Italic': 'CooperBlkBT-Italic',
    'CooperBlkBT-Regular': 'CooperBlkBT-Regular',
    'CooperLtBT-Bold': 'CooperLtBT-Bold',
    'CooperLtBT-BoldItalic': 'CooperLtBT-BoldItalic',
    'CooperLtBT-Italic': 'CooperLtBT-Italic',
    'CooperLtBT-Regular': 'CooperLtBT-Regular',
    'CooperMdBT-Regular': 'CooperMdBT-Regular'
}

def load_courses():
    if os.path.exists('courses.json'):
        with open('courses.json', 'r') as file:
            return json.load(file)
    return []

def save_courses(courses):
    with open('courses.json', 'w') as file:
        json.dump(courses, file, indent=2)

def load_positions():
    try:
        with open('positions.json', 'r') as file:
            positions = json.load(file)
            # Ensure fontSize is stored as a number without 'px'
            for element in positions.values():
                element['fontSize'] = str(element.get('fontSize', '16')).replace('px', '')
            return positions
    except (FileNotFoundError, json.JSONDecodeError):
        default_positions = {
            'name': {
                'top': '280',
                'left': '442',
                'fontSize': '46',
                'fontStyle': 'CooperBlkBT-Italic'
            },
            'certificate_id': {
                'top': '600',
                'left': '160',
                'fontSize': '16',
                'fontStyle': 'CooperBlkBT-Italic'
            },
            'course_duration': {
                'top': '600',
                'left': '850',
                'fontSize': '16',
                'fontStyle': 'CooperLtBT-Italic'
            }
        }
        save_positions(default_positions)
        return default_positions

def save_positions(positions):
    cleaned_positions = {}
    for key, value in positions.items():
        cleaned_positions[key] = {
            'top': str(value.get('top', '0')).replace('px', ''),
            'left': str(value.get('left', '0')).replace('px', ''),
            'fontSize': str(value.get('fontSize', '16')).replace('px', ''),
            'fontStyle': value.get('fontStyle', 'CooperBlkBT-Italic')
        }
    
    with open('positions.json', 'w') as file:
        json.dump(cleaned_positions, file, indent=2)
def generate_certificate(user_name, course_duration, certificate_id, positions, output_path):
    # Get page dimensions for landscape orientation
    page_width, page_height = landscape(letter)
    
    # Create the canvas with landscape orientation
    c = canvas.Canvas(output_path, pagesize=landscape(letter))
    
    # Draw the certificate template
    template_path = os.path.join('static', 'certificate-template.jpg')
    c.drawImage(template_path, 0, 0, page_width, page_height)
    
    # Function to convert web coordinates to PDF coordinates
    def convert_coordinates(web_x, web_y, web_width=1084, web_height=799):
        pdf_x = (float(web_x) / web_width) * page_width
        # Invert Y coordinate for PDF
        pdf_y = page_height - ((float(web_y) / web_height) * page_height)
        return pdf_x, pdf_y
    
    # Add text elements
    for elem_id, content in {
        'name': user_name,
        'certificate_id': certificate_id,
        'course_duration': course_duration
    }.items():
        if elem_id in positions:
            pos = positions[elem_id]
            x, y = convert_coordinates(pos['left'], pos['top'])
            
            # Get font details and ensure fontSize is a number
            font_name = FONT_MAPPING.get(pos['fontStyle'].strip("'"), 'Helvetica')
            font_size = float(str(pos['fontSize']).replace('px', ''))
            
            try:
                c.setFont(font_name, font_size)
                c.drawString(x, y, str(content))
            except Exception as e:
                print(f"Error with font {font_name}: {e}")
                c.setFont('Helvetica', font_size)
                c.drawString(x, y, str(content))
    
    c.save()


@app.route('/')
def index():
    courses = load_courses()
    return render_template('index.html', courses=courses)

@app.route('/save-positions', methods=['POST'])
def save_positions_route():
    try:
        positions = request.json
        save_positions(positions)
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/get-positions', methods=['GET'])
def get_positions():
    try:
        positions = load_positions()
        return jsonify(positions)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download-pdf', methods=['POST'])
def download_pdf():
    try:
        user_name = request.form.get('user_name', '')
        course_duration = request.form.get('course_duration', '')
        certificate_id = request.form.get('certificate_id', '')
        
        positions = load_positions()
        output_path = 'generated_certificate.pdf'
        
        generate_certificate(user_name, course_duration, certificate_id, positions, output_path)
        
        return send_file(output_path, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/upload-csv', methods=['POST'])
def upload_csv():
    if 'csv_file' not in request.files:
        return 'No file uploaded', 400
    
    file = request.files['csv_file']
    if file.filename == '' or not file.filename.endswith('.csv'):
        return 'Invalid file', 400
    
    try:
        # Create output directory
        output_dir = os.path.join('static', 'certificates', 
                                datetime.now().strftime('%Y%m%d_%H%M%S'))
        os.makedirs(output_dir, exist_ok=True)
        
        # Read CSV and generate certificates
        df = pd.read_csv(file)
        positions = load_positions()
        
        for _, row in df.iterrows():
            output_path = os.path.join(output_dir, f"certificate_{uuid.uuid4()}.pdf")
            generate_certificate(
                row.get('user_name', ''),
                row.get('course_duration', ''),
                row.get('certificate_id', ''),
                positions,
                output_path
            )
        
        return f'Certificates generated in {output_dir}', 200
    except Exception as e:
        return f'Error generating certificates: {str(e)}', 500

@app.route('/course/<course_name>', methods=['GET', 'POST'])
def course_page(course_name):
    if request.method == 'GET':
        return render_template('course_form.html', course_name=course_name)
    return certificate_preview()

@app.route('/certificate-preview', methods=['POST'])
def certificate_preview():
    return render_template(
        'certificate_preview.html',
        user_name=request.form.get('user_name'),
        course_duration=request.form.get('course_duration'),
        certificate_id=request.form.get('certificate_id'),
        course_name=request.form.get('course_name')
    )

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('static/fonts', exist_ok=True)
    os.makedirs('static/certificates', exist_ok=True)
    
    # Register fonts
    register_fonts()
    
    # Initialize positions.json if it doesn't exist
    if not os.path.exists('positions.json'):
        default_positions = {
            'name': {'top': '280', 'left': '442', 'fontSize': '46', 'fontStyle': 'CooperBlkBT-Italic'},
            'certificate_id': {'top': '600', 'left': '160', 'fontSize': '16', 'fontStyle': 'CooperBlkBT-Italic'},
            'course_duration': {'top': '600', 'left': '850', 'fontSize': '16', 'fontStyle': 'CooperBlkBT-Italic'}
        }
        save_positions(default_positions)
    
    app.run(debug=True)