#!/usr/bin/env python3
# This software is distributed under the terms of the MIT License.
# Copyright (c) 2024 Dmitry Ponomarev.
# Author: Dmitry Ponomarev <ponomarevda96@gmail.com>

import os
import subprocess

repo_url = "git@github.com:RaccoonlabDev/mini_v2_node.git"

def main():
    print("hi")
    current_directory = os.getcwd()
    print("Current directory: ", current_directory)
    # Check if current directory is a git repository
    git_directory = os.path.join(current_directory, ".git")
    if os.path.exists(git_directory):
        print("Current directory is a git repository")
    else:
        print("Current directory is not a git repository")
        subprocess.run(["git", "clone", repo_url, current_directory, '--recursive'])
        subprocess.run(["make", "cyphal"])

if __name__ == "__main__":
    main()
