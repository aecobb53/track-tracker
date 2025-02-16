import os
import logging

def init_logger():
    # Logging

    appname = 'track_tracker'
    # try:
    #     os.makedirs('logs')
    # except:
    #     pass
    # log_file = f"logs/{appname}.log"
    logger = logging.getLogger(appname)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(module)s %(funcName)s - %(message)s', '%Y-%m-%dT%H:%M:%SZ')
    logger.setLevel(logging.DEBUG)
    # fh = logging.FileHandler(log_file)
    # fh.setLevel(logging.DEBUG)
    # fh.setFormatter(formatter)
    # logger.addHandler(fh)
    # if os.environ.get('STREAM_HANDLER', 'False') == 'True':
    # if os.environ.get('STREAM_HANDLER', 'True') == 'True':
    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)
    sh.setFormatter(formatter)
    logger.addHandler(sh)
    return logger
