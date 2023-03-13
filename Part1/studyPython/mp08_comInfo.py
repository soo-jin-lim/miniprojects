# mp08_comInfo.py
import psutil
import socket
import requests # 없을시 ' pip install requests ' 다운로드
import re

print(psutil.cpu_freq())

in_addr = socket.gethostbyname(socket.gethostname())
print(in_addr)