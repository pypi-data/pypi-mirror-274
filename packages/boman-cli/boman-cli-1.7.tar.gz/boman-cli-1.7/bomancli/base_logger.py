import coloredlogs, logging
# from Config import Config

from bomancli.Config import Config

# logging.basicConfig(filename='bomancli.log',  
#                 level=logging.INFO,format='%(asctime)s-%(message)s',
#                 datefmt='%Y-%m-%d %H:%M:%S')



# if Config.log_level == 'INFO':
#     logging.basicConfig(filename='bomancli.log',  
#                 level=logging.INFO,format='%(asctime)s-%(message)s',
#                 datefmt='%Y-%m-%d %H:%M:%S')

#coloredlogs.install(level='INFO')   


# if Config.log_level == 'DEBUG':    
#     logging.basicConfig(filename='bomancli.log',  
#                 level=logging.DEBUG,format='%(asctime)s-%(message)s',
#                 datefmt='%Y-%m-%d %H:%M:%S')


#     coloredlogs.install(level='DEBUG')   

class LogStream:
    def __init__(self):
        self.logs = ''

    def write(self, message):
        self.logs += message

    def flush(self):
        pass

# Set up logging to use our custom stream
Config.log_stream = LogStream()

logging.basicConfig(stream=Config.log_stream,  
                level=logging.DEBUG,format='%(asctime)s-%(message)s',
                datefmt='%Y-%m-%d %H:%M:%S')


coloredlogs.install(level='DEBUG')    