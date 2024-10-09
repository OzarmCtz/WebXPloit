# cython: language_level=3


import threading
import queue
import time
import httpx

from concurrent.futures import ThreadPoolExecutor
from config.params import ConfigConst
import src.utils.generics.generic as UtilsGenerics


class ReverseIpV1:
    def __init__(self):
        self.DAILY_LIMIT_MESSAGE = "Daily reverse IP check limit reached"
        self.PROXIES_PATH = ConfigConst.DatabasePathConfig.PROXIES_PATH
        self.DOMAINS_PATH = ConfigConst.DatabasePathConfig.DOMAIN_PATH
        self.IP_LIST_CHECKED = ConfigConst.DatabasePathConfig.IP_LIST_CHECKED_PATH
        self.IP_LIST_RANGED_FOR_DOMAIN = (
            ConfigConst.DatabasePathConfig.IP_LIST_RANGED_FOR_DOMAIN
        )
        self.NUM_THREADS_RV1 = ConfigConst.LaunchConfig.THREADS_RV1
        self.IP_LIST_BLACKLISTED = ConfigConst.CommonPathConfig.BLACKLISTED_IP_PATH
        self.REV_LOG_FILE_PATH = ConfigConst.LoggingConfig.REV_LOG_FILE_PATH
        self.proxy_queue = queue.Queue()
        self.penalty_queue = queue.Queue()
        self.file_lock = threading.Lock()
        self.load_initial_proxies()
        self.notifier = UtilsGenerics.TelegramNotifier()
        threading.Thread(target=self.restore_proxies, daemon=True).start()
        self.logger = UtilsGenerics.setup_logging(
            logger_name=f"{ConfigConst.LoggingConfig.LOGGER_OUTPUT_NAME}",
            log_file=ConfigConst.LoggingConfig.OUTPUT_FILE_PATH,
        )
        self.logger_rev = UtilsGenerics.setup_logging(
            logger_name=f"{ConfigConst.LoggingConfig.LOGGER_REV_NAME}",
            log_file=ConfigConst.LoggingConfig.REV_LOG_FILE_PATH,
        )

    def run(self):
        self.step_one()
        self.step_two()

    def step_one(self):
        self.logger.info(f"ReverseIpV1 step_one : Starting")
        print(
            f"[{UtilsGenerics.ret_hour()}] ReverseIpV1-Step-One Process Starting .. See {self.REV_LOG_FILE_PATH} for more informations"
        )
        ip_checked_in_list_path = UtilsGenerics.read_content_file(
            self, self.IP_LIST_CHECKED
        )

        with ThreadPoolExecutor(max_workers=self.NUM_THREADS_RV1) as executor:
            list(
                executor.map(
                    self.find_domain,
                    ip_checked_in_list_path,
                    ["true"] * len(ip_checked_in_list_path),
                )
            )

        self.logger.info(f"ReverseIpV1 step_one : Finished")
        print(f"[{UtilsGenerics.ret_hour()}] ReverseIpV1-Step-One Process Done .")

    def step_two(self):
        self.logger.info(f"ReverseIpV1 step_two : Starting")

        print(
            f"[{UtilsGenerics.ret_hour()}] ReverseIpV1-Step-Two Process Starting .. See {self.REV_LOG_FILE_PATH} for more informations"
        )

        ip_ranged_in_list_path = UtilsGenerics.read_content_file(
            self, self.IP_LIST_RANGED
        )

        UtilsGenerics.push_result(
            self, self.IP_LIST_BLACKLISTED, (f"{ip}\n" for ip in ip_ranged_in_list_path)
        )

        with ThreadPoolExecutor(max_workers=self.NUM_THREADS_RV1) as executor:
            list(
                executor.map(
                    self.find_domain,
                    ip_ranged_in_list_path,
                    ["false"] * len(ip_ranged_in_list_path),
                )
            )
        self.transform_domains_with_condition()

        # TMP TO REMOVE IF NOT INTERSTED
        list_domain = UtilsGenerics.read_content_file(self, self.DOMAINS_PATH)

        self.logger.info(f"ReverseIpV1 step_two : Finished")
        print(
            f"[{UtilsGenerics.ret_hour()}] ReverseIpV1-Step-Two (Domain founded : {len(list_domain)}) Process Done ."
        )

    def load_initial_proxies(self):
        initial_proxies = UtilsGenerics.read_content_file(self, self.PROXIES_PATH)
        for proxy in initial_proxies:
            self.proxy_queue.put(proxy)

    def add_proxy_to_penalty_queue(self, proxy):
        self.penalty_queue.put((proxy, time.time()))

    def restore_proxies(self):
        while True:
            if not self.penalty_queue.empty():
                proxy, timestamp = self.penalty_queue.get()
                elapsed_time = time.time() - timestamp
                if elapsed_time >= 1800:  # 30 minutes
                    self.proxy_queue.put(proxy)
                else:
                    self.penalty_queue.put(
                        (proxy, timestamp)
                    )  # Re-add to penalty queue
            else:
                time.sleep(60)  # Check every minute

    def remove_port_suffix(self, url):
        if url.endswith(":80"):
            return url[:-3]  # Remove the last 3 characters ":80"
        elif url.endswith(":443"):
            return url[:-4]  # Remove the last 4 characters ":443"
        else:
            return url

    def find_domain(self, ip, ranged):
        ip_formatted = self.remove_port_suffix(ip)
        max_retries = 3
        retries = 0
        proxy = None

        while retries < max_retries:
            if proxy is None:
                proxy = self.proxy_queue.get()

            url = "https://domains.yougetsignal.com/domains.php"
            payload = {"remoteAddress": ip_formatted, "key": "", "_": ""}
            headers = {
                "User-Agent": f"{UtilsGenerics.get_random_user_agent()}",
                "Pragma": "no-cache",
                "Accept": "*/*",
            }

            proxy_url = f"http://{proxy}"
            try:
                with httpx.Client(
                    proxies={"http://": proxy_url, "https://": proxy_url}, timeout=10
                ) as client:
                    response = client.post(url, data=payload, headers=headers)

                if response.status_code == 200:
                    data = response.json()
                    if (
                        "message" in data
                        and self.DAILY_LIMIT_MESSAGE in data["message"]
                    ):
                        self.logger_rev.warning(
                            f"ReverseIpV1 : DAILY_LIMIT_MESSAGE {proxy} BANNED"
                        )
                        self.add_proxy_to_penalty_queue(proxy)
                        proxy = None
                    elif "status" in data and data["status"] == "Success":
                        self.proxy_queue.put(proxy)
                        self.handle_domain_response(data, ip_formatted, ranged)
                        break
                    else:
                        self.add_proxy_to_penalty_queue(proxy)
                        proxy = None
                else:
                    self.add_proxy_to_penalty_queue(proxy)
                    proxy = None
            except Exception as e:
                self.add_proxy_to_penalty_queue(proxy)
                proxy = None
            retries += 1

        if retries == max_retries:
            self.logger_rev.warning(
                f"ReverseIpV1 : Reached max retries for IP : {ip_formatted}"
            )

    def handle_domain_response(self, data, ip, ranged):
        if int(data["domainCount"]) > 0:
            self.logger_rev.debug(
                f"ReverseIpV1 : {ip} | Domain Founded : {data['domainCount']}"
            )
            domains = [item[0] for item in data["domainArray"]]
            if ranged == "true":
                UtilsGenerics.generate_ip_range(ip, self.IP_LIST_RANGED_FOR_DOMAIN)
            UtilsGenerics.push_result(
                self, self.DOMAINS_PATH, ("\n".join(domains) + "\n")
            )
        else:
            self.logger_rev.debug(
                f"ReverseIpV1 : {ip} | Domain Founded : {data['domainCount']}"
            )

    def transform_domains_with_condition(self):
        domains_with_www = set()
        domains_without_www = set()

        # Lire et catégoriser les domaines
        with self.file_lock:
            try:
                with open(self.DOMAINS_PATH, "r") as file:
                    for line in file:
                        domain = line.strip().lower()
                        if domain.startswith("www."):
                            domains_with_www.add(domain)
                        else:
                            domains_without_www.add(domain)
            except Exception as e:
                self.logger.error(
                    f"ReverseIpV1 transform_domains_with_condition : Error file {self.DOMAINS_PATH}: {e}"
                )

        # Ajouter les domaines avec 'www.' uniquement s'il n'y a pas d'équivalent sans 'www.'
        final_domains = set(domains_without_www)
        for domain in domains_with_www:
            if domain[4:] not in domains_without_www:
                final_domains.add(domain)

        # Supprimer les doublons éventuels au sein de chaque catégorie
        combined_domains = set()
        for domain in final_domains:
            if domain.startswith("www."):
                if domain[4:] not in combined_domains:
                    combined_domains.add(domain)
            else:
                combined_domains.add(domain)

        # Réécrire dans le même fichier
        with self.file_lock:
            try:
                with open(self.DOMAINS_PATH, "w") as file:
                    for domain in sorted(combined_domains):
                        file.write(domain + "\n")
            except Exception as e:
                self.logger.error(
                    f"ReverseIpV1 transform_domains_with_condition : Error file {self.DOMAINS_PATH}: {e}"
                )
