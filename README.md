# UK-ANPR

UK-ANPR is a deep learning-based Automatic Number Plate Recognition (ANPR) system tailored for UK license plates. It combines a license plate detector and a character recognizer to process static images and deliver readable plate text.

> ⚠️ This project is intended for **educational and personal experimentation only**.

---

## 🚀 Features

- License plate detection using a pre-trained model.
- Character segmentation and recognition using a second model.
- Clean web interface using Flask.
- Accepts image uploads and displays cropped and recognized results.
- Pre-included models for out-of-the-box functionality.

---

## 🛠 Requirements

- Python 3.8+
- Flask
- Torch / torchvision
- OpenCV
- PIL

Install dependencies:
```bash
pip install -r requirements.txt
```

---

## 📂 Project Structure

```
UK-ANPR/
├── app.py                  # Main Flask app
├── utils.py                # Core detection and recognition logic
├── models/                 # Pretrained PyTorch models
├── templates/              # HTML templates
├── static/                 # Output images (cropped, results)
├── uploads/                # Uploaded image files
├── examples/               # Example images
├── LICENSE.md              # Personal Use License
└── README.md               # You're reading it!
```

---

## ▶️ How to Run

```bash
python app.py
```

Then open your browser and go to:  
[http://127.0.0.1:5000](http://127.0.0.1:5000)

You can upload an image via the web interface to run the ANPR process and see results visually.

---

## 🧪 Example Usage

Use one of the images in `examples/` or upload your own:

```
examples/
├── ex1.png
├── ex2.png
```

Outputs (plate crops, OCR results) will be saved in:
- `static/crops/`
- `static/results/`

---

## 📄 License

📄 Licensed under a **Personal Use Only License**. See [LICENSE.md](./LICENSE.md) for details.

---

## 🛑 Disclaimer

This software is provided **strictly for personal, non-commercial use only**. It may not be used by any company, institution, government, or for any commercial or research purpose without express written consent from the author.

---

## 📬 Contact

For commercial or institutional licensing inquiries, please contact:  
📧 Jim.W1234@icloud.com  
👤 Author: trecks
