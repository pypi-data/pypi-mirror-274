# Xbox Python API
Xbox Python API wrapper based on https://xbl.io.

## Installation
```bash
pip install xbox-python-api
```

## Usage
Create an instance of the `XPA` class with your API key.
```python
from xpa import XPA

xpa = XPA(api_key="YOUR_API_KEY")
```

## Code example
```python
from xpa import XPA

xpa = XPA(api_key="YOUR_API_KEY")

# Get account gamertag
account_info = xpa.get_account_info_xuid(xuid="xuid")
print(account_info.Gamertag)


# Get user presence
presence = xpa.get_presence(xuid="xuid")
print(presence.state)
```

Full documentation can be found [here](https://github.com/Rarmash/Xbox-Python-API/tree/master/docs).
