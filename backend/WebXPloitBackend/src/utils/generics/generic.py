# cython: language_level=3

import datetime
import json
import os
import logging
import random
import re
import threading
import warnings
import requests
from bs4 import BeautifulSoup, MarkupResemblesLocatorWarning
from config.params import ConfigConst
from pathlib import Path


def setup_logging(logger_name, log_file, level=ConfigConst.LoggingConfig.LOGGING_LEVEL):
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


class TelegramNotifier:
    def __init__(self):
        self.file_lock = threading.Lock()
        self.logger = setup_logging(
            logger_name=f"{ConfigConst.LoggingConfig.LOGGER_OUTPUT_NAME}",
            log_file=ConfigConst.LoggingConfig.OUTPUT_FILE_PATH,
        )
        if ConfigConst.LaunchConfig.APP_DEBUG:
            self.bot_token = ConfigConst.SecretConfig.BOT_TOKEN_DEBUG
            self.chat_id = ConfigConst.SecretConfig.BOT_CHAT_ID_DEBUG
        else:
            self.bot_token = ConfigConst.SecretConfig.BOT_TOKEN_PROD
            self.chat_id = ConfigConst.SecretConfig.BOT_CHAT_ID_PROD

        self.server_number = ConfigConst.GlobalConfig.SERVER_NBR
        self.version = ConfigConst.GlobalConfig.VERSION
        self.failed_log_path = ConfigConst.LoggingConfig.TG_SENDING_FAILED
        self.tg_enabled = ConfigConst.LaunchConfig.API_TELEGRAM

    def send_to_tg(self, message):
        if self.tg_enabled:
            message += f"\n\n<i>⚡️ Serv : {self.server_number}\n\n=> Version {self.version}</i>"

            data = {
                "chat_id": self.chat_id,
                "text": self.escape_html_except_in_valid_tags(message),
                "parse_mode": "HTML",
            }

            try:
                rep = requests.post(
                    f"https://api.telegram.org/bot{self.bot_token}/sendMessage",
                    data=data,
                )
                if rep.status_code != 200:
                    # If the first attempt fails, log the failure and try to send the failure notification
                    self.logger.error(f"Failed to send Telegram message: {rep.text}")
                    push_result(
                        self,
                        self.failed_log_path,
                        f"{self.escape_html_except_in_valid_tags(message)}\n",
                    )
            except requests.exceptions.RequestException as e:
                self.logger.error(
                    f"An exception occurred while sending Telegram message: {e} , with rep json : {rep.json()}"
                )
                # Attempt to log the failed message to a file
        else:
            return

    def escape_html_except_in_valid_tags(self, text):
        # Protège le contenu à l'intérieur des balises HTML valides
        protected_segments = []

        def protect_match(match):
            protected_segments.append(match.group(0))
            return f"__PROTECTED_SEGMENT_{len(protected_segments) - 1}__"

        text = re.sub(r"<[^<>]+>", protect_match, text)

        # Échappe les caractères < et >
        text = text.replace("<", "&lt;").replace(">", "&gt;")

        # Remplacement des marqueurs par les segments protégés originaux
        for i, segment in enumerate(protected_segments):
            text = re.sub(f"__PROTECTED_SEGMENT_{i}__", segment, text)

        return text


def remove_duplicates_and_empty_lines(self, file_path):
    with self.file_lock:
        try:
            with open(file_path, "r+") as file:
                unique_lines = set(file.read().splitlines())
                file.seek(0)
                file.writelines(f"{line}\n" for line in unique_lines if line)
                file.truncate()
        except Exception as e:
            self.logger.error(
                f"Error to remove_duplicates_and_empty_lines in file: {file_path}: {e}"
            )


def get_random_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPad; CPU OS 15_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.181 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; U; Android 11; en-us; SM-G991B Build/RP1A.200720.012) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/88.0.4324.181 Mobile Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/605.1.15",
    ]

    return random.choice(user_agents)


def ret_hour():
    now = datetime.datetime.now()
    heure_formattee = now.strftime(
        "%Y-%m-%d %H:%M:%S"
    )  # Enlève les trois derniers chiffres pour les millisecondes
    return heure_formattee


def push_result(self, path_file, content):
    with self.file_lock:
        try:
            with open(path_file, "a", encoding="utf-8") as file:
                if hasattr(content, "__iter__") and not isinstance(content, str):
                    # Si content est un itérable (comme un générateur) mais pas une chaîne de caractères
                    for item in content:
                        file.write(item)
                else:
                    # Si content est une seule chaîne de caractères
                    file.write(content)
        except Exception as e:
            self.logger_vuln.error(f"Error to push content in file: {path_file}: {e}")


def read_content_file(self, path_file):
    with self.file_lock:
        try:
            with Path(path_file).open("r") as file:
                content_per_line = set(file.read().splitlines())
            return content_per_line
        except Exception as e:
            self.logger.error(f"Error to read_content_file in file: {path_file}: {e}")


def generate_ip_range(self, ip_address, filepath):
    base_ip = ".".join(ip_address.split(".")[:-1])
    ip_range = [f"{base_ip}.{i}" for i in range(1, 256)]
    push_result(self, filepath, ("\n".join(ip_range) + "\n"))


def remove_duplicates_and_empty_entries(data):
    if isinstance(data, dict):
        new_data = {}
        for key, value in data.items():
            if isinstance(value, list):
                # Appliquer la suppression sur chaque liste dans le dictionnaire
                new_data[key] = remove_duplicates_and_empty_entries(value)
            else:
                # Conserver les autres valeurs telles quelles
                new_data[key] = value
        return new_data

    elif isinstance(data, list):
        seen = set()
        new_list = []
        for item in data:
            # Convertir en un type hachable pour la comparaison
            item_tuple = json.dumps(item, sort_keys=True)
            if item_tuple not in seen and item:
                seen.add(item_tuple)
                new_list.append(item)
        return new_list

    else:
        # Si le type de données n'est ni un dictionnaire ni une liste
        raise ValueError(
            "Le type de données JSON n'est ni une liste ni un dictionnaire"
        )


def parse_content(self, content, urlvuln):
    def log_warning(message, category, filename, lineno, file=None, line=None):
        self.logger_vuln.warning(
            f"parse_content / MarkupResemblesLocatorWarning in {urlvuln}: {message}"
        )

    with warnings.catch_warnings(record=True) as captured_warnings:
        warnings.showwarning = log_warning
        warnings.filterwarnings("always", category=MarkupResemblesLocatorWarning)

        # Essayer d'abord avec le parseur HTML
        soup = BeautifulSoup(content, "html.parser")

        # Vérifier si un MarkupResemblesLocatorWarning a été capturé
        if any(
            item.category == MarkupResemblesLocatorWarning for item in captured_warnings
        ):
            try:
                # Si oui, essayer avec le parseur XML
                soup = BeautifulSoup(content, "lxml-xml")
                self.logger_vuln.debug(
                    f"parse_content / Switched to lxml-xml parser for: {urlvuln}"
                )
            except Exception as e:
                self.logger_vuln.error(
                    f"parse_content / Error using lxml-xml parser in: {urlvuln} / {e}"
                )
                return None

        return soup


