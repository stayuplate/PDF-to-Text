
import argparse
import os
import glob
import pdfplumber
import logging
from tqdm import tqdm


def get_arguments():
    parser = argparse.ArgumentParser(description="Extract text from PDF files and save it as .txt files")
    parser.add_argument("pdf_dir", help="Directory containing the PDF files")
    parser.add_argument("txt_dir", help="Directory to save the .txt files")
    parser.add_argument("-o", "--overwrite", action="store_true", help="Overwrite existing .txt files")
    parser.add_argument("-p", "--password", type=str, default=None, help="Password for encrypted PDFs")
    return parser.parse_args()


def setup_logger():
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%d-%b-%y %H:%M:%S',
        level=logging.INFO
    )


def extract_text_from_pdf(pdf_dir_path, txt_dir_path, overwrite, password):
    pdf_files = glob.glob(os.path.join(pdf_dir_path, '*.pdf'))
    logging.info(f"Found {len(pdf_files)} PDF files")

    for pdf_file in tqdm(pdf_files, desc="Processing PDF files"):
        txt_file_name = os.path.join(txt_dir_path, os.path.basename(pdf_file).replace('.pdf', '.txt'))

        if not overwrite and os.path.exists(txt_file_name):
            logging.warning(f"File {txt_file_name} already exists. Skipping...")
            continue

        try:
            with pdfplumber.open(pdf_file, password=password) as pdf:
                with open(txt_file_name, 'w') as txt_file:
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text is not None:
                            txt_file.write(page_text)
                            txt_file.write('\n')  # for separating pages
            logging.info(f"Successfully processed {pdf_file}")
        except Exception as e:
            logging.error(f"Failed to process {pdf_file}: {str(e)}")


if __name__ == "__main__":
    args = get_arguments()
    setup_logger()
    extract_text_from_pdf(args.pdf_dir, args.txt_dir, args.overwrite, args.password)
