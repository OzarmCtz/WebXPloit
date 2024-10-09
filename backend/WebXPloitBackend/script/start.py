# cython: language_level=3


import src.ip.ip_adress_generator as IpUtilityGenerator
import src.ip.ip_address_checker as IpUtilityChecker
import src.ip.ip_adress_ranger as IpAdressRanger
import src.reverse.reverse_ip as ReverseIpV1
from src.utils.specifics.clean_data_environment import CleanDatabaseEnvironment
from src.utils.specifics.remove_duplicates_results import RemoveDuplicatesLinesInResult
from config.params import ConfigConst
from src.vulnerability.start import StartProcessVuln


class StartProcess:
    def __init__(self):
        self.run_main_process()

    def run_main_process(self):
        CleanDatabaseEnvironment().run()
        IpUtilityGenerator.IPAddressGenerator().run()
        IpUtilityChecker.IpAddressChecker().run()
        IpAdressRanger.IpAdressRanger().run()
        if ConfigConst.LaunchConfig.DOMAIN:
            ReverseIpV1.ReverseIpV1().run()
        StartProcessVuln().run()
        RemoveDuplicatesLinesInResult()
