from flask import Flask

app = Flask(__name__)

from albumapp import routes
