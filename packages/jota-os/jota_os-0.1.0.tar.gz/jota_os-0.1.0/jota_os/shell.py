# shell.py

import argparse
import git
import os
import re
import shlex
from jpu.api import jpuAPI as j
from jpu.runners.python import PythonRunner
from .nfs import FileSystem
from .network import Network
from .processes import ProcessManager
from .ai import AIRunner

class Shell:
    def __init__(self, include_ai=False):
        self.input = "jota-os:/home"
        self.fs = FileSystem()
        self.network = Network()
        self.pm = ProcessManager()
        self.ai_runner = AIRunner() if include_ai else None
        self.python_runner = PythonRunner()
        self.api =j()

    def sanitize_input(self, user_input):
        allowed_pattern = re.compile(r'[a-zA-Z0-9\s\-_\./]')
        sanitized_input = ''.join(char for char in user_input if allowed_pattern.match(char))
        return sanitized_input

    def run(self):
        while True:
            self.prompt = f"{self.input}{os.getcwd()}> "
            try:
                command = input(self.prompt)
                command = self.sanitize_input(command)
            except ValueError as e:
                print(e)
                continue

            if command.startswith("cd"):
                _, dirname = command.split()
                try:
                    self.api.chdir(dirname)
                    print(f"Changed directory to {dirname}.")
                except FileNotFoundError:
                    print(f"Directory {dirname} does not exist.")
            elif command.startswith("mkdir"):
                _, dirname = command.split()
                self.api.mkdir(dirname)
                print(f"Directory {dirname} created.")
            elif command.startswith("ls"):
                contents = self.api.listdir('.')
                print("\n".join(contents))
            elif command.startswith("connect"):
                _, host, port = command.split()
                print(self.network.connect(host, int(port)))
            elif command.startswith("download"):
                _, url, destination = command.split()
                print(self.fs.download(url, destination))
            elif command.startswith("get_file"):
                _, path = command.split()
                print(self.fs.get_file(path))
            elif command.startswith("git add"):
                _, *files = command.split()
                try:
                    repo = git.Repo(os.getcwd())
                    repo.index.add(files)
                    print(f"Added files: {' '.join(files)}")
                except Exception as e:
                    print(f"Error adding files: {e}")
            elif command.startswith("git checkout"):
                _, branch = command.split()
                try:
                    git.Repo.checkout(branch)
                    print(f"Checked-out branch {branch}.")
                except Exception as e:
                    print(f"Error checking-out branch: {e}")
            elif command.startswith("git clone"):
                _, repo_url, repo_path = command.split()
                try:
                    git.Repo.clone_from(repo_url, repo_path)
                    print(f"Cloned repository {repo_url} to {repo_path}.")
                except Exception as e:
                    print(f"Error cloning repository: {e}")
            elif command.startswith("git commit"):
                _, *message = command.split()
                try:
                    repo = git.Repo(os.getcwd())
                    repo.index.commit(' '.join(message))
                    print(f"Committed with message: {' '.join(message)}")
                except Exception as e:
                    print(f"Error committing: {e}")
            elif command.startswith("git diff"):
                _, *message = command.split()
                try:
                    repo = git.Repo(os.getcwd())
                    changes = repo.index.diff()
                    print(f"Current change log: {changes}")
                except Exception as e:
                    print(f"Error committing: {e}")
            elif command.startswith("git pull"):
                try:
                    repo = git.Repo(os.getcwd())
                    repo.remotes.origin.pull()
                    print("Pulled from remote repository.")
                except Exception as e:
                    print(f"Error pulling from repository: {e}")
            elif command.startswith("git push"):
                try:
                    repo = git.Repo(os.getcwd())
                    repo.remotes.origin.push()
                    print("Pushed to remote repository.")
                except Exception as e:
                    print(f"Error pushing to repository: {e}")
            elif command.startswith("git status"):
                try:
                    print("Current status")
                    repo = git.Repo(os.getcwd())
                    print(f"Files to be committed: {repo.untracked_files}")
                    print("Files changed:")
                    diffs = repo.index.diff(None)
                    for d in diffs:
                        print(f"File at {d.a_path}: {d.change_type}")
                    
                except Exception as e:
                    print(f"Error getting status: {e}")
            elif command.startswith("grep"):
                _, string, *filenames = command.split()
                for filename in filenames:
                    try:
                        with open(filename, 'r') as file:
                            for line in file:
                                if re.search(string, line):
                                    print(line, end='')
                    except FileNotFoundError:
                        print(f"File {filename} not found.")
            elif command.startswith("load_model"):
                _, data = command.split(maxsplit=1)
                self.ai_runner.load_model([int(x) for x in data.split()])
                print("Model loaded.")
            elif command.startswith("python run"):
                _, script_path = command.split()
                self.python_runner.run_script(script_path)
            elif command.startswith("python install"):
                package_name = command.split()[-1]
                self.python_runner.run_pip_command(['install', package_name])
            elif command.startswith("python uninstall"):
                package_name = command.split()[-1]
                self.python_runner.run_pip_command(['uninstall', '-y', package_name])
            elif command.startswith("python list"):
                self.python_runner.run_pip_command(['list'])
            elif command.startswith("rm"):
                _, path = command.split()
                self.api.rm(path)
                print(f"Removed {path}.")
            elif command.startswith("run"):
                _, *cmd = command.split()
                print(self.pm.run_command(' '.join(cmd)))
            elif command.startswith("pwd"):
                print(os.getcwd())
            elif command.startswith("run_inference"):
                _, instructions = command.split(maxsplit=1)
                instr = parse_instructions(instructions)
                if instr:
                    print(f"Inference result: {self.ai_runner.run_inference(instr)}")
            elif command.startswith("send"):
                _, index, message = command.split(maxsplit=2)
                print(self.network.send(int(index), message))
            elif command in ["q", "quit", "exit"]:
                break
            else:
                print("Unknown command.")

def main():
    parser = argparse.ArgumentParser(description="Start the jota-os shell")
    parser.add_argument('--include_ai', action='store_true', help="Include AI Runner in the shell")
    args = parser.parse_args()
    
    shell = Shell(include_ai=args.include_ai)
    print("Starting the jota-os shell") 
    shell.run()
