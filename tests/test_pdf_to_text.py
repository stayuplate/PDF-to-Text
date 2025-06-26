import importlib.util
import sys
from types import SimpleNamespace
import os

import pytest


def import_module(monkeypatch):
    fake_pdfplumber = SimpleNamespace()
    fake_tqdm = SimpleNamespace(tqdm=lambda x, **kw: x)
    monkeypatch.setitem(sys.modules, 'pdfplumber', fake_pdfplumber)
    monkeypatch.setitem(sys.modules, 'tqdm', fake_tqdm)
    if 'PDFtoText' in sys.modules:
        del sys.modules['PDFtoText']
    spec = importlib.util.spec_from_file_location(
        'PDFtoText', os.path.join(os.path.dirname(__file__), os.pardir, 'PDFtoText.py')
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module, fake_pdfplumber


def test_extract_text_writes_file(tmp_path, monkeypatch):
    module, fake_pdfplumber = import_module(monkeypatch)

    pdf_dir = tmp_path / 'pdf'
    txt_dir = tmp_path / 'txt'
    pdf_dir.mkdir()
    txt_dir.mkdir()

    pdf_file = pdf_dir / 'sample.pdf'
    pdf_file.write_text('dummy')

    monkeypatch.setattr(module.glob, 'glob', lambda pattern: [str(pdf_file)])

    class FakePage:
        def __init__(self, text):
            self._text = text
        def extract_text(self):
            return self._text

    class FakePDF:
        def __init__(self):
            self.pages = [FakePage('Hello'), FakePage('World')]
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc, tb):
            pass

    def fake_open(path, password=None):
        assert path == str(pdf_file)
        assert password == 'pwd'
        return FakePDF()

    fake_pdfplumber.open = fake_open

    module.extract_text_from_pdf(str(pdf_dir), str(txt_dir), overwrite=False, password='pwd')

    result = (txt_dir / 'sample.txt').read_text()
    assert result == 'Hello\nWorld\n'


def test_extract_text_respects_overwrite(tmp_path, monkeypatch):
    module, fake_pdfplumber = import_module(monkeypatch)

    pdf_dir = tmp_path / 'pdf'
    txt_dir = tmp_path / 'txt'
    pdf_dir.mkdir()
    txt_dir.mkdir()

    pdf_file = pdf_dir / 'sample.pdf'
    pdf_file.write_text('dummy')

    target_txt = txt_dir / 'sample.txt'
    target_txt.write_text('OLD')

    calls = []

    class FakePage:
        def __init__(self, text):
            self._text = text
        def extract_text(self):
            return self._text

    class FakePDF:
        def __init__(self, text):
            self.pages = [FakePage(text)]
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc, tb):
            pass

    def fake_open(path, password=None):
        calls.append(path)
        return FakePDF('NEW')

    fake_pdfplumber.open = fake_open
    monkeypatch.setattr(module.glob, 'glob', lambda pattern: [str(pdf_file)])

    module.extract_text_from_pdf(str(pdf_dir), str(txt_dir), overwrite=False, password=None)
    assert target_txt.read_text() == 'OLD'
    assert not calls  # open not called when skipping

    module.extract_text_from_pdf(str(pdf_dir), str(txt_dir), overwrite=True, password=None)
    assert target_txt.read_text() == 'NEW\n'
    assert len(calls) == 1
