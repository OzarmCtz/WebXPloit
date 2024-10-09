# cython: language_level=3

import json
import re
import threading
import requests
import src.utils.generics.generic as UtilsGenerics
from config.params import ConfigConst
from src.vulnerability.services.exploit_info import ExploitInfo
from urllib.parse import urlparse


class CheckHostBeforeVuln:
    def __init__(self):
        self.logger_vuln = UtilsGenerics.setup_logging(
            logger_name=f"{ConfigConst.LoggingConfig.LOGGER_VULN_NAME}",
            log_file=ConfigConst.LoggingConfig.VULN_LOG_FILE_PATH,
        )
        self.file_lock = threading.Lock()
        self.RESULT_OSINT = ConfigConst.CommonPathConfig.RESULT_OSINT
        self.exploit_info = ExploitInfo()
        self.pattern_aws = re.compile(
            r'"region":"(.*?)","accessKeyId":"(.*?)","secretAccessKey":"(.*?)"'
        )
        self.check_cve_shodan = ConfigConst.Vulnerability.CHK_CVE_SHODAN
        self.check_additional_info = (
            ConfigConst.Vulnerability.CHK_BFR_VULN_ADDITONAL_TRAITEMENT
        )

        self.path_shodan_cve = ConfigConst.CommonPathConfig.RESULT_SHODAN_CVE
        self.path_shodan_port = ConfigConst.CommonPathConfig.RESULT_SHODAN_PORT

    def run(self, url):
        session = requests.Session()

        session.headers.update(
            {
                "User-Agent": UtilsGenerics.get_random_user_agent(),
                "Accept-Language": "en-US,en;q=0.5",
            }
        )
        is_valid, response = self.try_request(session, url)
        if is_valid:
            if self.check_cve_shodan:
                self.save_cve_shodan(url)
            if self.check_additional_info:
                is_founded = self.find_debug_bar(response, url, session)
                return session, is_founded
            return session, False
        else:
            return None, None

    def save_cve_shodan(self, ip):
        parsed_url = urlparse(ip)
        hostname = parsed_url.hostname
        response = requests.get(f"https://internetdb.shodan.io/{hostname}", timeout=10)
        if response.status_code == 200:
            data = response.json()
            self.update_items(data.get("vulns", []), self.path_shodan_cve)

            # Gérer les ports
            self.update_items(data.get("ports", []), self.path_shodan_port)

    def update_items(self, items, filename):
        # Préparer le contenu à écrire dans le fichier
        content_to_write = [f"{item}\n" for item in items]

        # Écrire les nouvelles données dans le fichier
        UtilsGenerics.push_result(self, filename, content_to_write)

    def try_request(self, session, url):
        try:
            response = session.get(url, timeout=5, allow_redirects=True, verify=False)
            return True, response.text
        except (requests.ConnectionError, requests.Timeout, Exception):
            return False, None

    def extraire_informations_json(self, soup):
        # Utiliser une expression régulière pour extraire les informations
        match = self.pattern_aws.search(str(soup))

        # Vérifier si à la fois aws key id et aws secret key ont été trouvés
        if match and match.group(2) and match.group(3):
            # Construire un dictionnaire avec les données trouvées
            data = {
                "aws": [
                    {
                        "aws key id": match.group(2),
                        "aws secret key": match.group(3),
                        "aws region": match.group(1) if match else "",
                    }
                ]
            }
            return True, json.loads(json.dumps(data, indent=4))
        else:
            # Les informations clés n'ont pas été trouvées
            return False, None

    def find_debug_bar(self, response, url, session):
        soup = UtilsGenerics.parse_content(self, response, url)
        if soup is None:
            return
        djDebug_div = soup.find("div", {"id": "djDebug", "class": "djdt-hidden"})
        if djDebug_div is not None:
            UtilsGenerics.push_result(
                self, self.RESULT_OSINT, f"Django Debug Bar Founded : {url}\n"
            )
        if "/media/plg_system_debug/" in response or "phpdebugbar" in response:
            UtilsGenerics.push_result(
                self, self.RESULT_OSINT, f"Random Debug Bar Founded : {url}\n"
            )
        if "Symfony Web Debug Toolbar" in response:
            UtilsGenerics.push_result(
                self, self.RESULT_OSINT, f"Symfony Debug Bar Founded : {url}\n"
            )
        if "<h1>Please wait while your request is being verified...</h1>" in response:
            UtilsGenerics.push_result(
                self, self.RESULT_OSINT, f"URL Detected Bot : {url}\n"
            )
        if (
            "aws" in str(soup).lower()
            and "accessKeyId" in str(soup)
            and "secretAccessKey" in str(soup)
        ):
            founded, json = self.extraire_informations_json(soup)
            if founded:
                success = self.exploit_info.run(
                    json, url, f"{url} CheckAddrBeforeVuln", session
                )
                if success:
                    return True
        return False
