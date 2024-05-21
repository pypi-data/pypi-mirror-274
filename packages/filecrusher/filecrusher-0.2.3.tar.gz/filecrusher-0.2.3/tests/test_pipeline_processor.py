import os
import shutil
import tempfile
from unittest import TestCase

from file_crusher import PipelineProcessor


class ProcessorA:
    def process_file(self, source, destination):
        with open(source, 'r') as src, open(destination, 'w') as dst:
            content = src.read()
            dst.write(content + "\nProcessed by A")


class ProcessorB:
    def process_file(self, source, destination):
        with open(source, 'r') as src, open(destination, 'w') as dst:
            content = src.read()
            dst.write(content + "\nProcessed by B")


class ProcessorC:
    def process_file(self, source, destination):
        with open(source, 'r') as src, open(destination, 'w') as dst:
            content = src.read()
            dst.write(content + "\nProcessed by C")


class TestPipelineProcessor(TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.input_file = os.path.join(self.test_dir, 'input.txt')
        self.output_file = os.path.join(self.test_dir, 'output.txt')

        with open(self.input_file, 'w') as f:
            f.write("Initial content")

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_pipeline_all_processors_succeed(self):
        processors = [ProcessorA(), ProcessorB(), ProcessorC()]
        pipeline = PipelineProcessor(True, processors=processors)
        pipeline.process_file(self.input_file, self.output_file)

        with open(self.output_file, 'r') as f:
            content = f.read()

        expected_content = "Initial content\nProcessed by A\nProcessed by B\nProcessed by C"
        self.assertEqual(content.strip(), expected_content)

    def test_pipeline_with_failed_processor(self):
        class FailingProcessor:
            def process_file(self, source, destination):
                raise Exception("Simulated failure")

        processors = [ProcessorA(), FailingProcessor(), ProcessorC()]
        pipeline = PipelineProcessor(True, processors=processors)
        pipeline.process_file(self.input_file, self.output_file)

        with open(self.output_file, 'r') as f:
            content = f.read()

        expected_content = "Initial content\nProcessed by A\nProcessed by C"
        self.assertEqual(content.strip(), expected_content)

    def test_pipeline_with_failed_processor_and_no_skipping(self):
        class FailingProcessor:
            def process_file(self, source, destination):
                raise Exception("Simulated failure")

        processors = [ProcessorA(), FailingProcessor(), ProcessorC()]
        pipeline = PipelineProcessor(False, processors=processors)
        self.assertRaises(Exception, pipeline.process_file, self.input_file, self.output_file)

        self.assertFalse(os.path.exists(self.output_file))
        expected_content = "Initial content"
        with open(self.input_file, 'r') as f:
            content = f.read()

        self.assertEqual(content.strip(), expected_content)

    def test_pipeline_with_quiet_failed_processor(self):
        class FailingProcessor:
            def process_file(self, source, destination):
                pass

        processors = [ProcessorA(), FailingProcessor(), ProcessorC()]
        pipeline = PipelineProcessor(True, processors=processors)
        pipeline.process_file(self.input_file, self.output_file)

        with open(self.output_file, 'r') as f:
            content = f.read()

        expected_content = "Initial content\nProcessed by A\nProcessed by C"
        self.assertEqual(content.strip(), expected_content)

    def test_pipeline_with_quiet_failed_processor_and_no_skipping(self):
        class FailingProcessor:
            def process_file(self, source, destination):
                pass

        processors = [ProcessorA(), FailingProcessor(), ProcessorC()]
        pipeline = PipelineProcessor(False, processors=processors)
        self.assertRaises(Exception, pipeline.process_file, self.input_file, self.output_file)

        self.assertFalse(os.path.exists(self.output_file))
        expected_content = "Initial content"
        with open(self.input_file, 'r') as f:
            content = f.read()

        self.assertEqual(content.strip(), expected_content)
