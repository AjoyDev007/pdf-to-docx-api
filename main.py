from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from pdf2docx import Converter
import os

app = FastAPI()

@app.post("/convert")
async def convert_pdf(file: UploadFile = File(...)):
    input_path = f"temp_{file.filename}"
    output_path = input_path.replace(".pdf", ".docx")
    
    with open(input_path, "wb") as buffer:
        buffer.write(await file.read())
        
    cv = Converter(input_path)
    cv.convert(output_path, start=0, end=None)
    cv.close()
    
    os.remove(input_path)
    return FileResponse(
        output_path, 
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document", 
        filename="converted.docx"
    )
