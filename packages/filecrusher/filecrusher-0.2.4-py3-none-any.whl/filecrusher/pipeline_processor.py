import os
import shutil
import tempfile

from .processor import processor


class PipelineProcessor:
    def __init__(self, skip_if_no_result_file, processors=None, event_handlers=None):
        """
        Process files wih multiple processors in a row
        @param skip_if_no_result_file: if a processor fails and doesn't give a result file just skip it and continue with the next one
        @param processors: a list of processors
        """
        self._processors = processors
        if processors is None:
            self._processors = []
        self._skip_if_no_result_file = skip_if_no_result_file
        self.event_handlers = event_handlers
        if event_handlers is None:
            self.event_handlers = []

    @processor
    def process_file(self, source_file: str, destination_file: str, file_ending: str="auto") -> None:
        current_source = source_file
        temp_files = []
        if file_ending == "auto":
            file_ending = source_file.split(".")[-1]

        try:
            with tempfile.TemporaryDirectory() as tempdir:
                for i, processor in enumerate(self._processors):
                    temp_destination = os.path.join(tempdir, f"temp_{i}"+file_ending)
                    try:
                        processor.process_file(current_source, temp_destination)
                        if os.path.exists(temp_destination):
                            current_source = temp_destination
                            temp_files.append(temp_destination)
                        elif not self._skip_if_no_result_file:
                            raise Exception(f"Processor {processor.__class__.__name__} failed")

                    except Exception as e:
                        if self._skip_if_no_result_file:
                            print(f"Processor {processor.__class__.__name__} failed with error: {e}")
                            continue
                        else:
                            raise e
                shutil.copy(current_source, destination_file)
        finally:
            # Cleanup temporary files
            for temp_file in temp_files:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
