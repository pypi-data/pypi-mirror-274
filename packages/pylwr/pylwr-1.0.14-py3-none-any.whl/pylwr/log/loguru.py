import sys
from loguru import logger

logger.add(sys.stderr, level="CRITICAL", format="{time} {level} {message}", colorize=True)

def warning(text: str, )-> None:
    '''
    输出warning日志

    :param: text 日志内容
    :type: str

    :rtype: None 
    '''
    logger.warning(text)