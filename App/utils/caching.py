from app import app
from flask_caching import Cache
import math

cache = Cache(app.server, config={
    # 'CACHE_TYPE': 'simple',
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': '/tmp/cache-directory',
    'CACHE_THRESHOLD': math.inf
})

TIMEOUT = 1800
