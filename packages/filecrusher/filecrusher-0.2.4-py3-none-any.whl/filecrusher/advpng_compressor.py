import os
import subprocess
import sys
from subprocess import CalledProcessError

from .config import ADVPNG_PATH
from .file_operations import copy_file, check_if_valid_image, get_file_size
from .processor import processor


class ADVPNGCompressor:
    def __init__(
            self,
            shrink_rate: int = 2,
            iterations: int = 1,
            extra_args: str = "",
            event_handlers=None
    ):
        """
        Compresses PNG images using advpng.
        :param shrink_rate (from 'https://www.advancemame.it/doc-advpng')
            -0, --shrink-store
                Disable the compression. The file is only stored and not compressed.
                The file is always rewritten also if it's bigger.
            -1, --shrink-fast
                Set the compression level to "fast" using the zlib compressor.
            -2, --shrink-normal
                Set the compression level to "normal" using the libdeflate compressor.
                This is the default level of compression.
            -3, --shrink-extra
                Set the compression level to "extra" using the 7z compressor.
                You can define the compressor iterations with the -i, --iter option.
            -4, --shrink-insane
                Set the compression level to "insane" using the zopfli compressor.
                You can define the compressor iterations with the -i, --iter option.
        :param iterations - amount of repetitions > 0
            more -> better compression but much slower
        :param extra_args: extra args to pass the executable
        :param event_handlers: (list of EventHandler) A list of event handlers. (pre and postprocessors)
        """
        self.event_handlers = event_handlers
        if self.event_handlers is None:
            self.event_handlers = []

        advpng_path = ADVPNG_PATH
        if not os.path.isfile(advpng_path):
            linux_error = "Install it with 'sudo apt install advancecomp'." if os.name != "nt" else ""
            raise FileNotFoundError(rf"advpng path not found at '{advpng_path}'. {linux_error}")

        if shrink_rate < 0 or shrink_rate > 4:
            raise ValueError("shrink_rate needs to be a value in range 0-4")
        if iterations < 0:
            raise ValueError("iterations need to be greater than 0")

        system_extra = "powershell.exe" if os.name == 'nt' else ""
        # compress, shrink-normal, 3 rounds of compression
        advpng_options = " ".join(("--recompress", f"-{shrink_rate}", f"-i {iterations}", extra_args))
        self.advpng_command = f"{system_extra}  {advpng_path} {advpng_options}"

    @processor
    def process_file(self, source_file: str, destination_path: str) -> None:
        copy_file(source_file, destination_path)
        check_if_valid_image(source_file)

        try:
            subprocess.check_output(f"{self.advpng_command} '{destination_path}'", stderr=subprocess.STDOUT, shell=True)
        except CalledProcessError as cpe:
            print(repr(cpe), file=sys.stderr)
            print("processing failed at the advpng stage. (IGNORE)\n", file=sys.stderr)
        except Exception as e:
            print(repr(e), file=sys.stderr)  # explicitly dont raise e

        if check_if_valid_image(destination_path, True) or get_file_size(source_file) < get_file_size(destination_path):
            copy_file(source_file, destination_path)
