# Bingx-API

This is yet another library to access Bingx's API. It provides a simple and efficient way to interact with Bingx's API using Python.

## Installation

You can install Bingx-API using pip:

```bash
pip install bingx-api
```

## Usage

To use the Bingx-API, you can import the `bingx_api` module and create an instance of the `BingxClient` class.

```python
from bingx_api import BingxClient

# Create a client instance
client = BingxClient()

# Make a request to the Bingx API
response = client.get_data('symbol', 'BTCUSDT')

# Print the response
print(response)
```

## Contributing

We welcome contributions to Bingx-API. If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

Bingx-API is licensed under the BSD-3-Clause license. See the [LICENSE](LICENSE) file for more information.