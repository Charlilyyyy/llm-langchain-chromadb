INSTALLED_APPS = [
    # …
    "corsheaders",
    # …
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    # Django’s default middlewares…
]

# Allow all domains (dev). In prod, set CORS_ALLOWED_ORIGINS = [...]
CORS_ALLOW_ALL_ORIGINS = True
