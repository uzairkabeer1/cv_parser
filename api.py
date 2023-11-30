from flask import Flask, request
from werkzeug.utils import secure_filename
from pyresparser import ResumeParser
import shutil
import os

app = Flask(__name__)

def format_resume_data(resume_data):
    formatted_data = {
        'Personal Information': {
            'Name': resume_data['name'],
            'Email': resume_data['email'],
            'Mobile Number': resume_data['mobile_number']
        },
        'Education': {
            'Degree': ', '.join(resume_data['degree']) if resume_data['degree'] else 'Not Available',
            'College Name': resume_data.get('college_name', 'Not Available')
        },
        'Professional Experience': {
            'Designation': ', '.join(resume_data['designation']) if resume_data['designation'] else 'Not Available',
            'Companies Worked At': ', '.join(resume_data['company_names']),
            'Details': ' | '.join(resume_data['experience'])
        },
        'Skills': ', '.join(resume_data['skills']),
        'Additional Information': {
            'Number of Pages in Resume': resume_data['no_of_pages'],
            'Total Experience (years)': resume_data['total_experience']
        }
    }
    return formatted_data
   

def parse_and_format_resume(file_path):
    resume_data = ResumeParser(file_path).get_extracted_data()
    formatted_data = format_resume_data(resume_data)
    return formatted_data

@app.route('/testing/', methods=['GET'])
def testing():
    return {"message": "Hello World"}

@app.route('/uploadresume/', methods=['POST'])
def upload_resume():
    try:
        if 'file' not in request.files:
            return {"error": "No file part"}
        file = request.files['file']
        if file.filename == '':
            return {"error": "No selected file"}
        
        temp_file_path = f"temp_{secure_filename(file.filename)}"
        file.save(temp_file_path)

        formatted_resume_data = parse_and_format_resume(temp_file_path)

        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

        return formatted_resume_data
    except Exception as e:
        return {"error": str(e)}

if __name__ == '__main__':
    app.run(debug=True)
