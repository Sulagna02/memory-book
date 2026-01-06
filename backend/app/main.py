# app/main.py
from fastapi import FastAPI, UploadFile, File, HTTPException # for building the API, backend framework, file uploads, and error handling
from pathlib import Path # for path manipulations
import shutil # for file operations
import fitz  # PyMuPDF for PDF text extraction

app = FastAPI(title="Enterprise Document Intelligence System") # Initialize FastAPI app

BASE_DIR = Path(__file__).resolve().parent.parent # Base directory of the project , saving pdf
DATA_DIR = BASE_DIR / "data" # Directory to store uploaded files, saving .txt

DATA_DIR.mkdir(exist_ok=True) # Ensure data directory exists, if not, create it


@app.get("/health") # Health check endpoint
def health_check(): # Simple health check endpoint
    return {"status": "ok"} # Return status ok if backend is running



@app.post("/upload") # Endpoint to upload PDF documents
def upload_document(file: UploadFile = File(...)): # Accept file uploads
    if file.content_type != "application/pdf": # Check if the uploaded file is a PDF
        raise HTTPException(status_code=400, detail="Only PDF files are supported") # Raise error if not a PDF

    pdf_path = DATA_DIR / file.filename # Path to save the uploaded PDF

    # Save PDF to disk
    with pdf_path.open("wb") as buffer: # Open file in write-binary mode
        shutil.copyfileobj(file.file, buffer) # Save the uploaded file to the specified path

    # Extract text from PDF
    pdf_document = fitz.open(pdf_path) # Open the PDF document using PyMuPDF
    text_content = "" # Initialize empty string to hold extracted text
    for page in pdf_document: # Iterate through each page in the PDF
        text_content += page.get_text() # Extract text from the page and append to text_content

    pdf_document.close() # Close the PDF document

    # Save text to .txt
    txt_filename = file.filename.replace(".pdf", ".txt") # Create a .txt filename based on the PDF filename 
    txt_path = DATA_DIR / txt_filename # Path to save the extracted text file
    with txt_path.open("w", encoding="utf-8") as f: # Open text file in write mode with UTF-8 encoding 
        f.write(text_content) # Write the extracted text to the .txt file

    # Return success response with file details
    return {
        "filename": file.filename,
        "status": "uploaded",
        "text_file": txt_filename
    }