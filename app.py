from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify
from fpdf import FPDF
import json
import os

app = Flask(__name__)

class CustomPDF(FPDF):
    def __init__(self):
        super().__init__(orientation='L', unit='mm', format='A4')
        # Register custom fonts from static/fonts directory
        font_dir = os.path.join(os.path.dirname(__file__), 'static', 'fonts')
        
        self.custom_fonts = {
            'CooperBlkBT-Italic': os.path.join(font_dir, 'CooperBlkBT-Italic.ttf'),
            'CooperBlkBT-Regular': os.path.join(font_dir, 'CooperBlkBT-Regular.ttf'),
            'CooperLtBT-Bold': os.path.join(font_dir, 'CooperLtBT-Bold.ttf'),
            'CooperLtBT-BoldItalic': os.path.join(font_dir, 'CooperLtBT-BoldItalic.ttf'),
            'CooperLtBT-Italic': os.path.join(font_dir, 'CooperLtBT-Italic.ttf'),
            'CooperLtBT-Regular': os.path.join(font_dir, 'CooperLtBT-Regular.ttf'),
            'CooperMdBT-Regular': os.path.join(font_dir, 'CooperMdBT-Regular.ttf')
        }
        
        # Register all custom fonts
        for font_name, font_path in self.custom_fonts.items():
            try:
                self.add_font(font_name, '', font_path, uni=True)
            except Exception as e:
                print(f"Error loading font {font_name}: {e}")

    def text(self, x, y, txt):
        # Override text method to handle encoding
        try:
            if isinstance(txt, bytes):
                txt = txt.decode('utf-8')
            elif isinstance(txt, str):
                txt = txt.encode('latin-1', errors='replace').decode('latin-1')
            super().text(x, y, txt)
        except Exception as e:
            print(f"Error writing text: {e}")
            super().text(x, y, '?')  # Fallback for problematic characters


def load_courses():
    if os.path.exists('courses.json'):
        with open('courses.json', 'r') as file:
            return json.load(file)
    return []

def save_courses(courses):
    with open('courses.json', 'w') as file:
        json.dump(courses, file)

def load_positions():
    try:
        with open('positions.json', 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        default_positions = {
            'name': {
                'top': '280',
                'left': '442',
                'fontSize': '46',
                'fontStyle': 'Arial'
            },
            'certificate_id': {
                'top': '600',
                'left': '160',
                'fontSize': '16',
                'fontStyle': 'Arial'
            },
            'duration': {
                'top': '600',
                'left': '850',
                'fontSize': '16',
                'fontStyle': 'Arial'
            }
        }
        save_positions(default_positions)
        return default_positions
def save_positions(positions):
    # Clean and validate the positions data
    cleaned_positions = {}
    for key, value in positions.items():
        cleaned_positions[key] = {
            'top': str(value.get('top', '0')).replace('px', ''),
            'left': str(value.get('left', '0')).replace('px', ''),
            'fontSize': str(value.get('fontSize', '16')).replace('px', ''),
            'fontStyle': value.get('fontStyle', 'Arial')
        }
    
    with open('positions.json', 'w') as file:
        json.dump(cleaned_positions, file, indent=2)
        
def save_courses(courses):
    with open('courses.json', 'w') as file:
        json.dump(courses, file)
@app.route('/save-positions', methods=['POST'])

def save_positions_route():
    try:
        positions = request.json
        save_positions(positions)
        return jsonify({'status': 'success', 'message': 'Positions saved successfully'})
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
    def __init__(self):
        super().__init__(orientation='L', unit='mm', format='A4')
        # Register custom fonts from static/fonts directory
        font_dir = os.path.join(os.path.dirname(__file__), 'static', 'fonts')
        
        self.custom_fonts = {
            'CooperBlkBT-Italic': os.path.join(font_dir, 'CooperBlkBT-Italic.ttf'),
            'CooperBlkBT-Regular': os.path.join(font_dir, 'CooperBlkBT-Regular.ttf'),
            'CooperLtBT-Bold': os.path.join(font_dir, 'CooperLtBT-Bold.ttf'),
            'CooperLtBT-BoldItalic': os.path.join(font_dir, 'CooperLtBT-BoldItalic.ttf'),
            'CooperLtBT-Italic': os.path.join(font_dir, 'CooperLtBT-Italic.ttf'),
            'CooperLtBT-Regular': os.path.join(font_dir, 'CooperLtBT-Regular.ttf'),
            'CooperMdBT-Regular': os.path.join(font_dir, 'CooperMdBT-Regular.ttf')
        }
        
        # Register all custom fonts
        for font_name, font_path in self.custom_fonts.items():
            try:
                self.add_font(font_name, '', font_path, uni=True)
            except Exception as e:
                print(f"Error loading font {font_name}: {e}")

    def text(self, x, y, txt):
        # Override text method to handle encoding
        try:
            if isinstance(txt, bytes):
                txt = txt.decode('utf-8')
            elif isinstance(txt, str):
                txt = txt.encode('latin-1', errors='replace').decode('latin-1')
            super().text(x, y, txt)
        except Exception as e:
            print(f"Error writing text: {e}")
            super().text(x, y, '?')  # Fallback for problematic characters
    try:
        # Get form data
        user_name = request.form.get('user_name', 'user_name')
        course_duration = request.form.get('course_duration', 'course_duration')
        certificate_id = request.form.get('certificate_id', 'certificate_id')

        # Load saved positions
        positions = load_positions()

        # Initialize PDF with custom fonts
        pdf = CustomPDF()
        pdf.add_page()
        pdf.image('static/certificate-template.jpg', x=0, y=0, w=297, h=210)
        
        
        def add_text(pdf, text, position_data, element_type): # Updated font mapping with the available Cooper fonts
            font_map = {
        'Arial': 'Arial',
        'Times New Roman': 'Times',
        'CooperBlackItalic': 'CooperBlkBT-Italic',
        'CooperBlackRegular': 'CooperBlkBT-Regular',
        'CooperLightBold': 'CooperLtBT-Bold',
        'CooperLightBoldItalic': 'CooperLtBT-BoldItalic',
        'CooperLightItalic': 'CooperLtBT-Italic',
        'CooperLightRegular': 'CooperLtBT-Regular',
        'CooperMediumRegular': 'CooperMdBT-Regular'
    }


            # Get font size (remove 'px' if present and convert to integer)
            font_size = position_data.get('fontSize', '16')
            if isinstance(font_size, str):
                font_size = font_size.replace('px', '')
            font_size = int(float(font_size))

            # Get font style (clean up font name)
            font_style = position_data.get('fontStyle', 'Arial')
            if isinstance(font_style, str):
                font_style = font_style.split(',')[0].strip().replace('"', '')
            font_name = font_map.get(font_style, 'Arial')
             # Set font
            try:
                pdf.set_font(font_name, size=font_size)
            except RuntimeError as e:
                print(f"Font error: {e}. Falling back to Arial")
                pdf.set_font('Arial', size=font_size)

            # Get position values (remove 'px' if present and convert to float)
            left = position_data.get('left', '0')
            top = position_data.get('top', '0')
            if isinstance(left, str):
                left = left.replace('px', '')
            if isinstance(top, str):
                top = top.replace('px', '')
            left = float(left)
            top = float(top)

            # Template and PDF dimensions
            template_width = 1084
            template_height = 799
            pdf_width = 297
            pdf_height = 210

            # Calculate scaled positions
            x = (left / template_width) * pdf_width
            y = (top / template_height) * pdf_height

            # Add text to PDF
            pdf.set_text_color(0, 0, 0)  # Set text color to black
            pdf.text(x=x, y=y, txt=str(text))

        # Add elements to the PDF with proper position data
        name_pos = positions.get('name', {})
        cert_id_pos = positions.get('certificate_id', {})  # Note the hyphen
        duration_pos = positions.get('course_duration', {})

        # Add each text element
        add_text(pdf, user_name, name_pos, 'name')
        add_text(pdf, certificate_id, cert_id_pos, 'certificate_id')
        add_text(pdf, course_duration, duration_pos, 'duration')

        # Save and send PDF
        pdf_file = 'generated_certificate.pdf'
        pdf.output(pdf_file)

        return send_file(pdf_file, as_attachment=True)

    except Exception as e:
        print(f"Error in download_pdf: {e}")
        return jsonify({'error': str(e)}), 500
@app.route('/')
def index():
    courses = load_courses()
    return render_template('index.html', courses=courses)

@app.route('/course/<course_name>', methods=['GET', 'POST'])
def course_page(course_name):
    if request.method == 'GET':
        return render_template('course_form.html', course_name=course_name)
    elif request.method == 'POST':
        return certificate_preview()

@app.route('/certificate-preview', methods=['POST'])
def certificate_preview():
    user_name = request.form.get('user_name')
    course_duration = request.form.get('course_duration')
    certificate_id = request.form.get('certificate_id')
    course_name = request.form.get('course_name')

    return render_template(
        'certificate_preview.html',
        course_name=course_name,
        user_name=user_name,
        course_duration=course_duration,
        certificate_id=certificate_id
    )

if __name__ == '__main__':
    # Create necessary directories if they don't exist
    os.makedirs('static/fonts/CooperBlackItalic', exist_ok=True)
    
    # Create empty positions.json if it doesn't exist
    if not os.path.exists('positions.json'):
        default_positions = {
            'name': {'top': '280px', 'left': '442px', 'fontSize': '46px', 'fontStyle': 'CooperBlackItalic'},
            'certificate_id': {'top': '600px', 'left': '160px', 'fontSize': '16px', 'fontStyle': 'CooperBlackItalic'},
            'duration': {'top': '600px', 'left': '850px', 'fontSize': '16px', 'fontStyle': 'CooperBlackItalic'}
        }
        with open('positions.json', 'w') as file:
            json.dump(default_positions, file)
    
    app.run(debug=True)