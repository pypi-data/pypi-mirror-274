# SentrifyAI Python Package

SentrifyAI is a Python package that provides a client for interacting with the SentrifyAI API.

## Installation

You can install the package via pip:

```
pip install sentrifyai
```

## Usage

```
from sentrifyai import api

# Initialize the client
client = api.SentrifyAI()

# List models available on SentrifyAI
models = client.list_models()
print(models)

# Classify a message using a specific model
result = client.classify_message(model_slug='Sentrify-Mod-1.1', message='Your message here')
print(result)
```

## Documentation

For more detailed usage instructions and API reference, please refer to the [documentation](https://github.com/sentrifybot/sentrifyai-python).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.