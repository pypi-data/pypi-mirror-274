import os

# package name PyMuPdf
import fitz

from ..file_operations import get_filename
from ..processor import processor


class PdfToImageConverter:
    SUPPORTED_FILETYPES = ["png", "pnm", "pgm", "pbm", "ppm", "pam", "psd", "ps"]  # TODO test all possible types

    def __init__(
            self,
            file_type_to: str,
            dpi: int = 400,
            event_handlers=None
    ):
        """
        :param file_type_to: resulting image file type
        :param dpi: pdf dpi that should be used when converting to image pixels
        :param event_handlers: A list of event handlers. (pre and postprocessors)
        """
        self.event_handlers = event_handlers
        if self.event_handlers is None:
            self.event_handlers = []

        if file_type_to == "":
            raise ValueError("file_type_to cant be empty!")
        self._file_type_to = self.without_dot_at_the_beginning(file_type_to).lower()
        if self._file_type_to not in self.SUPPORTED_FILETYPES:
            raise ValueError(f"{file_type_to} is not supported.")

        if dpi < 0:
            raise ValueError("default dpi needs to be greater than 0")
        self.__dpi = dpi

    @staticmethod
    def without_dot_at_the_beginning(string):
        return string if not string.endswith(".") else string[1:]

    @processor
    def process_file(self, source_file: str, destination_path: str) -> None:
        # create destination directory if not already exists
        # TODO create proper preprocessor/postprocessors for console output
        print("--splitting pdf into images--")

        # open pdf and split it into rgb-pixel maps -> png
        doc = fitz.open(source_file)
        chars_needed_for_highest_page_number = len(str(len(doc)))

        def get_page_number_string(page_num: int) -> str:
            raw_num = str(page_num)
            return "0" * (chars_needed_for_highest_page_number - len(raw_num)) + raw_num

        for page in doc:
            print(f"** - Finished Page {page.number + 1}/{len(doc)}")
            pix = page.get_pixmap(dpi=self.__dpi)
            page_number = get_page_number_string(page.number + 1)
            pix.save(os.path.join(destination_path, '%s_page_%s.%s' %
                                  (get_filename(source_file), page_number, self._file_type_to)))
