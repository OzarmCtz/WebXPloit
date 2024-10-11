# cython: language_level=3

import os
import logging
from pathlib import Path
from typing import Final, List


class ConfigConst:
    class GlobalConfig:
        # Application version and production date
        VERSION: Final[str] = "7.2.1 01/14/2023"
        SERVER_NBR: Final[str] = "1"

    class LaunchConfig:
        # Flag to enable IP generation
        IP: Final[bool] = True

        # Number of IP addresses to generate
        NBR_IP_TO_GENERATE: Final[int] = 5000

        # Enable to include domain list linked to the generated IPs for vulnerability scanning (requires proxies in backend/WebXPloitBackend/data/proxies; not recommended)
        DOMAIN: Final[bool] = False

        # Number of threads for reverse IP lookups if DOMAIN is enabled
        THREADS_RV1: Final[int] = 20

        # Number of threads for vulnerability testing
        THREADS_CHEK_VULNS: Final[int] = 10

        # Enable to receive alerts via Telegram ChatBot (not recommended)
        API_TELEGRAM: Final[bool] = False

        # Enable to modify script behavior for debugging purposes (not recommended)
        APP_DEBUG: Final[bool] = True

    class ApiConfig:
        # Address where WebXPloitApi is running (ensure it matches the information specified in api/WebXPloitApi/config class LaunchApiConfig) 
        # It is recommended to use a different server from WebXPloitBackend for better load distribution.
        API_PORT: Final[str] = "8000"
        API_IP: Final[str] = "127.0.0.1"

    class IpChecker:
        # Number of threads for validating generated IP addresses
        THREADS_CHECK_IP_FROM_GENERATOR: Final[int] = 1000

        # List of ports to check for Ip availability
        PORT: Final[List[int]] = [8080, 8443, 80, 443]  

        # Thread settings for IP validation; /!\ DO NOT MODIFY /!\
        THREADS_CHECK_IP_FROM_RANGER: Final[int] = 5
        THREADS_CHECK_IP_FROM_RANGER_SECOND: Final[int] = 100

    class Vulnerability:
        # Enable Git folder exposure check (need to use WebXPloitApi for this) 
        GIT: Final[bool] = True

        # Enable .env file exposure check
        ENV: Final[bool] = True

        # Enable AWS file exposure check
        AWS: Final[bool] = True

        # Enable Yii Debug Bar exposure check
        YII: Final[bool] = True

        # Enable PHP Info file exposure check
        PHPINFO: Final[bool] = True

        # /!\DO NOT ENABLE /!\: Exploit is illegal. 

        # Joomla CVE DB (4.0.0 <= Joomla <= 4.2.7)
        CVE_2023_23752: Final[bool] = False 

        # Enable additional vulnerability checks (not recommended)
        CHK_BFR_VULN_ADDITONAL_TRAITEMENT: Final[bool] = False
        CHK_CVE_SHODAN: Final[bool] = False

    class SecretConfig:
        # Add Telegram keys in backend/WebXploitBackend/config/.env if API_TELEGRAM = True

        # Telegram ChatBot Token for production environment
        BOT_TOKEN_PROD: Final[str] = os.getenv("BOT_TOKEN_PROD")
        BOT_CHAT_ID_PROD: Final[str] = os.getenv("BOT_CHAT_ID_PROD")

        # Telegram ChatBot Token for debugging
        BOT_TOKEN_DEBUG: Final[str] = os.getenv("BOT_TOKEN_DEBUG")
        BOT_CHAT_ID_DEBUG: Final[str] = os.getenv("BOT_CHAT_ID_DEBUG")

    #   -------------------------------------------------------------------------------------------- /!\ DO NOT MODIFY /!\ --------------------------------------------------------------------------------------------

    class LoggingConfig:
        # Configuration for output and logging directories
        OUTPUT_FOLDER_PATH: Final[Path] = Path("./output")
        LOG_FOLDER_PATH: Final[Path] = OUTPUT_FOLDER_PATH / "log"
        OUTPUT_FILE_PATH: Final[Path] = LOG_FOLDER_PATH / "output.log"
        REV_LOG_FILE_PATH: Final[Path] = LOG_FOLDER_PATH / "reverse.log"
        VULN_LOG_FILE_PATH: Final[Path] = LOG_FOLDER_PATH / "vuln.log"
        CVELOG_FILE_PATH: Final[Path] = LOG_FOLDER_PATH / "cve.log"
        TG_SENDING_FAILED: Final[Path] = LOG_FOLDER_PATH / "tg_sending_failed.txt"
        CVE_OUTPUT_NAME: Final[str] = "cve_logger"
        LOGGER_OUTPUT_NAME: Final[str] = "output_logger"
        LOGGER_REV_NAME: Final[str] = "reverse_logger"
        LOGGER_VULN_NAME: Final[str] = "vuln_logger"
        LOGGING_LEVEL: Final[str] = logging.INFO

    class CommonPathConfig:
        # Configuration for output and result directories
        OUTPUT_FOLDER_PATH: Final[Path] = Path("./output")
        RESULT_FOLDER_PATH: Final[Path] = OUTPUT_FOLDER_PATH / "result"
        RESULT_SMTP: Final[Path] = RESULT_FOLDER_PATH / "smtp.txt"
        RESULT_PHPMYADMIN: Final[Path] = RESULT_FOLDER_PATH / "phpmyadmin.txt"
        RESULT_ADMINER: Final[Path] = RESULT_FOLDER_PATH / "adminer.txt"
        RESULT_MYSQL: Final[Path] = RESULT_FOLDER_PATH / "mysql.txt"
        RESULT_AWS_KEY: Final[Path] = RESULT_FOLDER_PATH / "aws.txt"
        RESULT_MAILGUN_KEY: Final[Path] = RESULT_FOLDER_PATH / "mailgun.txt"
        RESULT_TWILIO_KEY: Final[Path] = RESULT_FOLDER_PATH / "twilio.txt"
        RESULT_VULN: Final[Path] = RESULT_FOLDER_PATH / "hits.txt"
        RESULT_OSINT: Final[Path] = RESULT_FOLDER_PATH / "osint.txt"
        RESULT_CPANEL: Final[Path] = RESULT_FOLDER_PATH / "cpanel.txt"
        RESULT_JOOMLA: Final[Path] = RESULT_FOLDER_PATH / "joomla.txt"
        RESULT_SHODAN_CVE: Final[Path] = RESULT_FOLDER_PATH / "shodan_cve.txt"
        RESULT_SHODAN_PORT: Final[Path] = RESULT_FOLDER_PATH / "shodan_port.txt"
        BLACKLISTED_IP_PATH: Final[Path] = OUTPUT_FOLDER_PATH / "ip_blacklisted.txt"

    class DatabasePathConfig:
        # Configuration for database and data directories
        DB_FOLDER_PATH: Final[Path] = Path("./data")
        IP_LIST_GENERATED_PATH: Final[Path] = DB_FOLDER_PATH / "ip_list_generated.txt"
        IP_LIST_CHECKED_PATH: Final[Path] = DB_FOLDER_PATH / "ip_list_checked.txt"
        PROXIES_PATH: Final[Path] = DB_FOLDER_PATH / "proxies.txt"
        IP_LIST_RANGED_FOR_DOMAIN: Final[Path] = (
            DB_FOLDER_PATH / "ip_list_ranged_for_domain.txt"
        )
        IP_LIST_RANGED_FOR_IP: Final[Path] = (
            DB_FOLDER_PATH / "ip_list_ranged_for_ip.txt"
        )
        DOMAIN_PATH: Final[Path] = DB_FOLDER_PATH / "domains.txt"

    @staticmethod
    def get_all_file_paths() -> List[Path]:
        # Retrieves all relevant file paths for the application
        file_paths = [
            ConfigConst.DatabasePathConfig.IP_LIST_GENERATED_PATH,
            ConfigConst.DatabasePathConfig.IP_LIST_CHECKED_PATH,
            ConfigConst.DatabasePathConfig.PROXIES_PATH,
            ConfigConst.DatabasePathConfig.IP_LIST_RANGED_FOR_DOMAIN,
            ConfigConst.DatabasePathConfig.IP_LIST_RANGED_FOR_IP,
            ConfigConst.DatabasePathConfig.DOMAIN_PATH,
            ConfigConst.CommonPathConfig.RESULT_SMTP,
            ConfigConst.CommonPathConfig.RESULT_PHPMYADMIN,
            ConfigConst.CommonPathConfig.RESULT_ADMINER,
            ConfigConst.CommonPathConfig.RESULT_MYSQL,
            ConfigConst.CommonPathConfig.RESULT_AWS_KEY,
            ConfigConst.CommonPathConfig.RESULT_MAILGUN_KEY,
            ConfigConst.CommonPathConfig.BLACKLISTED_IP_PATH,
            ConfigConst.CommonPathConfig.RESULT_VULN,
            ConfigConst.CommonPathConfig.RESULT_TWILIO_KEY,
            ConfigConst.CommonPathConfig.RESULT_OSINT,
            ConfigConst.CommonPathConfig.RESULT_CPANEL,
            ConfigConst.CommonPathConfig.RESULT_JOOMLA,
            ConfigConst.CommonPathConfig.RESULT_SHODAN_CVE,
            ConfigConst.CommonPathConfig.RESULT_SHODAN_PORT,
            ConfigConst.LoggingConfig.TG_SENDING_FAILED,
        ]
        return file_paths

    @staticmethod
    def get_all_directory_paths() -> List[Path]:
        # Retrieves all relevant directory paths for the application
        directory_paths = [
            Path("./output/result"),
            Path("./output/log"),
            Path("./data"),
        ]
        return directory_paths
