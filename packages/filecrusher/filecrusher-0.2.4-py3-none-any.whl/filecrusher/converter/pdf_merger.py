# package name PyMuPdf
import os

import fitz


def merge_pdf_files(file_list: list[str], merged_result_file: str) -> None:
    # merge page files into final destination
    merger = fitz.open()
    for file in file_list:
        if os.path.exists(merged_result_file):
            with fitz.open(merged_result_file) as f:
                merger.insert_pdf(f)
        with fitz.open(file) as f:
            merger.insert_pdf(f)
        os.remove(file)
    merger.save(merged_result_file)
