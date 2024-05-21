import asyncio
from typing import List


async def batch_process_files_async(file_list: List[str], destination: str, processor):
    loop = asyncio.get_running_loop()
    tasks = [
        loop.run_in_executor(
            None,
            processor.process_file, file, destination)
        for file in file_list
    ]
    return await asyncio.gather(*tasks)


def batch_process_files(file_list: List[str], destination: str, processor):
    for file in file_list:
        processor.process_file(file, destination)
