import argparse
from urllib.parse import urlparse


class ArgsParser:
    """
        Parses and stores the command line arguments provided to the application.

        Attributes:
            base_url (str): The full URL of the Proxmox server.
            hostname (str): The hostname extracted from the base_url.
            username (str): User's Proxmox account username including the realm.
            password (str): Proxmox account password.
            node (str): Identifier for the Proxmox node.
            vm_id (int): The VM ID to fetch the SPICE file for.
            output_file (str): The name for the saved SPICE file.
            ssl_verify (bool): Flag to verify SSL connections.
        """
    base_url: str
    hostname: str
    username: str
    password: str
    node: str
    vm_id: int
    output_file: str
    ssl_verify: bool

    def __init__(self):
        parser = argparse.ArgumentParser(description='Proxmox SPICE File Downloader')
        parser.add_argument('-s', '--server', type=str, required=True, help='Proxmox host URL')
        parser.add_argument('-u', '--username', type=str, required=True, help='Proxmox username')
        parser.add_argument('-p', '--password', type=str, required=True, help='Proxmox password')
        parser.add_argument('-n', '--node', type=str, required=True, help='Proxmox node')
        parser.add_argument('-i', '--vm_id', type=int, required=True, help='VM ID')
        parser.add_argument('-o', '--output_file', type=str, required=True, help='Output SPICE file name')
        parser.add_argument('-v', '--ssl_verify', action='store_true', help='Verify ssl connection')

        args = parser.parse_args()

        self.base_url = args.server
        self.hostname = urlparse(self.base_url).hostname
        self.username = args.username

        if not self.username.__contains__('@'):
            raise ValueError(f'Username must contains "@" symbol with auth method. Example: {self.username}@pam')

        self.password = args.password
        self.node = args.node
        self.vm_id = args.vm_id
        self.output_file = args.output_file

        if not self.output_file.endswith('.vv'):
            self.output_file += '.vv'

        self.ssl_verify = args.ssl_verify
