
# PDF to Text Converter

This script extracts text from PDF files in a specified directory and saves the extracted text as .txt files in another specified directory.

## Dependencies
This script uses the following Python libraries:
- pdfplumber
- tqdm
- argparse

You can install these libraries using pip:
```bash
pip install pdfplumber tqdm argparse
```

## Usage
You can run the script using the following command:
```bash
python PDFtoText.py <pdf_directory> <txt_directory> [-o] [-p <password>]
```
- `<pdf_directory>`: The directory containing the PDF files.
- `<txt_directory>`: The directory where the text files will be saved.
- The output directory must already exist; the script does not create it.
- `-o` or `--overwrite`: (Optional) If specified, existing text files will be overwritten. If not specified, existing text files will be skipped.
- `-p <password>` or `--password <password>`: (Optional) If your PDFs are encrypted, you can provide the password using this option.

## Logging
The script provides logging information, including the number of PDF files found, the progress of processing the files, and any errors encountered. The logging information is displayed in the console.

## Note
This script works with both encrypted and unencrypted PDFs. For encrypted PDFs, you will need to provide the password.
