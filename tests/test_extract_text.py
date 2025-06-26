import os
import sys
import types
from pathlib import Path

# Ensure repository root is in sys.path for module imports
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# Stub tqdm to avoid dependency on the real package
tqdm_stub = types.ModuleType("tqdm")
tqdm_stub.tqdm = lambda iterable, **kwargs: iterable
sys.modules['tqdm'] = tqdm_stub

# create a minimal pdfplumber stub before importing the module under test
pdfplumber_stub = types.ModuleType("pdfplumber")

class DummyPage:
    def extract_text(self):
        return "dummy page text"

class DummyPdf:
    def __init__(self, *args, **kwargs):
        self.pages = [DummyPage()]
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc, tb):
        pass

def dummy_open(file, password=None):
    return DummyPdf()

pdfplumber_stub.open = dummy_open
sys.modules['pdfplumber'] = pdfplumber_stub

import PDFtoText


def test_uppercase_pdf_extension(tmp_path):
    pdf_dir = tmp_path / "pdfs"
    txt_dir = tmp_path / "txts"
    pdf_dir.mkdir()
    txt_dir.mkdir()

    # create a dummy PDF file with uppercase extension
    pdf_file = pdf_dir / "sample.PDF"
    pdf_file.write_text("content")

    PDFtoText.extract_text_from_pdf(str(pdf_dir), str(txt_dir), True, None)

    expected_txt = txt_dir / "sample.txt"
    assert expected_txt.exists(), "Text file was not created for uppercase PDF"
    # verify contents were written from DummyPage
    assert "dummy page text" in expected_txt.read_text()
