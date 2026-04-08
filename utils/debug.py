from datetime import datetime

def print_debug(text:str='', end:str='\n'):
    now = datetime.now()
    time = now.strftime('%H:%M:%S.') + now.strftime('%f')[:2]
    print(f"[DEBUG {time}] " + text, end=end)
