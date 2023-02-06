# Hypernode API Python Client

_**Please note: this project is still in its early stages and the API may be subject to change.**_

## Installation

```bash
git clone https://github.com/byteinternet/hypernode-api-python.git
cd hypernode-api-python
python3 -m venv venv
. venv/bin/activate
pip install -r requirements/development.txt
```

## Usage

### Acquiring an API token

Each Hypernode has an API token associated with it, you can use that to talk to the API directly. You can find the token in `/etc/hypernode/hypernode_api_token`. For API tokens with special permissions please contact support@hypernode.com. Not all functionality in the API is currently generally available but if you'd like to start automating and have an interesting use-case we'd love to hear from you.


### Installing the library in your project

First make sure your project has the library installed:
```bash
pip install -e git+https://github.com/byteinternet/hypernode-api-python.git@master#egg=hypernode_api_python
```
Of course you might want to put that in a `requirements.txt` file in your project instead of installing it manually.

Alternatively, you can also install the [hypernode-api-python library from PyPI](https://pypi.org/project/hypernode-api-python/):
```
$ python3 -m venv venv
$ . venv/bin/activate
$ pip install hypernode-api-python
$ pip freeze | grep hypernode-api-python
hypernode-api-python==0.0.3
```

###  Performing API calls

Then to use the API client you can test out an example request in your Python repl:
```python
from hypernode_api_python.client import HypernodeAPIPython

client = HypernodeAPIPython(token='yoursecrettoken')

response = client.get_app_flavor('yourhypernodeappname')

response.json()
{'name': '2CPU/8GB/60GB (Falcon S 202202)', 'redis_size': '1024'}
```

Using the Hypernode-API you can automate all kinds of cool things like configuring settings:
```python
client.set_app_setting('yourhypernodeappname', 'php_version', '8.1').json()
{'name': 'yourhypernodeappname', 'type': 'persistent', 'php_version': '8.1', ...}
```

To even performing acts of cloud automation, like scaling to the first next larger plan:
```python
client.xgrade(
    'yourhypernodeappname',
      data={
          'product': client.get_next_best_plan_for_app_or_404(
              'yourhypernodeappname'
          ).json()['code']
      }
)
```


## Development

To run the unit tests you can use `tox`:
```bash
tox -r
```

## Related projects

- The official [Hypernode API PHP Client](https://github.com/byteinternet/hypernode-api-php)
- The official [Hypernode Deploy](https://github.com/byteinternet/hypernode-deploy-configuration) tool
- The official [Hypernode Docker](https://github.com/byteinternet/hypernode-docker) image
