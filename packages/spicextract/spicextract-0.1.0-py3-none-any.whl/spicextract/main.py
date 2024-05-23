import requests

import urllib3

from spicextract.common.args_parser import ArgsParser
from spicextract.common.proxmox_exporter import ProxmoxExporter

urllib3.disable_warnings()

if __name__ == "__main__":
    try:
        proxmox_exporter = ProxmoxExporter(ArgsParser())
        proxmox_exporter.extract_spice_data_from_proxmox_and_save_to_file()
    except requests.HTTPError as e:
        print(f"HTTP error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
