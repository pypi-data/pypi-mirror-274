# Krutrim Wrapper
An unofficial wrapper for Krutrim written in python

## Usage
### Get an API Key
1. Open https://cloud.olakrutrim.com/
2. Register a new account
3. Submit a request for API access
4. Go to the sidebar and select Interface Service > API Keys to generate a new key

### Example
```py
from krutrimpy import Krutrim

k = Krutrim("<API_KEY>") 
res = k.send("Hey There")

print(res.response)
```