from flask import request,send_from_directory,render_template
import PyPDF2
import os
import app

from app import app,SPLIT_FILE,IMAGE_PDF
from PIL import Image
def process1_pdf():
    if request.method=='POST':
        first=request.form['start_page']
        end=request.form['end_page']
        first,end=int(first),int(end)
        file=request.files['pdf_file']
        reader=PyPDF2.PdfReader(file)
        writer=PyPDF2.PdfWriter()
        while first<=end:
            page=reader.pages[first]
            writer.add_page(page)
            first+=1
        split_path=os.path.join(app.config['UPLOAD_FOLDER'],SPLIT_FILE)
        with open(split_path,"wb") as f:
            writer.write(f)
        return render_template('ready.html')
def split_final():
    return  send_from_directory(app.config['UPLOAD_FOLDER'],SPLIT_FILE,as_attachment=True)  
def image_to_pdf():
    if request.method=='POST':
        files=request.files.getlist('files')  
        list=[]
        for file in files:
            img=Image.open(file) 
            img=img.convert('RGB')
            list.append(img)  
            
        save_path=os.path.join(app.config['UPLOAD_FOLDER'],IMAGE_PDF) 
        list[0].save(save_path,save_all=True,append_images=list[1:],resolution=100.0,quality=95)
        return render_template('ready1.html')
        
def image_final():             
       return send_from_directory(app.config['UPLOAD_FOLDER'],IMAGE_PDF)   
