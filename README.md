# 📊 PEMD Diagnostic Tool

![Python Version](https://img.shields.io/badge/python-3.13.1-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.27.0-orange)
![License](https://img.shields.io/badge/License-MIT-green)

[![Open in Streamlit](https://img.shields.io/badge/Open%20App-Streamlit-orange)](https://pemdapp-mdxxrcfaen7suzshgdsmee.streamlit.app/)


## PEMD_App

## Description
The **PEMD** (Products, Equipment, Materials, and Waste) Diagnostic Tool is a simple web application to **estimate the mass of construction materials** before demolition or recycling.  
It allows users to input materials, volumes, or dimensions, and generates a **summary table with totals**.  
The app also supports **CSV export** for further use in Excel or other software.

---

## Features
- Select materials from a **modifiable list** (`materials.py`) with known densities.  
- Input modes for volume calculation:  
  - **Direct volume** (m³)  
  - **Dimensions** (length × width × height)  
  - **Surface + thickness**  
- Automatic calculation of **volume and mass** for each material.  
- Display a **summary table** showing:  
  - Total volume  
  - Total mass  
  - Percentage contribution of each material  
- **CSV export** ready for Excel.  
- Deployable on **Streamlit Community Cloud** for web access.

---

## Installation (Local)

1. Clone the repository:  
```bash
git clone https://github.com/YOUR_USERNAME/PEMD_App.git
cd PEMD_App
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
streamlit run PEMD_App.py
```

## Main File

- `PEMD_App.py` : Main Streamlit application.

- `materials.py` : List of materials and their densities.

- `requirements.txt` : Python dependencies (`streamlit`, `pandas`).

 
##  