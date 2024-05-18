# Superblocks Python SDK

[![Python version](https://img.shields.io/badge/python-%3E=_3.10-teal.svg)](https://www.python.org/downloads/)

## Quickstart

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install.

```sh
pip install superblocks-agent
```

## Quickstart

### Run an API

```python3
import asyncio

from superblocks_agent.things.Client import Client
from superblocks_agent.model.ClientConfig import ClientConfig
from superblocks_agent.model.Agent import Agent
from superblocks_agent.model.Auth import Auth


client = Client(ClientConfig(agent=Agent(endpoint="agent_url"), auth=Auth(token="auth_token")))
api = Api("some_api_id")
execution_result = asyncio.run(api.run(client=client))
```

### Run an API with inputs

```python3
import asyncio

from superblocks_agent.things.Client import Client
from superblocks_agent.model.ClientConfig import ClientConfig
from superblocks_agent.model.Agent import Agent
from superblocks_agent.model.Auth import Auth


client = Client(ClientConfig(agent=Agent(endpoint="agent_url"), auth=Auth(token="auth_token")))
api = Api("some_api_id")
execution_result = asyncio.run(api.run(client=client, inputs={"Input1": "foo"}))
```

### Run an API and Mock a Step

```python3
import asyncio

from superblocks_agent.things.Client import Client
from superblocks_agent.model.ClientConfig import ClientConfig
from superblocks_agent.model.Agent import Agent
from superblocks_agent.model.Auth import Auth
from superblocks_agent.model.MockApiFilters import MockApiFilters


client = Client(ClientConfig(agent=Agent(endpoint="agent_url"), auth=Auth(token="auth_token")))
api = Api("some_api_id")
mock = on(MockApiFilters(integration_type="postgres")).return_({"foo": "bar"})
execution_result = asyncio.run(api.run(client=client, mocks=[mock]))
```

## Development

Install Dependencies

```sh
make deps
```

Build Package

```sh
make pkg-build
```
