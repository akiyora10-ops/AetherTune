import logging, os

LOG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'aethertune.log')
logging.basicConfig(filename=LOG, level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

def log(msg):
    logging.info(msg)
