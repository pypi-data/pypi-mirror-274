# Llama3 Package

## Overview

The Llama3 package allows you to interact with Meta's Llama 3 model locally using Ollama. The package automatically handles the installation and setup of Ollama and the Llama 3 model, allowing you to start using it with minimal effort.

## Installation

### Step 1: Install the Llama3 Package

You can install the Llama3 package using pip:

```bash
pip install llama3_package
```

## Usage

The Llama3 package automatically installs Ollama, starts the Ollama server, pulls the Llama 3 model, and runs the model. You can interact with the model using the `Llama3Model` class.

### Example

Here's a quick example to get you started:

```python
from llama3 import Llama3Model

# Initialize the model
model = Llama3Model()

# Send a prompt to the model
response = model.prompt("5+5=")
print("Prompt Response:", response)

# Stream a prompt to the model
for chunk in model.stream_prompt("Tell me a joke"):
    print("Stream Prompt Response:", chunk)
```

### How It Works

1. **Automatic Installation of Ollama**: If Ollama is not installed on your system, the package will automatically download and install it.
    - On **Linux**, it uses the command: `curl -fsSL https://ollama.com/install.sh | sh`
    - On **macOS**, it uses the command: `brew install ollama`
2. **Starting Ollama Server**: The package starts the Ollama server in the background and verifies it is running.
3. **Pulling the Llama 3 Model**: The package ensures the Llama 3 model is pulled and ready to use.
4. **Running the Model**: The Ollama service is started in the background and managed by the package.

### Configuration

You can configure the model using environment variables. For example, to use a different version of the Llama 3 model, you can set the `LLAMA3_MODEL_NAME` environment variable:

```bash
export LLAMA3_MODEL_NAME="llama3-70B"
```

### Troubleshooting

If you encounter any issues with the package, please ensure that:
- You have an active internet connection for downloading and pulling the model.
- Your system meets the requirements for running Ollama.

For further assistance, please open an issue on our [GitHub repository](https://github.com/PrinceDisant/llama3_package).

### Example Test Script

You can also use the following test script to verify the functionality:

```python
import sys
import os
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from llama3.model import Llama3Model

class TestLlama3Model(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = Llama3Model()

    @classmethod
    def tearDownClass(cls):
        del cls.model

    def test_prompt(self):
        response = self.model.prompt("5+5=")
        print("Prompt Response:", response)
        self.assertIn("10", response.lower())

if __name__ == "__main__":
    unittest.main()
```

## Contributing

We welcome contributions! Please see the [CONTRIBUTING.md](CONTRIBUTING.md) for more details.

## License

This project is licensed under the MIT License.
