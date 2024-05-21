# Python Library for Conva AI

This is the python library for using Conva AI Co-pilots

## Examples

### 1. A simple example for generating response using Conva Co-pilot
```
import asyncio
from conva_ai import AsyncConvaAI
client = AsyncConvaAI(
    assistant_id="<YOUR_ASSISTANT_ID>", 
    assistant_version="<YOUR_ASSISTANT_VERSION>", 
    api_key="<YOUR_API_KEY>"
)
async def generate_with_capability_group(client: AsyncConvaAI, query: str, capability_group: str = "default", stream: bool = "True"):
  if stream:
    response = await client.invoke_capability_group_stream(query, capability_group=capability_group)
    out = ""
    async for res in response:
        out = res.model_dump_json(indent=4)
    return out
  else:
    response = await client.invoke_capability_group(query, capability_group=capability_group)
    return response.model_dump_json(indent=4)

final_response = asyncio.run(generate_with_capability_group(client, "how are you", stream=True))
print(final_response)
```

The above snippet of code is used for invoking a capability group. 

Similarly, a particular capability can be invoked by
```
import asyncio
from conva_ai import AsyncConvaAI
client = AsyncConvaAI(
    assistant_id="<YOUR_ASSISTANT_ID>", 
    assistant_version="<YOUR_ASSISTANT_VERSION>", 
    api_key="<YOUR_API_KEY>"
)
async def generate_with_capability_name(client: AsyncConvaAI, query: str, capability_name: str, stream: bool):
  if stream:
    response = await client.invoke_capability_stream(query, capability_name=capability_name)
    out = ""
    async for res in response:
        out = res.model_dump_json(indent=4)
    return out
  else:
    response = await client.invoke_capability(query, capability_name=capability_name)
    return response.model_dump_json(indent=4)

final_response = asyncio.run(generate_with_capability_name(client, "buy 10 shares", "order_management", True))
print(final_response)
```

You can try out the co-pilot on [Google Colab](https://colab.research.google.com/drive/1WtbARTRQ9wCvztrAQuEhQUvwImhtPZXd#scrollTo=ZSVBQsOelgfv)

If you want to get the response as dictionary, then replace
```
out = res.model_dump_json(indent=4)
```

with
```
out = res.model_dump()
```

### 2. How to clear history

Conva AI client, by default keeps track of your conversation history and uses it as the context for responding intelligently

You can clear conversation history by executing the below code:

```
from conva_ai.client import AsyncConvaAI
client = AsyncConvaAI(
    assistant_id="<YOUR_ASSISTANT_ID>", 
    assistant_version="<YOUR_ASSISTANT_VERSION>", 
    api_key="<YOUR_API_KEY>"
)
client.clear_history()
```

In case you are buliding an application where you don't want to track conversation history, you can disable history tracking

```
client.use_history(False)
```

You can enable history by

```
client.use_history(True)
```

### 3. Debugging responses

Conva AI uses generative AI to give you the response to your query. In order for you to understand the reasoning behind the response. We also provide you with AI's reasoning

```
final_response_dict = json.loads(final_response)
print(final_response_dict["reason"])
```