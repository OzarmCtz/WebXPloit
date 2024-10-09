# cython: language_level=3


import src.utils.generics.generic as UtilsGenerics
from config.params import ConfigConst
from pathlib import Path


class OnceMakeEnvironment:
    def __init__(self):
        # Configure the logger
        self.logger = UtilsGenerics.setup_logging(
            logger_name=f"{ConfigConst.LoggingConfig.LOGGER_OUTPUT_NAME}",
            log_file=ConfigConst.LoggingConfig.OUTPUT_FILE_PATH,
        )

        self.logger.info(f"OnceMakeEnvironment : Started .")

        [
            self.create_directory(directory_path)
            for directory_path in ConfigConst.get_all_directory_paths()
        ]

        [self.create_file(file_path) for file_path in ConfigConst.get_all_file_paths()]

        self.logger.info(f"OnceMakeEnvironment : Finished .")
        print(f"[{UtilsGenerics.ret_hour()}] OnceMakeEnvironment Process Done .")

    def create_directory(self, path: Path):
        try:
            path.mkdir(parents=True, exist_ok=True)
            self.logger.debug(f"OnceMakeEnvironment : Directory already {path}")
        except OSError as e:
            self.logger.error(
                f"OnceMakeEnvironment : An error occurred while creating directory {path}: {e}"
            )

    def create_file(self, file_path: Path):
        try:
            # The 'touch' method will create the file if it does not exist.
            file_path.touch(exist_ok=True)
            self.logger.debug(f"OnceMakeEnvironment : File already {file_path}")
        except IOError as e:
            self.logger.error(
                f"OnceMakeEnvironment : An error occurred while creating file {file_path}: {e}"
            )


OnceMakeEnvironment()
