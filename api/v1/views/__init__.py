from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

from .index import *
from .user import *
from .rescue import *
from .adopt import *