# Py-DCHcaptcha

A simplep python wrapper for [dchcaptcha.com](https://dchcaptcha.com/).

## Setup
`pip install py_dchcaptcha`

## How to use
```python
from py_dchcaptcha import DCHcaptcha

key = DCHcaptcha.solve(
    'site_key', # HCaptcha site key of your website.
    'link', # Link of the page where you are solving it.
    'proxy', # HTTP Proxy, format: user:pass@ip:port or ip:port
    'rqdata' # Optional, used for silent captcha, ex: discord join.
)
print(key)
```