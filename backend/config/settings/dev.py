from .base import *

environ.Env.read_env(BASE_DIR / ".env.dev")

DEBUG = env.bool("DEBUG", default=True)

ALLOWED_HOSTS = []