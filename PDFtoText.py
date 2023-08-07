import pdfplumber
import os
import glob

def extract_text_from_pdf(pdf_dir_path, txt_dir_path):
    pdf_files = glob.glob(os.path.join(pdf_dir_path, '*.pdf'))

    for pdf_file in pdf_files:
        try:
            with pdfplumber.open(pdf_file) as pdf:
                txt_file_name = os.path.join(txt_dir_path, os.path.basename(pdf_file).replace('.pdf', '.txt'))
                with open(txt_file_name, 'w') as txt_file:
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        # only write to file if page_text is not None
                        if page_text is not None:
                            txt_file.write(page_text)
                            txt_file.write('\n') # for separating pages
        except Exception as e:
            print(f"Failed to process {pdf_file}: {str(e)}")

# Usage
extract_text_from_pdf('Path_to_PDF', 'Path_to_txt_Output')