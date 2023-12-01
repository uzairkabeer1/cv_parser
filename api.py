from fastapi import FastAPI, File, UploadFile
from boto3 import session as boto3_session
from botocore.client import Config
from pyresparser import ResumeParser
import os
import shutil

app = FastAPI()


ACCESS_ID = 'DO00NTV6Z7P4HNXANDWF'  
SECRET_KEY = '0FHGT+GOLfu6Fg9k/X52DE3MU70/bG83O7N9DWxu1VM' 


session = boto3_session.Session()
client = session.client('s3',
                        region_name='nyc3',  
                        endpoint_url='https://cvdata.nyc3.digitaloceanspaces.com',  
                        aws_access_key_id=ACCESS_ID,
                        aws_secret_access_key=SECRET_KEY)


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


@app.get("/testing/")
async def testing():
    return {"message": "Hello World"}


@app.post("/uploadresume/")
async def upload_resume(file: UploadFile = File(...)):
    try:
        temp_file_path = file.filename.split('/')[-1].split('\\')[-1]

        
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        
        client.upload_file(temp_file_path, 'cvdata', f'cv/{temp_file_path}')

        
        resume_data = parse_and_format_resume(temp_file_path)
        formatted_data = format_resume_data(resume_data)

        
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

        return formatted_data
    except Exception as e:
        return {"error": str(e)}