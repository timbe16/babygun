from flask import Flask
import logging
import sys

app = Flask(__name__)
app.url_map.strict_slashes = False

logging.basicConfig()
handler = logging.StreamHandler(stream=sys.stdout)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)

app.config.from_object('app.config.config')
from app.api import mail_api
from app.util.db import db
from app.util import cron
