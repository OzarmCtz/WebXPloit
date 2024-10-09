import logging
# cython: language_level=3


from pathlib import Path
import src.utils.generics.generic as UtilsGenerics
from config.params import ConfigConst


class CleanDatabaseEnvironment:
    def __init__(self):
        self.logger = UtilsGenerics.setup_logging(
            logger_name=f"{ConfigConst.LoggingConfig.LOGGER_OUTPUT_NAME}",
            log_file=ConfigConst.LoggingConfig.OUTPUT_FILE_PATH,
        )

        self.file_paths = [
            ConfigConst.DatabasePathConfig.IP_LIST_GENERATED_PATH,
            ConfigConst.DatabasePathConfig.IP_LIST_CHECKED_PATH,
            ConfigConst.DatabasePathConfig.IP_LIST_RANGED_FOR_DOMAIN,
            ConfigConst.DatabasePathConfig.IP_LIST_RANGED_FOR_IP,
            ConfigConst.DatabasePathConfig.DOMAIN_PATH,
        ]

    def run(self):
        self.logger.info(f"CleanDatabaseEnvironment Started ..")

        for file_path in self.file_paths:
            try:
                self.create_or_clear_file(Path(file_path))
            except Exception as e:
                self.logger.error(f"An error occurred while creating or clearing file {file_path}: {e}")

        self.logger.info(f"CleanDatabaseEnvironment Finished .")

        print(f"[{UtilsGenerics.ret_hour()}] CleanDatabaseEnvironment Process Done .")

    def create_or_clear_file(self, file_path: Path):
        try:
            # Create the file if it doesn't exist
            file_path.touch()

            # Clear the contents of the file if it exists
            file_path.write_text("")
        
            self.logger.debug(f"CleanDatabaseEnvironment of {Path(file_path)}")
        except IOError as e:
            self.logger.error(
                f"CleanDatabaseEnvironment : An error occurred while creating or clearing file {file_path}: {e}"
            )