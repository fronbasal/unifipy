# Unifi Python Voucher API
![PyPI](https://img.shields.io/pypi/v/unifipy)
![PyPI - License](https://img.shields.io/pypi/l/unifipy)

This API contains a Unifi API wrapper specifically for creating vouchers programmatically.

## Usage

```python
from unifi import unifi
api = Unifi("foo", "bar", "http://unifi.local")
```

```python
vouchers = api.generate_voucher(expire=42, usages=23)
for voucher in vouchers:
    print(voucher["code"])
```
