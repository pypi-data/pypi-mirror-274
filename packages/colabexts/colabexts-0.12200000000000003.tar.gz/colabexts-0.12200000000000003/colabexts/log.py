import logging


LOG_FMT="%(name)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.DEBUG, format=LOG_FMT)
#-----------------------------------------------------------------------------------
def ldeb(*kwargs):    logging.debug   ( kwargs )
def linf(*kwargs):    logging.info    ( kwargs )
def lwar(*kwargs):    logging.warning ( kwargs )
def lerr(*kwargs):    logging.error   ( kwargs )
def lcri(*kwargs):    logging.critical( kwargs )

