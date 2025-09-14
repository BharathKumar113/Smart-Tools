from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, send_file, after_this_request,jsonify,session
import requests
import io
from dateutil.relativedelta import relativedelta  
import csv
import os
import mimetypes
import PyPDF2
import instaloader
import gtts
import qrcode
import googletrans
from datetime import datetime
import calendar
from PIL import Image

app = Flask(__name__)
app.secret_key = 'your_secret_key'


UPLOAD_FOLDER = 'uploads'
REELS_FOLDER = 'reels'  
ENCRYPTED_FILE_NAME = 'new_encrypted.pdf'
SPLIT_FILE = 'splitted.pdf'
INSTA_FILE = 'insta.mp4'
IMAGE_PDF='images_to_pdf.pdf'
TEXT='pdf.txt'
SPEECH='speech.mp3'
QR='qr.png'
TEXT_SPEECH=''''''
COMPRESS='compress.png'
USER_DATA_FILE="users.csv"

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['REELS_FOLDER'] = REELS_FOLDER


os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REELS_FOLDER, exist_ok=True)


import operation


@app.route('/process', methods=['GET', 'POST'])
def process_pdf():
    return operation.process1_pdf()

@app.route('/pdf_text')
def pdf_to_text():
    return render_template('text.html')


def calculate_interest(amount, rate, time_months):
    return amount * rate * time_months / 100

def calculate_total(amount, interest):
    return amount + interest

@app.route('/interest_calculator', methods=['GET', 'POST'])
def interest_calculator():
    if request.method == 'POST':
        try:
            amount = float(request.form['amount'])
            months = int(request.form['months'])
            interest_rate = float(request.form['interest_rate'])  

            
            start_day = int(request.form['start-day'])
            start_month = int(request.form['start-month'])
            start_year = int(request.form['start-year'])
            end_day = int(request.form['end-day'])
            end_month = int(request.form['end-month'])
            end_year = int(request.form['end-year'])

            
            start_date = datetime(start_year, start_month, start_day)
            end_date = datetime(end_year, end_month, end_day)

            
            time_difference = (end_date.year - start_date.year) * 12 + end_date.month - start_date.month
            if end_date.day < start_date.day:
                time_difference -= 1 

          
            if time_difference < 0:
                time_difference = 0

            
            interest = calculate_interest(amount, interest_rate, time_difference)
            total_amount = calculate_total(amount, interest)
            total_interest = interest

            return jsonify({
                'success': True,
                'total_amount': total_amount,
                'total_interest': total_interest
            })
        
        except KeyError as e:
            return jsonify({'success': False, 'message': f'Missing form field: {e}'}), 400
        except ValueError:
            return jsonify({'success': False, 'message': 'Invalid input'}), 400

    return render_template('interest.html')

@app.route('/text_to_speech')
def text_to_speech():
    return render_template('speech.html')
@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/login")
def login():
    return render_template("login.html")
@app.route('/validate_signup', methods=['POST'])
def validate_signup():
    if request.method=="POST":
        
        full_name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')
    
        
        if not full_name or not email or not password or not confirm_password:
            return "All fields are required!", 400
        
        if password != confirm_password:
            return "Passwords do not match!", 400
    
       
        with open(USER_DATA_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            
            
            if file.tell() == 0:
                writer.writerow(['Full Name', 'Email', 'Password'])
            
            
            writer.writerow([full_name, email, password])
        
        
        return redirect(url_for('login'))

@app.route('/validate_login', methods=['POST'])
def login_post():
    if request.method=="POST":
        session['logged_in'] = True
        email = request.form.get('email')
        password = request.form.get('password')
    
       
        with open(USER_DATA_FILE, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  
            
            for row in reader:
                if row[1] == email and row[2] == password:
                    
                    return redirect(url_for('dash'))
    
        
        flash("Invalid email or password", "error")
        return redirect(url_for('login'))
    
@app.route('/image_compress')  
def image_compress():
            return render_template('image_compress.html')  
@app.route('/compressing',methods=['GET','POST'])
def compressing():
    quality=80
    if request.method=='POST':
        num=request.form['size']
        num=int(num)
        target=num*1024
        
        image=request.files['image']
        path=os.path.join(app.config['UPLOAD_FOLDER'],image.filename)
        image.save(path)
        img=Image.open(path)
        while True:
            size=os.path.getsize(path)
            if size<=target:
                break
            else:
                    quality-=5
                    img.save(path,optimize=True,quality=quality)
                    
                    
            
        
    acpath=os.path.join(app.config['UPLOAD_FOLDER'],COMPRESS)
    os.rename(path,acpath)    
    return send_from_directory(app.config['UPLOAD_FOLDER'],COMPRESS,as_attachment=True)
                
            
            
            
@app.route('/calendar')
def view_calendar():
    return render_template('calendar.html')

@app.route('/submit_date', methods=['POST'])
def submit_date():
    if request.method == 'POST':
        year = int(request.form['year'])
        month = int(request.form['month'])
        
        if month == 0:  
            html = calendar.HTMLCalendar(calendar.SUNDAY)
            yearly_cal = {
                calendar.month_name[m]: html.formatmonth(year, m)
                for m in range(1, 13)
            }
            return render_template('final_cal.html', yearly_cal=yearly_cal)
        
        else:  
            html = calendar.HTMLCalendar(calendar.SUNDAY)
            cal = html.formatmonth(year, month)
            return render_template('final_cal.html', cal=cal)

@app.route('/birthday_calculator')
def birthday_calculator():
      return render_template('birthday.html')
@app.route('/calculate_age',methods=['GET','POST'])      

def calculate_age():
    result = ''  
    if request.method == 'POST':
        dt = request.form['dob']
        dob = datetime.strptime(dt, "%Y/%m/%d")
        today = datetime.now()
        
        
        age = relativedelta(today, dob)
        
        result = f"You are {age.years} years {age.months} months {age.days} days old."
    
    return render_template('birthday_final.html', result=result)

        



@app.route('/text_to_qr')
def text_to_qrcode():
    return render_template('qrcode.html')

@app.route("/date")
def date():
    return render_template('date.html')

@app.route("/date_diff",methods=['GET','POST'])
def date_diff():
    global final
    if request.method=='POST':
        fdate=request.form['start_date']
        ldate=request.form['end_date']
        first_date=datetime.strptime(fdate,"%Y/%m/%d")
        last_date=datetime.strptime(ldate,"%Y/%m/%d")
        years=last_date.year-first_date.year
        months=last_date.month-first_date.month
        days=last_date.day-first_date.day
        if days<0:
            
             if months==1:
                days+=(datetime(last_date.year-1,12,1)-datetime(last_date.year-1,11,1)).days
                months-=1
             else:
                days+=(datetime(last_date.year,last_date.month,1)-datetime(last_date.year,last_date.month-1,1)).days
                months-=1    
             if months<0:
               years-=1
               months+=12   
        final=f"{years} years {months} months and {days} days"           
    return render_template('final_date.html',final=final)    
        


@app.route('/generate_qr',methods=['POST','GET'])
def generate_qr():
    if request.method=='POST':
        text=request.form['text']
        qr=qrcode.make(text)
        for i in os.listdir(app.config['UPLOAD_FOLDER']):
            if i.endswith('.png'):
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'],i))
        path=os.path.join(app.config['UPLOAD_FOLDER'],QR)
        qr.save(path)    
    return send_from_directory(app.config['UPLOAD_FOLDER'],QR,as_attachment=True)     

@app.route('/submit_speech',methods=['POST'])
def submit_speech():
    global TEXT_SPEECH
    if request.method=='POST':
             text=request.form['text']
             TEXT_SPEECH=text  
    return render_template('finalspeech.html')   
@app.route('/eng_download')  
def eng_download():
              global  TEXT_SPEECH
              text=TEXT_SPEECH
              voice=gtts.gTTS(text)
              for i in os.listdir(app.config['UPLOAD_FOLDER']):
                  if i.endswith('.mp4'):
                      os.remove(os.path.join(app.config['UPLOAD_FOLDER'],i))
              path=os.path.join(app.config['UPLOAD_FOLDER'],SPEECH)
              voice.save(path)
              return send_from_directory(app.config['UPLOAD_FOLDER'],SPEECH)
              
              
@app.route('/tel_download')
def tel_download():
                
                global  TEXT_SPEECH
                text=TEXT_SPEECH
                trans=googletrans.Translator()
                translated=trans.translate(text=text,src='en',dest='te')
                voice=gtts.gTTS(translated.text,slow=True)
                for i in os.listdir(app.config['UPLOAD_FOLDER']):
                    if i.endswith('.mp4'):
                        os.remove(os.path.join(app.config['UPLOAD_FOLDER'],i))
                path=os.path.join(app.config['UPLOAD_FOLDER'],SPEECH)
                voice.save(path)   
                return send_from_directory(app.config['UPLOAD_FOLDER'],SPEECH,as_attachment=False)     
                
                
                                                
@app.route('/pdftext', methods=['POST'])
def pdf_text():
    doc = ''
    if request.method == 'POST':
        file = request.files['pdf']
        reader = PyPDF2.PdfReader(file)
        for i in range(len(reader.pages)):
            page = reader.pages[i]
            doc += page.extract_text()

       
        for i in os.listdir(app.config['UPLOAD_FOLDER']):
            if i.endswith('.doc'):
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], i))

        path = os.path.join(app.config['UPLOAD_FOLDER'], TEXT)
        with open(path, "w") as f:
            f.write(doc)

    return send_from_directory(app.config['UPLOAD_FOLDER'], TEXT,as_attachment=True)
    
    
    
    
@app.route('/splitpdf')
def split_pdf():
    return render_template('pdf.html')

@app.route('/upload_images',methods=['POST'])
def upload_image():
    return operation.image_to_pdf()

@app.route('/imagetopdf')
def images_to_pdf():
    return render_template('imagepdf.html')

@app.route("/insta_download", methods=['GET', 'POST'])
def insta_downloader():
    if request.method == 'POST':
        print("hello")
        url = request.form['url']
        if not url:
            flash("Please provide a valid Instagram video URL.", "error")
            return redirect(url_for('insta'))

        try:
            L = instaloader.Instaloader()
            shortcode = url.split('/')[-2]
            post = instaloader.Post.from_shortcode(L.context, shortcode)
            video_url=post.video_url
            print(video_url)
            buffer=io.BytesIO()
            response=requests.get(video_url)
            print(len(response.content))
            if response.status_code==200:
                for chunk in response.iter_content(chunk_size=1024):
                    buffer.write(chunk)
                   
                buffer.seek(0)
                return send_file(buffer,mimetype="video/mp4")
           

      
            

        except Exception as e:
            flash(f"Error downloading Instagram video: {str(e)}", "error")
            return redirect(url_for('insta'))

    return render_template('insta.html')


@app.route("/finale")
def downloading():
    return send_from_directory(app.config['UPLOAD_FOLDER'], INSTA_FILE, as_attachment=True)


@app.route('/')
def dash():
    return render_template('demo1.html')


@app.route("/insta")
def insta():
    return render_template('insta.html')


@app.route("/home")
def home():
    return render_template('index.html')

@app.route('/splitter')
def split_finale():
    return operation.split_final()

@app.route('/imagespdf')
def image_finale():
    return operation.image_final()
@app.route("/pass")
def name():
    encrypted_file_path = os.path.join(app.config['UPLOAD_FOLDER'], ENCRYPTED_FILE_NAME)
    file_exists = os.path.isfile(encrypted_file_path)
    return render_template('home.html', encrypted_file=ENCRYPTED_FILE_NAME if file_exists else None)


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        password = request.form['password']
        mimetype, _ = mimetypes.guess_type(file.filename)
        if mimetype != 'application/pdf':
            flash("Invalid file type. Please upload a PDF.", "error")
            return redirect(url_for('home'))
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        try:
            with open(file_path, "rb") as file_to_encrypt:
                reader = PyPDF2.PdfReader(file_to_encrypt)
                writer = PyPDF2.PdfWriter()
                for page in reader.pages:
                    writer.add_page(page)

                writer.encrypt(user_password=password)

                encrypted_path = os.path.join(UPLOAD_FOLDER, ENCRYPTED_FILE_NAME)
                with open(encrypted_path, "wb") as f:
                    writer.write(f)

            flash("File encrypted successfully!", "success")
            return redirect(url_for('name'))
        except PyPDF2.errors.PdfReadError as e:
            flash(f"Error reading PDF: {str(e)}", "error")
            return redirect(url_for('home'))
    else:
        flash("No file uploaded for encryption.", "error")
        return redirect(url_for('home'))


@app.route('/download')
def download_file():
    encrypted_path = os.path.join(UPLOAD_FOLDER, ENCRYPTED_FILE_NAME)
    if not os.path.isfile(encrypted_path):
        flash("Encrypted file not found.", "error")
        return redirect(url_for('name'))

    return send_from_directory(app.config['UPLOAD_FOLDER'], ENCRYPTED_FILE_NAME, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
