import logging

logger = logging.getLogger(name='logger')
formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(funcName)s : %(message)s')
logger.setFormatter(formatter)
logger.setLevel(logging.DEBUG)

filehandler = logging.FileHandler('log.txt')
filehandler.setLevel(logging.DEBUG)
filehandler.setFormatter(formatter)
logger.addHandler(filehandler)
