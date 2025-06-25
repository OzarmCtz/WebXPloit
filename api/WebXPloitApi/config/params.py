# cython: language_level=3

import logging
from pathlib import Path
from typing import Final, List

class ConfigApiConst:
    class GlobalApiConfig:
        # Application version and production date
        VERSION: Final[str] = "4.2.3 01/2/2023"
        API_NBR: Final[str] = "1"

    class LaunchApiConfig:
        # Address of the server where the API is running. (ensure it matches the information specified in api/WebXPloitBackend/config class LaunchApiConfig) 
        # It is recommended to use a different server than WebXPloitBackend for better load distribution.
        HOST: Final[str] = "127.0.0.1"
        PORT: Final[str] = "8000"

        # Number of threads for vulnerability checks.
        THREADS_API: Final[int] = 3

        # Enable to process requests related to Git folder exposure (dumping).
        GIT: Final[bool] = True

        # /!\ DO NOT MODIFY /!\ Not implemented yet
        SVN: Final[bool] = False

#   -------------------------------------------------------------------------------------------- /!\ DO NOT MODIFY /!\ --------------------------------------------------------------------------------------------

    class LoggingApiConfig:
        LOG_API_FOLDER_PATH: Final[Path] = Path("./output/log")
        OUTPUT_FILE_PATH: Final[Path] = LOG_API_FOLDER_PATH / "api.log"
        GIT_LOG_FILE_PATH: Final[Path] = LOG_API_FOLDER_PATH / "git.log"
        TG_SENDING_FAILED: Final[Path] = LOG_API_FOLDER_PATH / "tg_sending_failed.txt"
        LOGGER_OUTPUT_NAME: Final[str] = "api_logger"
        LOGGER_GIT_NAME: Final[str] = "git_logger"
        LOGGING_LEVEL: Final[str] = logging.DEBUG

    class CommonPathApiConfig:
        # Git dump and database names for API operations.
        GIT_DUMP_NAME: Final[str] = "dump"
        GIT_DATABASE_NAME: Final[str] = "database"

    @staticmethod
    def get_all_file_paths() -> List[Path]:
        file_paths = [
            # Uncomment the following lines to include specific file paths.
            # ConfigApiConst.CommonPathApiConfig.RESULT_SMTP,
            # ConfigApiConst.CommonPathApiConfig.RESULT_PHPMYADMIN,
            # ConfigApiConst.CommonPathApiConfig.RESULT_ADMINER,
            # ConfigApiConst.CommonPathApiConfig.RESULT_MYSQL,
            # ConfigApiConst.CommonPathApiConfig.RESULT_AWS_KEY,
            # ConfigApiConst.CommonPathApiConfig.RESULT_MAILGUN_KEY,
            # ConfigApiConst.CommonPathApiConfig.RESULT_VULN,
            # ConfigApiConst.CommonPathApiConfig.RESULT_TWILIO_KEY,
            # ConfigApiConst.LoggingApiConfig.TG_SENDING_FAILED,
        ]
        return file_paths
        
    @staticmethod
    def get_all_directory_paths() -> List[Path]:
        directory_paths = [
            # Uncomment the following lines to include specific directory paths.
            Path("../result"),
            Path("../log"),
            Path("./data"),
        ]
        return directory_paths
