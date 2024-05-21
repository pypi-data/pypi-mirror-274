import os
import subprocess

from .config import PNGQUANT_PATH
from .file_operations import compare_and_use_better_option, check_if_valid_image
from .processor import processor


class PNGQuantCompressor:
    __FILE_SIZE_INCREASED_ERROR: int = 98
    __IMAGE_QUALITY_BELOW_LIMIT_ERROR: int = 99

    def __init__(
            self,
            speed: int = 1,
            min_quality: int = 80,
            max_quality: int = 100,
            event_handlers=None
    ):
        """
        Compresses PNG images using pngquant.
        :param speed: Speed of compression, where 0 is the slowest (best quality) and 10 is the fastest.
        :param min_quality: The minimum quality threshold, ranging from 1 to 99. If the conversion results
            in a quality below this threshold, the image won't be saved.
        :param max_quality: The maximum quality threshold, ranging from 1 to 99. Instructs pngquant to use
            the least amount of colors required to meet or exceed this quality.
        :param event_handlers: A list of event handlers. (pre and postprocessors)

        :returns: None
        """
        self.event_handlers = event_handlers
        if self.event_handlers is None:
            self.event_handlers = []

        pngquant_path = PNGQUANT_PATH
        if not os.path.isfile(pngquant_path):
            linux_error = "Install it with 'sudo apt install pngquant'." if os.name != "nt" else ""
            raise FileNotFoundError(rf"pngquant path not found at '{pngquant_path}'. {linux_error}")

        if speed < 0 or speed > 10:
            raise ValueError("speed needs to be a value in range 0-10")
        if min_quality < 0 or min_quality >= 100:
            raise ValueError("min_quality needs to be between 0 and 100")
        if max_quality < 0 or max_quality < min_quality:
            raise ValueError("max_quality need to be greater than 0 and min_quality")

        system_extra = "powershell.exe" if os.name == 'nt' else ""
        pngquant_options = " ".join((
            f"--quality={min_quality}-{max_quality}",
            "--force",
            f"--speed {speed}",
            "--strip",
            "--ext '-comp.png'"
        ))
        self.pngquant_command = rf'{system_extra}  {pngquant_path} {pngquant_options}'

    @processor
    def process_file(self, source_file: str, destination_path: str):
        check_if_valid_image(source_file)
        if not os.path.exists(os.path.dirname(destination_path)):
            os.makedirs(os.path.dirname(destination_path), exist_ok=True)

        subprocess.check_output(f'{self.pngquant_command} "{source_file}"',
                                stderr=subprocess.STDOUT, shell=True)
        result_file = source_file[:-4] + '-comp.png'
        compare_and_use_better_option(source_file, result_file, destination_path)
        if os.path.exists(result_file):
            os.remove(result_file)
