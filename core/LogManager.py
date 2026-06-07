from loguru import logger

class LogManager:
    def __init__(self):
        self.log = logger
    
    def info(self,message:str):
        self.log.info(message)
    
    def warn(self,message:str):
        self.log.warning(message)
    
    def debug(self,message:str):
        self.log.debug(message)

    def exception(self,message:str):
        self.log.exception(message)
    
    def error(self,message:str):
        self.log.error(message)
    


log = LogManager()
