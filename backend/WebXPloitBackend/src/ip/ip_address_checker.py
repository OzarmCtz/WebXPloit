# cython: language_level=3


from queue import Queue
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
import threading
from config.params import ConfigConst

import src.utils.generics.generic as UtilsGenerics

import http.client


class IpAddressChecker:
    def __init__(self):
        self.file_lock = threading.Lock()
        self.path_file_list_ip_generated = (
            ConfigConst.DatabasePathConfig.IP_LIST_GENERATED_PATH
        )
        self.path_file_list_ip_checked = (
            ConfigConst.DatabasePathConfig.IP_LIST_CHECKED_PATH
        )
        self.num_threads_ip_checker = (
            ConfigConst.IpChecker.THREADS_CHECK_IP_FROM_GENERATOR
        )
        self.notifier = UtilsGenerics.TelegramNotifier()
        self.logger = UtilsGenerics.setup_logging(
            logger_name=f"{ConfigConst.LoggingConfig.LOGGER_OUTPUT_NAME}",
            log_file=ConfigConst.LoggingConfig.OUTPUT_FILE_PATH,
        )
        self.checked_ips = set()
        self.results_queue = Queue()

        self.ip_list_len = len(
            UtilsGenerics.read_content_file(self, self.path_file_list_ip_generated)
        )

        self.IP_LIST_RANGED_FOR_IP = (
            ConfigConst.DatabasePathConfig.IP_LIST_RANGED_FOR_IP
        )

    def run(self):
        print(
            f"[{UtilsGenerics.ret_hour()}] IpAddressCheckerV2 of {self.ip_list_len} IPV4 Adress Process Started .."
        )

        self.logger.info(
            f"IpAddressCheckerV2 : Checking {self.ip_list_len} IPV4 adress Started ..."
        )

        ip_list = UtilsGenerics.read_content_file(
            self, self.path_file_list_ip_generated
        )

        # Clear the result file
        open(self.path_file_list_ip_checked, "w").close()

        # Start the thread for recording results
        results_thread = threading.Thread(target=self.record_results)
        results_thread.start()

        with ThreadPoolExecutor(max_workers=self.num_threads_ip_checker) as executor:
            chunk_size = 100  # Set the chunk size
            ip_list = list(ip_list)  # Convert the set to a list
            chunks = [ip_list[i:i + chunk_size] for i in range(0, len(ip_list), chunk_size)]  # Split the IP list into chunks
            for chunk in chunks:
                executor.map(self.valid_ip, chunk)  # Process each chunk of IP addresses
  # Process each chunk of IP addresses

        # Wait for all tasks to be done
        self.results_queue.join()

        # Stop the results recording thread
        self.results_queue.put(None)
        results_thread.join()

        print(
            f"[{UtilsGenerics.ret_hour()}] IpAddressCheckerV2 of {self.ip_list_len} IPV4 Adress Process Done ."
        )

        self.logger.info(
            f"IpAddressCheckerV2 : Checking {self.ip_list_len} IPV4 adress Finsished ."
        )

        return

    def valid_ip(self, ip):
        ports = [80, 443]
        for port in ports:
            try:
                conn = http.client.HTTPConnection(ip, port, timeout=5)
                conn.request("HEAD", "/")
                response = conn.getresponse()
                if response.status == 200:
                    conn.close()
                    self.results_queue.put(ip)
                    break
                conn.close()
            except Exception:
                pass

    def record_results(self):
        ip_buffer = []
        while True:
            ip = self.results_queue.get()
            if ip is None:  # Signal to stop the thread
                break
            if ip not in self.checked_ips:
                self.checked_ips.add(ip)
                ip_buffer.append(ip)
                self.results_queue.task_done()

            if len(ip_buffer) >= 100:  # Adjust the buffer size as needed
                UtilsGenerics.push_result(
                    self, self.path_file_list_ip_checked, "\n".join(ip_buffer) + "\n"
                )
                ip_buffer = []

        if ip_buffer:  # Write any remaining IPs in the buffer
            UtilsGenerics.push_result(
                self, self.path_file_list_ip_checked, "\n".join(ip_buffer) + "\n"
            )
