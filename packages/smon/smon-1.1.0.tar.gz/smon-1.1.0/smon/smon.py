import sys
import logging

import click
import dotenv

from PySide6.QtWidgets import QApplication

import genlib.ansiec as ansiec
from smon.oscilloscope import Oscilloscope


config = dotenv.find_dotenv(filename=".xnode", usecwd=True)
if config:
    dotenv.load_dotenv(dotenv_path=config)
    
@click.command()
@click.option(
    "--group",
    envvar="MCAST_GROUP",
    default='239.8.7.6',
    type=click.STRING,
    help="UDP Multicast Group (default '239.8.7.6')",
    metavar="GROUP",
)
@click.option(
    "--iport",
    envvar="HOST_PORT",
    default=7321,
    type=click.INT,
    help="UDP Server or Multicast Group Port (default 7321).",
    metavar="IPORT",
)
@click.option(
    "--mcast",
    envvar="MCAST",
    default=False,
    type=click.BOOL,
    help="Enable Multicast (default False)",
    metavar="MCAST",
)
@click.option(
    "--log",
    envvar="LOG",
    default='None',
    type=click.STRING,
    help="Data Logging (default none)",
    metavar="LOG",
)
def main(group, iport, mcast, log):
    logger = logging.getLogger('stream')
    logger.setLevel(logging.INFO)
    logger = logging.getLogger('file')
    logger.setLevel(logging.INFO)
    
    formatter = logging.Formatter(ansiec.ANSIEC.FG.BRIGHT_YELLOW + '[%(asctime)s]' + ansiec.ANSIEC.FG.BRIGHT_CYAN + '%(funcName)s: ' + ansiec.ANSIEC.OP.RESET + '%(message)s')
    formatter_file = logging.Formatter('[%(asctime)s]%(funcName)s: %(message)s')
    log_name = ''

    if log.lower() == 'none':
        logger.setLevel(logging.NOTSET)
    elif log.lower() == 'stream':
        log_name = 'stream'
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        handler.setFormatter(formatter)
        logger = logging.getLogger(log_name)
        logger.addHandler(handler)
    else:
        log_name = 'file'
        handler = logging.FileHandler(log)
        handler.setLevel(logging.INFO)
        handler.setFormatter(formatter_file)
        logger = logging.getLogger(log_name)
        logger.addHandler(handler)

    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    clipboard = app.clipboard()
    Oscilloscope(group, iport, mcast, clipboard, log_name).show()
    app.exec()
    
if __name__ == "__main__":    
    main()