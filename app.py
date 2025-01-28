from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify
from fpdf import FPDF
import json
import csv
import os
from zipfile import ZipFile

app = Flask(__name__)

# Route to render the Add Course page
@app.route('/add-course')
def add_course():
    return render_template('add_course.html')

@app.route('/save-course', methods=['POST'])
def save_course():
    course_name = request.form.get('course_name')
    if not course_name:
        return "Course name is required!", 400

    # Load existing courses
    courses = load_courses()

    # Add the new course to the list
    courses.append({'name': course_name})

    # Save updated courses
    save_courses(courses)

    # Redirect to the home page
    return redirect('/')

# Helper function to load courses from a file
def load_courses():
    if os.path.exists('courses.json'):
        with open('courses.json', 'r') as file:
            return json.load(file)
    return []

# Helper function to save courses to a file
def save_courses(courses):
    with open('courses.json', 'w') as file:
        json.dump(courses, file)

# Route to save adjusted positions and font settings
@app.route('/save-positions', methods=['POST'])
def save_positions():
    positions = request.json
    with open('positions.json', 'w') as file:
        json.dump(positions, file)
    return jsonify({'status': 'success'})

# Route to save font settings
@app.route('/save-font-settings', methods=['POST'])
def save_font_settings():
    font_settings = request.json
    try:
        # Load existing positions.json
        with open('positions.json', 'r') as file:
            positions = json.load(file)

        # Update with font settings
        positions['font_size'] = font_settings.get('font_size', 16)
        positions['font_style'] = font_settings.get('font_style', 'Arial')

        # Save updated positions
        with open('positions.json', 'w') as file:
            json.dump(positions, file)

        return jsonify({'message': 'Font settings saved successfully!'})
    except Exception as e:
        return jsonify({'message': f'Error saving font settings: {str(e)}'}), 500

# Route for certificate preview
@app.route('/certificate-preview', methods=['POST'])
def certificate_preview():
    user_name = request.form.get('user_name')
    course_duration = request.form.get('course_duration')
    certificate_id = request.form.get('certificate_id')
    course_name = request.form.get('course_name')  # Hidden field in course_form.html

    return render_template(
        'certificate_preview.html',
        course_name=course_name,
        user_name=user_name,
        course_duration=course_duration,
        certificate_id=certificate_id
    )

# Route to generate and download the PDF
@app.route('/download-pdf', methods=['POST'])
def download_pdf():
    try:
        # Get form data
        user_name = request.form.get('user_name', 'User Name')
        course_duration = request.form.get('course_duration', 'Duration')
        certificate_id = request.form.get('certificate_id', 'Certificate ID')

        # Load saved positions and font settings
        with open('positions.json', 'r') as file:
            positions = json.load(file)

        # Generate the certificate PDF
        pdf = FPDF(orientation='L', unit='mm', format='A4')
        pdf.add_page()
        pdf.image('static/certificate-template.jpg', x=0, y=0, w=297, h=210)  # A4 size in landscape

        # Helper function to add text with individual font and size
        def add_text(pdf, text, position):
            font_size = position.get('fontSize', '16px').replace('px', '')
            font_style = position.get('fontStyle', 'Arial, sans-serif')

            # Ensure font size is valid
            try:
                font_size = int(font_size)
            except ValueError:
                font_size = 16  # Default font size

            # Map CSS font names to FPDF-compatible fonts
            font_map = {
                'Arial, sans-serif': 'Arial',
                'Times New Roman, serif': 'Times',
                'Courier New, monospace': 'Courier',
                'CooperBlkBT-Italic': 'CooperBlkBT-Italic',
                'CooperBlkBT-Italic': 'CooperBlkBT-Italic',
                'CooperBlkBT-Regular': 'CooperBlkBT-Regular',
                'CooperLtBT-Bold': 'CooperLtBT-Bold',
                'CooperLtBT-BoldItalic': 'CooperLtBT-BoldItalic',
                'CooperLtBT-Italic': 'CooperLtBT-Italic',
                'CooperLtBT-Regular': 'CooperLtBT-Regular',
                'CooperMdBT-Italic': 'CooperMdBT-Italic',
                'CooperMdBT-Regular': 'CooperMdBT-Regular'
                }
            font_style = font_map.get(font_style, 'Arial')  # Default to Arial if font not mapped

            # Set font and add text
            pdf.set_font(font_style, size=font_size)
            left = float(position['left'].replace('px', '')) * 0.264583  # Convert px to mm
            top = float(position['top'].replace('px', '')) * 0.264583    # Convert px to mm
            pdf.text(x=left, y=top, txt=text)

        # Add elements to the certificate
        add_text(pdf, user_name, positions.get('name', {}))
        add_text(pdf, course_duration, positions.get('duration', {}))
        add_text(pdf, certificate_id, positions.get('certificate_id', {}))

        # Save the PDF
        pdf_file = 'generated_certificate.pdf'
        pdf.output(pdf_file)

        return send_file(pdf_file, as_attachment=True)

    except Exception as e:
        print(f"Error in download_pdf: {e}")
        return jsonify({'error': str(e)}), 500


# Route for the initial page
@app.route('/')
def index():
    courses = load_courses()  # Load courses from the file
    return render_template('index.html', courses=courses)

# Route for handling course selection and form submission
@app.route('/course/<course_name>', methods=['GET', 'POST'])
def course_page(course_name):
    if request.method == 'GET':
        return render_template('course_form.html', course_name=course_name)
    elif request.method == 'POST':
        return certificate_preview()

# Route to create a new course
@app.route('/create-course', methods=['POST'])
def create_course():
    course_name = request.form.get('course_name')
    course_description = request.form.get('course_description')

    # Add new course to the list
    courses = load_courses()
    courses.append({
        'name': course_name,
        'description': course_description
    })
    save_courses(courses)  # Save the updated list of courses

    # Redirect to home page after course creation
    return redirect('/')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload-csv', methods=['POST'])
def upload_csv():
    if 'csv_file' not in request.files:
        return redirect(request.url)
    
    file = request.files['csv_file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Process CSV file for bulk certificate generation
        with open(file_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                user_name = row['user_name']
                course_duration = row['course_duration']
                certificate_id = row['certificate_id']

                # Call the function to generate certificates for each row
                # You can add logic to save or generate the certificates here
                print(f'Generating certificate for {user_name} ({course_duration}, {certificate_id})')

        return 'Bulk certificate generation is successful!'

    return 'Invalid file format. Please upload a CSV file.'

if __name__ == '__main__':
    app.run(debug=True)
