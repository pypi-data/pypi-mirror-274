from typing import Tuple

import requests

from spicextract.common.args_parser import ArgsParser


class ProxmoxExporter:
    """
        Handles the extraction and saving of SPICE data from Proxmox.

        Attributes:
            __args (ArgsParser): The arguments parser instance containing all command line options.
            __session (requests.session): The session object for making HTTP requests.
        """
    __args: ArgsParser
    __session: requests.session

    def __init__(self, args: ArgsParser):
        self.__args = args
        self.__session = requests.session()

    def extract_spice_data_from_proxmox_and_save_to_file(self):
        try:
            ticket, csrf_token = self.__get_proxmox_ticket()
            spice_file_data = self.__get_spice_file_data(ticket, csrf_token)
            self.__save_spice_file(spice_file_data, self.__args.output_file)
        finally:
            self.__session.close()

    def __get_proxmox_ticket(self) -> Tuple[str, str]:
        post_data = {
            'username': self.__args.username,
            'password': self.__args.password
        }

        response = self.__session.post(
            f"{self.__args.base_url}/api2/extjs/access/ticket",
            data=post_data,
            verify=self.__args.ssl_verify
        )

        if response.status_code != 200:
            raise requests.HTTPError(response.reason)

        response.raise_for_status()
        result = response.json()

        if result['success'] == 0:
            raise requests.HTTPError(f'Status code: {result["status"]}. Message: {result["message"]}')

        return result['data']['ticket'], result['data']['CSRFPreventionToken']

    def __get_spice_file_data(self, ticket: str, csrf_token: str) -> dict:
        headers = {
            'Cookie': f'PVEAuthCookie={ticket}',
            'Csrfpreventiontoken': csrf_token
        }

        response = self.__session.post(
            f"{self.__args.base_url}/api2/extjs/nodes/{self.__args.node}/qemu/{self.__args.vm_id}/spiceproxy",
            data={'proxy': self.__args.hostname},
            headers=headers,
            verify=self.__args.ssl_verify
        )

        if response.status_code != 200:
            raise requests.HTTPError(response.reason)

        response.raise_for_status()
        result = response.json()

        if result['success'] == 0:
            raise requests.HTTPError(f'Status code: {result["status"]}. Message: {result["message"]}')

        return result['data']

    @staticmethod
    def __save_spice_file(spice_file_data: dict, filename: str):
        if spice_file_data is None or len(spice_file_data) == 0:
            raise ValueError('Spice file data is NULL!')

        with open(filename, 'w') as file:
            file.write("[virt-viewer]\n")
            for key, value in sorted(spice_file_data.items()):
                file.write(f"{key}={value}\n")

        print(f'SPICE file saved as {filename}')
