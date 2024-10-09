# cython: language_level=3


import ipaddress
import random
import threading

from config.params import ConfigConst

import src.utils.generics.generic as UtilsGenerics


class IPAddressGenerator:
    def __init__(self):
        self.file_lock = threading.Lock()
        self.logger = UtilsGenerics.setup_logging(
            logger_name=f"{ConfigConst.LoggingConfig.LOGGER_OUTPUT_NAME}",
            log_file=ConfigConst.LoggingConfig.OUTPUT_FILE_PATH,
        )
        self.nbr_ip_to_generate = ConfigConst.LaunchConfig.NBR_IP_TO_GENERATE
        self.ip_list_generated = ConfigConst.DatabasePathConfig.IP_LIST_GENERATED_PATH
        self.notifier = UtilsGenerics.TelegramNotifier()
        self.blacklist_ips = UtilsGenerics.read_content_file(
            self, ConfigConst.CommonPathConfig.BLACKLISTED_IP_PATH
        )
        self.BLACKLISTED_IP_PATH = ConfigConst.CommonPathConfig.BLACKLISTED_IP_PATH

    def run(self):
        print(
            f"[{UtilsGenerics.ret_hour()}] IPAddressGenerator of {self.nbr_ip_to_generate} IPV4 Adress Process Started .."
        )

        self.logger.info(
            f"IPAddressGenerator : Genarating of {self.nbr_ip_to_generate} IPV4 adress Started ..."
        )

        try:
            ip_set = set()
            blacklist_ips_set = set(self.blacklist_ips)
            for _ in range(self.nbr_ip_to_generate):
                ip = ipaddress.IPv4Address._string_from_ip_int(random.getrandbits(32))
                if str(ip) not in blacklist_ips_set.union(ip_set):
                    ip_set.add(str(ip))
        except Exception as e:
            self.logger.error(f"IPAddressGenerator : An error occurred: {e}")

        UtilsGenerics.push_result(
            self, self.ip_list_generated, (f"{ip}\n" for ip in ip_set if ip)
        )

        UtilsGenerics.push_result(
            self, self.BLACKLISTED_IP_PATH, (f"{ip}\n" for ip in ip_set if ip)
        )

        print(
            f"[{UtilsGenerics.ret_hour()}] IPAddressGenerator of {len(ip_set)} IPV4 Adress Process Done ."
        )

        self.logger.info(
            f"IPAddressGenerator : Genarating of {len(ip_set)} IPV4 adress Finished ."
        )
