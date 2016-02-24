ps aux | grep python | grep sockChange.py | awk '{print $2}' |xargs kill -9
