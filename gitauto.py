#!/usr/bin/env python3

"""
══════════════════════════════════════════════════════════
 ██████╗ ██╗████████╗   █████╗ ██╗   ██╗████████╗ ██████╗
██╔════╝ ██║╚══██╔══╝  ██╔══██╗██║   ██║╚══██╔══╝██╔═══██╗
██║  ███╗██║   ██║     ███████║██║   ██║   ██║   ██║   ██║
██║   ██║██║   ██║     ██╔══██║██║   ██║   ██║   ██║   ██║
╚██████╔╝██║   ██║     ██║  ██║╚██████╔╝   ██║   ╚██████╔╝
 ╚═════╝ ╚═╝   ╚═╝     ╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝
══════════════════════════════════════════════════════════
by: Vlad Haidaichuk
version: 1.0.0
license: MIT
"""

by = "Vlad Haidaichuk"
version = "1.0.0"
license = "MIT"

import os
import time
from github import Github
import click
import subprocess
from pathlib import Path
import platform




os_type = platform.system()


cli = click.Group()


@click.command("auto")
@click.option('--github-token', help='Your GitHub Personal Access Token')
@click.option('--repo-owner', help='Owner of the GitHub repository')
@click.option('--repo-name', help='Name of the GitHub repository')
@click.option('--local-path', help='Local path to the cloned repository')
def auto_pull(github_token, repo_owner, repo_name, local_path):
    """Track changes on a GitHub repository and perform auto-pull if changes are detected."""

    current_path = os.getcwd()
    try:
        with open(f"{current_path}/.gitauto", mode="r") as conf_file:
            lines = conf_file.read().split("\n")
            configs = [line.split('=') for line in lines]
            configs = {key: value for key, value in configs}
            github_token = configs["TOKEN"]
            repo_owner = configs["OWNER"]
            repo_name = configs["REPO-NAME"]
            local_path = current_path

    except FileNotFoundError as FoundError:
        pass

    if github_token is None:
        return print("Error: Option github-token not transferred")
    if repo_owner is None:
        return print("Error: Option repo-owner not transferred")
    if repo_name is None:
        return print("Error: Option repo-name not transferred")
    if local_path is None:
        return print("Error: Option local-path not transferred")

    # Connect to GitHub using the token
    g = Github(github_token)

    # Get the repository
    repo = g.get_repo(f"{repo_owner}/{repo_name}")

    # Save the last commit used for updating
    last_commit_sha = None

    try:
        while True:
            # Get the latest commit on the default branch
            latest_commit = repo.get_commits()[0]
            latest_commit_sha = latest_commit.sha

            # Compare commit SHAs, if they differ, perform a pull
            if last_commit_sha is None or last_commit_sha != latest_commit_sha:
                print("Detected new commit. Performing git pull.")
                os.chdir(local_path)
                os.system("git pull")
                print("Local copy updated successfully.")
                last_commit_sha = latest_commit_sha

            # Wait before the next iteration
            time.sleep(300)  # Wait for 5 minutes before the next check

    except KeyboardInterrupt:
        print("Exiting...")


@click.command("config")
@click.option('--github-token', prompt='GitHub Token', help='Your GitHub Personal Access Token')
@click.option('--repo-owner', prompt='Repository Owner', help='Owner of the GitHub repository')
@click.option('--repo-name', prompt='Repository Name', help='Name of the GitHub repository')
def init(github_token, repo_owner, repo_name):
    """Create init file to auto pull"""
    current_path = os.getcwd()
    with open(f"{current_path}/.gitauto", mode="w") as conf_file:
        conf_file.write(
            f"TOKEN={github_token}\n"
            f"OWNER={repo_owner}\n"
            f"REPO-NAME={repo_name}"
        )

class Setup:
    def __init__(self):
        self.project_dir = Path(__file__).resolve().parent
        self.link_name = "gitauto"
        self.dir_name = "gitauto"
        self.source_path = self.project_dir / f"{self.link_name}.py"
        self.link_path_mac = f"/usr/local/bin/{self.link_name}"
        self.link_path_windows = f"/usr/local/bin/{self.link_name}"

    def create_namespace(self):
        if os_type.lower() == "darwin":
            subprocess.call(["ln", "-s", self.source_path, self.link_path_mac])
            subprocess.run(['chmod', '+x', self.source_path])
            print(f"Namespace '{self.link_name}' created successfully.")

        if os_type.lower() == "windows":
            command = ['netsh', 'namespace', 'add', 'prefix', self.link_name, '1']
            subprocess.run(command, check=True)
            print(f"Namespace '{self.link_name}' created successfully.")


if __name__ == "__main__":
    setup = Setup()
    setup.create_namespace()
    cli.add_command(init)
    cli.add_command(auto_pull)
    cli()
