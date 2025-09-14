![Python](https://img.shields.io/badge/Python-3.10-blue)
![Flask](https://img.shields.io/badge/Flask-Framework-green)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Contributions welcome](https://img.shields.io/badge/Contributions-welcome-brightgreen.svg)



# Smart Tools

Smart Tools is a Flask-based multi-utility web application that combines a wide range of tools into one platform. It is designed to help users perform everyday tasks such as working with PDFs, generating QR codes, compressing images, converting text to speech, and much more — all through a simple and user-friendly web interface.

---

## Features

### PDF Tools

* Encrypt and password-protect PDF files.
* Split PDF files into separate pages.
* Convert PDF documents to plain text.

### Calendar and Date Utilities

* Display monthly and yearly calendars in an interactive format.
* Calculate the difference between two dates in years, months, and days.
* Birthday calculator to find exact age in years, months, and days.

### Finance

* Interest calculator that computes total amount and interest over a period using start and end dates.

### Image Tools

* Convert multiple images into a single PDF.
* Compress images to a target size while maintaining quality.

### Text to Speech

* Convert English text into speech.
* Translate English text to Telugu and generate speech in Telugu.

### QR Code Generator

* Generate downloadable QR codes from any given text.

### Instagram Reels Downloader

* Download Instagram videos using Instaloader and Requests.

---

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/smart-tools.git
   cd smart-tools
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:

   ```bash
   python app.py
   ```

4. Open your browser at:

   ```
   http://127.0.0.1:5000/
   ```

---

## Project Structure

```
smart-tools/
│── app.py               # Main Flask application
│── operation.py         # Helper functions for PDF & image processing
│── requirements.txt     # Dependencies
│── templates/           # HTML templates
│── uploads/             # Temporary upload folder
│── reels/               # Instagram reel storage
│── static/              # Static files (CSS, JS, images)
```

---


## Tech Stack

* Backend: Python, Flask
* Frontend: HTML, Bootstrap,css
* Libraries: PyPDF2, Instaloader, gTTS, Pillow, qrcode, Googletrans

---

## Contributing

Contributions, issues, and feature requests are welcome.
Feel free to fork this repository and submit a pull request.

---

