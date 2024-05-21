# Shared Python Utilities

Set AUTH_SERVICE_BASE_URL=

To install 

```bash
poetry add git+https://github.com/capitalsagetechnology/pykolofinance.git@main

poetry add pykolofinance
```

## Usage
1. Install the package 

```bash
poetry add pykolofinance
```

2. Add `pykolofinance` to installed apps in django
3. update `REST_FRAMEWORK` settings as showing below

```bash
REST_FRAMEWORK = {
    ...
    # 'DATE_INPUT_FORMATS': ["%d/%m/%Y", ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        "pykolofinance.authentication.CustomJWTAuthentication",
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    ...
}
```