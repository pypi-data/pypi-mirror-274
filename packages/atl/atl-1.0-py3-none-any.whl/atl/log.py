'''
Example:
  if __name__ == "__main__":
    log_enable()
    log("WARNING", LogColors.WARNING)
    log("Normal")
    log("HEADER", LogColors.HEADER)
    log("Normal")
    log("FAIL", LogColors.FAIL)
    log("Normal")
'''

class LogColor:
    HEADER    = '\033[95m'
    OKBLUE    = '\033[94m'
    OKCYAN    = '\033[96m'
    OKGREEN   = '\033[92m'
    WARNING   = '\033[93m'
    FAIL      = '\033[91m'
    ENDC      = '\033[0m'
    BOLD      = '\033[1m'
    UNDERLINE = '\033[4m'
    
_atl_log_enable = False

def log_isEnabled():
  return _atl_log_enable

def log_enable() -> None:
  global _atl_log_enable
  _atl_log_enable = True
  
def log_disable() -> None:
  global _atl_log_enable
  _atl_log_enable = False
  
def log(msg: str, color: LogColor = LogColor.ENDC) -> None:
  if(color != LogColor.ENDC):
    print(f'{color}[LOG] {msg}{LogColor.ENDC}')
  else:
    print(f'[LOG] {msg}')
    
