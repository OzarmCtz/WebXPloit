# cython: language_level=3

import os


class FastViewResult:
    def __init__(self) -> None:
        self.result_folder_path = "../result"

    def run(self):
        self.count_lines_in_folder(self.result_folder_path)

    def count_lines_in_folder(self, folder):
        for file_name in os.listdir(folder):
            file_path = os.path.join(folder, file_name)
            # Check if it's a file and not a directory
            if os.path.isfile(file_path):
                try:
                    with open(file_path, "r", encoding="utf-8") as file:
                        lines = file.readlines()
                        print(f"{file_name}: {len(lines)} lines")
                except Exception as e:
                    print(f"Error reading file {file_name}: {e}")


FastViewResult().run()
