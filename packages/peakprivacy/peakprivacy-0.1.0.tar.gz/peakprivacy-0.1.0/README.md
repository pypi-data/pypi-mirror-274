# PeakPrivacy Python Client

The PeakPrivacy Python Client provides convenient access to the PeakPrivacy REST API from any Python 3.7+
application. The client includes type definitions for all request params and response fields.

## Documentation

The REST API documentation can be found [on peakprivacy.ch](https://peakprivacy.ch/en/guide/api).
The full API of this client can be found in [api.md](api.md).

## Installation

```sh
pip install peakprivacy
```

## Usage

The full API of this client can be found in [api.md](api.md).

```python
import os
from dotenv import load_dotenv

load_dotenv()
from peakprivacy import PeakPrivacy

client = PeakPrivacy(
    # This is the default and can be omitted
    api_token=os.environ.get("PEAKPRIVACY_API_TOKEN")
)

chat_completion = client.chat.completions.create(
    model='mistral-swiss',
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ]
)
```

While you can provide an `api_token` keyword argument,
we recommend using [python-dotenv](https://pypi.org/project/python-dotenv/)
to add `PEAKPRIVACY_API_TOKEN="My API Token"` to your `.env` file
so that your API Token is not stored in source control.

## Streaming Responses

We provide support for streaming responses using Server Side Events (SSE).

Simply add ```stream=True``` parameter into the ```client.chat.completions.create``` method.

Pay attention to the fact that handling streaming responses is different from handling regular responses.

Check out the example below.

```python
load_dotenv()
from peakprivacy import PeakPrivacy

client = PeakPrivacy(
    # This is the default and can be omitted
    api_token=os.environ.get("PEAKPRIVACY_API_TOKEN")
)

stream = client.chat.completions.create(
    model='mistral-swiss',
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ],
    stream=True
)

for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="")
```

## Supported models

As long as you can utilize a model from the code example above, ```model='mistral-swiss'```, there is a range of options available for use.

You can find the full list of supported models [on peakprivacy.ch](https://peakprivacy.ch/en/guide/api) or by using the ```client.models.list()``` method. 

For a complete description of the method, refer to [api.md](api.md).

```python
load_dotenv()
from peakprivacy import PeakPrivacy

client = PeakPrivacy(
    # This is the default and can be omitted
    api_token=os.environ.get("PEAKPRIVACY_API_TOKEN")
)

models = client.models.list()
print(models)
```


## Handling errors

When the client is unable to connect to the API (for example, due to network connection problems or a timeout), a
subclass of `peakprivacy.ApiConnectionError` is raised.

When the API returns a non-success status code (that is, 4xx or 5xx response), a subclass
of `peakprivacy.ApiStatusError` is raised, containing `status_code` and `response` properties.

All errors inherit from `peakprivacy.ApiError`.

```python
import os
from dotenv import load_dotenv

load_dotenv()
from peakprivacy import PeakPrivacy, ApiTokenNotFoundError, AuthenticationError, PermissionDeniedError, ApiError,
    ApiConnectionError, ApiStatusError

try:
    client = PeakPrivacy(
        # This is the default and can be omitted
        api_token=os.environ.get("PEAKPRIVACY_API_TOKEN")
    )
except ApiTokenNotFoundError as err:
    # exception if token not found
    print(err)
except Exception as err:
    # exception if something went incredibly wrong
    print(err)

try:
    chat_completion = client.chat.completions.create(
        model='mistral-swiss',
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello!"}
        ]
    )
except AuthenticationError as e:
    # 401 catch example ("You Shall Not Pass")
    print(f"AuthenticationError: {e.status_code}, {e.message}, {e.response}")
except PermissionDeniedError as e:
    # 403 catch example (Nope, Not Today, Not Ever)
    print(f"PermissionDeniedError: {e.status_code}, {e.message}, {e.response}")
except ApiStatusError as e:
    # 400, 401, 403, 404, 422, 429, >=500 catch example ("Gremlins in the API: Someone fed them after midnight!")
    print(f"ApiStatusError: {e.status_code}, {e.message}, {e.response}")
except ApiConnectionError as e:
    # request errors
    print(f"ApiConnectionError: {e.status_code}")
except ApiError as e:
    # parent for all errors
    print(f"ApiError: {e.status_code}")
except Exception as err:
    # exception if something went incredibly wrong ("Houston, We’ve Had a Problem")
    print(err)
```

Error codes are as followed:

| Status Code | Error Type                 |
|-------------|----------------------------|
| 400         | `BadRequestError`          |
| 401         | `AuthenticationError`      |
| 403         | `PermissionDeniedError`    |
| 404         | `NotFoundError`            |
| 422         | `UnprocessableEntityError` |
| 429         | `RateLimitError`           |
| >=500       | `InternalServerError`      |
| N/A         | `ApiConnectionError`       |

## Requirements

Python 3.7 or higher.

# Package structure

### Client API

```python
client = PeakPrivacy(
    # This is the default and can be omitted
    api_token=os.environ.get("PEAKPRIVACY_API_TOKEN")
)
```

### Chat api_token validation API

```python
client.chat.check_api_token()
```

### Chat supported models list API

```python
client.models.list()
```

### Chat Completions API

```python
client.chat.completions.create(
    model='mistral-swiss',
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ]
)
```