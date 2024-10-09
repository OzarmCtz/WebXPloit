# cython: language_level=3

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
import src.utils.generics.generic as GenericApiUtils
from config.params import ConfigApiConst
from pathlib import Path


class OnceMakeEnvironment:
    def __init__(self):
        # Configure the logger
        self.logger_environment = GenericApiUtils.setup_logging(
            logger_name=f"{ConfigApiConst.LoggingApiConfig.LOGGER_OUTPUT_NAME}",
            log_file=ConfigApiConst.LoggingApiConfig.OUTPUT_FILE_PATH,
        )

        self.logger_environment.info(f"OnceMakeApiEnvironment: Started .")

        # Create the necessary directories

        [self.create_directory(directory_path) for directory_path in ConfigApiConst.get_all_directory_paths()]

        [self.create_file(file_path) for file_path in ConfigApiConst.get_all_file_paths()]


        self.logger_environment.info(f"OnceMakeApiEnvironment : Finished .")
        print(f"[{GenericApiUtils.ret_hour()}] OnceMakeEnvironment Process Done .")

    def create_directory(self, path: Path):
        try:
            path.mkdir(parents=True, exist_ok=True)
            self.logger_environment.debug(
                f"OnceMakeApiEnvironment : Directory already {path}"
            )
        except OSError as e:
            self.logger_environment.error(
                f"OnceMakeApiEnvironment : An error occurred while creating directory {path}: {e}"
            )

    def create_file(self, file_path: Path):
        try:
            # The 'touch' method will create the file if it does not exist.
            file_path.touch(exist_ok=True)
            self.logger_environment.debug(
                f"OnceMakeApiEnvironment : File already {file_path}"
            )
        except IOError as e:
            self.logger_environment.error(
                f"OnceMakeApiEnvironment : An error occurred while creating file {file_path}: {e}"
            )
