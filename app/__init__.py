from flask import Flask
import logging
import sys

app = Flask(__name__)
app.url_map.strict_slashes = False
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.config.from_object('app.config.config')

from app.api import *
from app.util.db import db
from app.util import cron
