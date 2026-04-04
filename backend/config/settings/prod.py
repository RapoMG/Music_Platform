from .base import *

# Load .env file

env_file = BASE_DIR / ".env.prod"
if env_file.exists():
    environ.Env.read_env(env_file)

DEBUG = False

ALLOWED_HOSTS = []