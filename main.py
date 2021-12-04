import uvicorn
from fastapi import FastAPI, File, UploadFile
from starlette.responses import RedirectResponse
import json
import requests

app_desc = """<h2>Try this app by uploading any image with `predict/image`</h2>"""

app = FastAPI(title="Tensorflow FastAPI Start Pack", description=app_desc)


@app.get("/", include_in_schema=False)
async def index():
    return RedirectResponse(url="/docs")


@app.post("/predict/image")
async def predict_api(file: UploadFile = File(...)):
    extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png")
    if not extension:
        return "Image must be jpg or png format!"

    url = 'https://api.fpt.ai/vision/idr/vnm'

    files = {'image': open('samples/' + file.filename, 'rb').read()}
    headers = {
        'api-key': 'CSxplM7ICE5iXUjcQGJRnD0p2UKxT94a'# cập nhật key
    }

    response = requests.post(url, files=files, headers=headers)
    result = json.loads(response.text)  

    if (result['data'][0]['doe']=="" or result['data'][0]['doe']=="N/A"):
       result['data'][0]['doe']= 'Không có thông tin'       
    if (result['data'][0]['id']=="" or result['data'][0]['id']=="N/A"):
       result['data'][0]['id']= 'Không có thông tin'      
    if (result['data'][0]['name'] == "" or result['data'][0]['name']=="N/A"):
       result['data'][0]['name']= 'Không có thông tin'       
    if (result['data'][0]['sex']=="" or result['data'][0]['sex']=="N/A"):
       result['data'][0]['sex']= 'Không có thông tin'          
    if (result['data'][0]['dob']=="" or result['data'][0]['dob']=="N/A"):
       result['data'][0]['dob']= 'Không có thông tin'       
    if (result['data'][0]['home']=="" or result['data'][0]['home']=="N/A"):
       result['data'][0]['home']= 'Không có thông tin'      
    if (result['data'][0]['address']=="" or result['data'][0]['address']=="N/A"):
       result['data'][0]['address']= 'Không có thông tin'       

    result_json = {'id':  result['data'][0]['id'],\
                    'hoten':  result['data'][0]['name'],\
                    'ngaysinh':   result['data'][0]['dob'],\
                    'gioitinh':   result['data'][0]['sex'] ,\
                    'nguyenquan':  result['data'][0]['home'],\
                    'thuongtru':   result['data'][0]['address'],\
                    'ngayhethan':   result['data'][0]['doe']   }
    return result_json
#Internal Server Error ràng buộc mã lỗi

if __name__ == "__main__":
    uvicorn.run(app, debug=True)