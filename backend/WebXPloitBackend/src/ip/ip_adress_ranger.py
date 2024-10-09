# cython: language_level=3


from concurrent.futures import ThreadPoolExecutor
import ipaddress
import socket
import threading
import http.client
from config.params import ConfigConst
import src.utils.generics.generic as UtilsGenerics 


class IpAdressRanger:
    def __init__(self) -> None:
        self.file_lock = threading.Lock()
        self.logger = UtilsGenerics.setup_logging(
                logger_name=f"{ConfigConst.LoggingConfig.LOGGER_OUTPUT_NAME}",
                log_file=ConfigConst.LoggingConfig.OUTPUT_FILE_PATH,
            )
        self.IP_LIST_RANGED_FOR_IP = (
            ConfigConst.DatabasePathConfig.IP_LIST_RANGED_FOR_IP
        )
        self.path_file_list_ip_checked = (
            ConfigConst.DatabasePathConfig.IP_LIST_CHECKED_PATH
        )
        self.BLACK_LIST_IP = ConfigConst.CommonPathConfig.BLACKLISTED_IP_PATH
        self.notifier = UtilsGenerics.TelegramNotifier() 
        self.threads_ip_checker_for_ranger = ConfigConst.IpChecker.THREADS_CHECK_IP_FROM_RANGER
        self.threads_ip_checker_for_ranger_second = ConfigConst.IpChecker.THREADS_CHECK_IP_FROM_RANGER_SECOND
        self.PORTS = ConfigConst.IpChecker.PORT
        
        
    def run (self):
        ip_list_checked = UtilsGenerics.read_content_file(self, self.path_file_list_ip_checked)
        
        
        self.logger.info(
            f"IpAdressRanger of {len(ip_list_checked)} IPV4 Adresses Ranged Started."
        )
        print(
            f"[{UtilsGenerics.ret_hour()}] IpAdressRanger of {len(ip_list_checked)} IPV4 Adresses Ranged Started."
        )
        self.notifier.send_to_tg(
            f"[🛰] <b>SiteXplorer BOT</b> [🛰]\n\n<i>⚡️ STEPS TWO (1.5/2)\n\n⚡️ IPV4 To Range </i><b>{len(ip_list_checked)} ({len(ip_list_checked) * 255})</b> <i>\n\n⚡️ Status Started .. </i>"
        )
        
        
        all_results = []
        with ThreadPoolExecutor(max_workers=self.threads_ip_checker_for_ranger) as executor:
            for result in executor.map(self.generate_ip_range_v2, ip_list_checked):
                all_results.extend(result)
        self.write_all_results(self.IP_LIST_RANGED_FOR_IP, all_results)

        

        ip_list_ranged_for_ip = UtilsGenerics.read_content_file(self, self.IP_LIST_RANGED_FOR_IP)
        
        
        UtilsGenerics.push_result(
            self, self.BLACK_LIST_IP, (ip.split(':')[0] + "\n" for ip in ip_list_ranged_for_ip)
        )

        

        self.logger.info(
            f"IpAdressRanger : {len(ip_list_ranged_for_ip)} Live IPV4 adress founded wtih IpAdressRanger."
        )
        print(
            f"[{UtilsGenerics.ret_hour()}] IpAdressRanger ({len(ip_list_ranged_for_ip)} Live IPV4 Adress) Process Done ."
        )
        self.notifier.send_to_tg(
            f"[🛰] <b>SiteXplorer BOT</b> [🛰]\n\n<i>⚡️ STEPS TWO (2/2)\n\n⚡️ LIVE IPV4 : </i><b>{len(ip_list_ranged_for_ip)}</b><i>\n\n⚡️ Status : Finished . </i>"
        )
        self.logger.info(
            f"IpAdressRanger : Checking {len(ip_list_ranged_for_ip)} IPV4 adress finished ."
        )
        return
        
        
    def generate_ip_range_v2(self, ip_range):
        with ThreadPoolExecutor(max_workers=self.threads_ip_checker_for_ranger_second) as executor:
            ip_formatted = self.transform_ip(ip_range)
            futures = [executor.submit(self.check_list_ranged, str(ip)) for ip in ipaddress.IPv4Network(f"{ip_formatted}/24")]
            results = [future.result() for future in futures if future.result() is not None]

        return [f"{result}\n" for result in results]



    def push_result(self, path_file, content):
        """Ajoute le contenu au tampon. Écrit dans le fichier si le tampon est plein."""
        with self.file_lock:
            if hasattr(content, "__iter__") and not isinstance(content, str):
                self.result_buffer.extend(content)
            else:
                self.result_buffer.append(content)

            if len(self.result_buffer) >= self.buffer_size:
                self.flush_buffer(path_file)
                
                

    def transform_ip(self , ip_address):
        parts = ip_address.split('.')
        parts[-1] = '0'
        return '.'.join(parts)

    def check_list_ranged(self, ip):
        for port in self.PORTS:
            try:
                conn = http.client.HTTPConnection(ip, port, timeout=5)
                conn.request("HEAD", "/")
                response = conn.getresponse()
                if response.status == 200:
                    conn.close()
                    return f"{ip}:{port}"
                conn.close()
            except Exception:
                continue
        return None
    
    def write_all_results(self, path_file, content):
        with self.file_lock:
            try:
                with open(path_file, "a", encoding="utf-8") as file:
                    file.writelines(content)
            except Exception as e:
                self.logger.error(f"Error writing to file: {path_file}: {e}")