# cython: language_level=3

import datetime
import logging
import os


def setup_logging(logger_name, log_file, level=logging.DEBUG):
    logger = logging.getLogger(logger_name)
    if not logger.handlers:
        logger.setLevel(level)

        # Vérifier si le répertoire parent existe, sinon le créer
        log_dir = os.path.dirname(log_file)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)

        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        file_formatter = logging.Formatter(log_format)
        file_handler.setFormatter(file_formatter)

        logger.addHandler(file_handler)

    return logger


def ret_hour():
    now = datetime.datetime.now()
    heure_formattee = now.strftime(
        "%Y-%m-%d %H:%M:%S"
    )  # Enlève les trois derniers chiffres pour les millisecondes
    return heure_formattee
