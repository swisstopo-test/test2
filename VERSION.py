#!/usr/bin/env python
import subprocess
process = subprocess.Popen(["git", "tag", "--points-at", "HEAD"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
stdout, stderr = process.communicate()
git_version = stdout.decode('utf-8').strip()
if git_version == '':
    proc = subprocess.Popen(["git", "rev-parse", "--short", "HEAD"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    VERSION = stdout.decode('utf-8').strip()
else:
    VERSION = git_version
print(VERSION)
