import subprocess
import os
import conf
from pathlib import Path


class Setup:
    def __init__(self):
        self.project_dir = Path(__file__).resolve().parent
        self.source_path = self.project_dir / f"{conf.link_name}.py"
        self.link_path_mac = f"/usr/local/bin/{conf.link_name}"
        self.link_path_windows = f"/usr/local/bin/{conf.link_name}"
        self.os_type = conf.os_type

    def create_namespace(self):
        if self.os_type.lower() == "darwin" and not os.path.isfile(self.link_path_mac):
            subprocess.call(["ln", "-s", self.source_path, self.link_path_mac])
            subprocess.run(['chmod', '+x', self.source_path])
            print(f"Namespace '{conf.link_name}' created successfully.")

        if self.os_type.lower() == "windows" and not os.path.isfile(self.link_path_windows):
            command = ['netsh', 'namespace', 'add', 'prefix', conf.link_name, '1']
            subprocess.run(command, check=True)
            print(f"Namespace '{conf.link_name}' created successfully.")


if __name__ == '__main__':
    setup = Setup()

    setup.create_namespace()
