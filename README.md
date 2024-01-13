# Bitcoin-Analyst

Analysis last news about bitcoin and gives advice should buy or not

# Installation

AutoGen Locally Using Virtual Environment
When installing AutoGen locally, we recommend using a virtual environment for the installation.
This will ensure that the dependencies for AutoGen are isolated from the rest of your system.

### Setup venv

You can create a virtual environment with venv as below:

```shell
python3 -m venv pyautogen
```

```shell
source pyautogen/bin/activate
```

The following command will deactivate the current venv environment:

```
deactivate
```

### Change env variables

```python
OPENAI_API_KEY = "TOKEN"
CRYPTO_PANIC_API_KEY = "TOKEN"
GNEWS_PANIC_API_KEY = "TOKEN"
```

# Usage

```shell
python3 main.py
```
