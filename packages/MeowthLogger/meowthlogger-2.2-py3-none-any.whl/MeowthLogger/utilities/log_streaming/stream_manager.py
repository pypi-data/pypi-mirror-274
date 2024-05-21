class Stream:
    def setup_logger(self, logger):
        self.logger = logger
    
    def write(self, message: str):
        raise NotImplementedError