import requests

url = 'https://seashell-app-g9kqu.ondigitalocean.app/cv-parser2/uploadresume/'  
file_path = 'C:/LinkHR/Cvs/all Cvs/Abubakar_Sattar.pdf'  


with open(file_path, 'rb') as file:
    files = {'file': (file_path, file)}
    response = requests.post(url, files=files)


print(response.text)
