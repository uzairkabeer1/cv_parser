from fastapi import FastAPI, UploadFile, File
from pyresparser import ResumeParser
from threading import Thread
import shutil
import os
app = FastAPI()


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
    return resume_data


@app.get("/cv-parser2/testing/")
async def testing():
    return {"message": "Hello World"}


@app.post("/cv-parser2/uploadresume/")
async def upload_resume(file: UploadFile = File(...)):
    try:
        
        temp_file_path = f"temp_{file.filename}"
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        
        thread = Thread(target=parse_and_format_resume, args=(temp_file_path,))
        thread.start()
        thread.join()  

        
        formatted_resume_data = parse_and_format_resume(temp_file_path)

        
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

        return formatted_resume_data
    except Exception as e:
        return {"error": str(e)}