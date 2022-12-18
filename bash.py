import os
import subprocess
import platform

print(platform.platform())

os.environ['PATH'] += ':'+'/home/bjorn/humdrum-tools/humdrum/bin'
subprocess.run(['wsl', 'humdrum', '-h'], shell=True)

