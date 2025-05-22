
# Challenge Description

A URL is provided that points to data containing hidden information. Your task is to build a program that retrieves this data and reveals hidden characters by interpreting their associated x-y coordinates.


# Render Hidden Characters to Word

This is a simple Python script that retrieves data from a given URL containing a list of characters associated with specific x- and y-coordinates. These characters are in Unicode but when rendered based on their coordinates, they reveal a hidden word.

The script processes the coordinate-character data and outputs the correctly ordered hidden word to the terminal.

---

## 📄 URL to Hidden Data

The hidden data is hosted on the following public Google Docs page:

[https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub](https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub)

---

## 💻 Prerequisites

* Python 3.8 or higher
* `pip` (Python package installer)
* Internet connection (to access the document)

---

## ⚙️ Setup Instructions

1. **Clone the repository**

   ```bash
   git clone https://github.com/EgbieAndersonUku1/render_hidden_word.git . 
   cd render_hidden_word
   ```

2. **Create a virtual environment**

   * On macOS/Linux:

     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

   * On Windows:

     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Navigate to the working directory**

   Make sure you're inside the `renderInputData` folder.

   ```bash
   cd renderInputData
   ```

5. **Run the script**

   ```bash
   python render_hidden_word.py
   ```

   The script will process the document and output the hidden word in your terminal.

---


## ✅ Example Output

```text
Hidden word: hidden word```

