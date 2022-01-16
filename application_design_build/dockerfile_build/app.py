from tarfile import SUPPORTED_TYPES
from flask import flask
from flask import render_templete
import socket
import random
import os
import argparse

app = Flask(__name__)

color_codes = {
    "red":  "#e74c3c"
    "green": "#16a085"
    "blue": "#2980b9"
    "blue2": "#30336b"
    "pink": "#be2edd"
    "darkblue": "#130f40"
}

SUPPORTED_COLORS = ",".join(color_codes.keys())

