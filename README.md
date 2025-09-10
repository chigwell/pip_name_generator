[![PyPI version](https://badge.fury.io/py/pip_name_generator.svg)](https://badge.fury.io/py/pip_name_generator)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://static.pepy.tech/badge/pip_name_generator)](https://pepy.tech/project/pip_name_generator)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-blue)](https://www.linkedin.com/in/eugene-evstafev-716669181/)

# pip_name_generator

`pip_name_generator` is a Python package designed for generating unique, PyPI-compatible package names based on descriptive text. It uses a combination of deterministic fallback mechanisms and simulated LLM signals to produce candidate names, ensuring that the first available name is returned efficiently without requiring network access.

## Installation

To install `pip_name_generator`, use pip:

```bash
pip install pip_name_generator
```

## Usage

Here's an example of how to utilize `pip_name_generator` to generate an available package name for a product described as "Data analysis toolkit":

```python
from pip_name_generator import generate_available_package_name
from langchain_llm7 import ChatLLM7

# Example description
description = "Data analysis toolkit"

llm = ChatLLM7(model="qwen2.5-coder-32b-instruct", base_url="https://api.llm7.io/v1")

# Generate a package name
name = generate_available_package_name(description, llm=llm)

print(f"Suggested package name: {name}")
```

## Features

- Simulated name availability check to avoid network calls
- Supports mock LLM inputs for more contextual candidates
- Falls back to deterministic name generation if LLM signals are unavailable
- Ensures generated names are valid PyPI names (lowercase, underscores, alphanumeric)

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/chigwell/pip_name_generator/issues).

## License

`pip_name_generator` is licensed under the [MIT License](https://opensource.org/licenses/MIT).

## Author

Eugene Evstafev <hi@eugene.plus>  
Repository: [https://github.com/chigwell/pip_name_generator](https://github.com/chigwell/pip_name_generator)