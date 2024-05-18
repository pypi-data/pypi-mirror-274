# keymateapi


<!-- Start SDK Installation [installation] -->
## SDK Installation

```bash
pip install keymateapi
```
<!-- End SDK Installation [installation] -->

<!-- Start SDK Example Usage [usage] -->
## SDK Example Usage

### Example

```python
import keymateapi

s = keymateapi.Keymateapi(
    bearer_auth="<YOUR_BEARER_TOKEN_HERE>",
)

res = s.upsert(q='I prefer Costa over Starbucks.')

if res.object is not None:
    # handle response
    pass

```
<!-- End SDK Example Usage [usage] -->

<!-- Start Available Resources and Operations [operations] -->
## Available Resources and Operations

### [Keymateapi SDK](docs/sdks/keymateapi/README.md)

* [upsert](docs/sdks/keymateapi/README.md#upsert) - Inserts record to Keymate Memory.
* [query](docs/sdks/keymateapi/README.md#query) - Queries the user's Keymate Memory.
* [browseurl](docs/sdks/keymateapi/README.md#browseurl) - The plugin enables user to conduct web browsing by extracting the text content of a specified URL. It will generate title and content.
* [browse](docs/sdks/keymateapi/README.md#browse) - Fetch any URLs without proxy it would probably fail on major websites but quicker than browseurl 
* [search](docs/sdks/keymateapi/README.md#search) - Without proxies searches keyword on the internet and fetches urls and optimizes output
* [ultrafastsearch](docs/sdks/keymateapi/README.md#ultrafastsearch) - This plugin provides 10 ultra fast search results from multiple sources giving a more comprehensive view.
* [gptsbrowse](docs/sdks/keymateapi/README.md#gptsbrowse) - Fetch memory.keymate.ai URLs
* [internetsearch](docs/sdks/keymateapi/README.md#internetsearch) - Conduct an internet search
<!-- End Available Resources and Operations [operations] -->

<!-- Start Error Handling [errors] -->
## Error Handling

Handling errors in this SDK should largely match your expectations.  All operations return a response object or raise an error.  If Error objects are specified in your OpenAPI Spec, the SDK will raise the appropriate Error type.

| Error Object                 | Status Code                  | Content Type                 |
| ---------------------------- | ---------------------------- | ---------------------------- |
| errors.BrowseurlResponseBody | 400                          | application/json             |
| errors.SDKError              | 4xx-5xx                      | */*                          |

### Example

```python
import keymateapi
from keymateapi.models import errors, operations

s = keymateapi.Keymateapi(
    bearer_auth="<YOUR_BEARER_TOKEN_HERE>",
)

res = None
try:
    res = s.browseurl(request=operations.BrowseurlRequest(
    inputwindowwords='10000',
    q='https://keymate.ai',
    percentile='1',
    numofpages='1',
    paging='1',
))
except errors.BrowseurlResponseBody as e:
    # handle exception
    raise(e)
except errors.SDKError as e:
    # handle exception
    raise(e)

if res.two_hundred_application_json_object is not None:
    # handle response
    pass

```
<!-- End Error Handling [errors] -->

<!-- Start Server Selection [server] -->
## Server Selection

### Select Server by Index

You can override the default server globally by passing a server index to the `server_idx: int` optional parameter when initializing the SDK client instance. The selected server will then be used as the default on the operations that use it. This table lists the indexes associated with the available servers:

| # | Server | Variables |
| - | ------ | --------- |
| 0 | `https://server.searchweb.keymate.ai` | None |

#### Example

```python
import keymateapi

s = keymateapi.Keymateapi(
    server_idx=0,
    bearer_auth="<YOUR_BEARER_TOKEN_HERE>",
)

res = s.upsert(q='I prefer Costa over Starbucks.')

if res.object is not None:
    # handle response
    pass

```


### Override Server URL Per-Client

The default server can also be overridden globally by passing a URL to the `server_url: str` optional parameter when initializing the SDK client instance. For example:
```python
import keymateapi

s = keymateapi.Keymateapi(
    server_url="https://server.searchweb.keymate.ai",
    bearer_auth="<YOUR_BEARER_TOKEN_HERE>",
)

res = s.upsert(q='I prefer Costa over Starbucks.')

if res.object is not None:
    # handle response
    pass

```
<!-- End Server Selection [server] -->

<!-- Start Custom HTTP Client [http-client] -->
## Custom HTTP Client

The Python SDK makes API calls using the [requests](https://pypi.org/project/requests/) HTTP library.  In order to provide a convenient way to configure timeouts, cookies, proxies, custom headers, and other low-level configuration, you can initialize the SDK client with a custom `requests.Session` object.

For example, you could specify a header for every request that this sdk makes as follows:
```python
import keymateapi
import requests

http_client = requests.Session()
http_client.headers.update({'x-custom-header': 'someValue'})
s = keymateapi.Keymateapi(client=http_client)
```
<!-- End Custom HTTP Client [http-client] -->

<!-- Start Authentication [security] -->
## Authentication

### Per-Client Security Schemes

This SDK supports the following security scheme globally:

| Name          | Type          | Scheme        |
| ------------- | ------------- | ------------- |
| `bearer_auth` | http          | HTTP Bearer   |

To authenticate with the API the `bearer_auth` parameter must be set when initializing the SDK client instance. For example:
```python
import keymateapi

s = keymateapi.Keymateapi(
    bearer_auth="<YOUR_BEARER_TOKEN_HERE>",
)

res = s.upsert(q='I prefer Costa over Starbucks.')

if res.object is not None:
    # handle response
    pass

```
<!-- End Authentication [security] -->

<!-- Placeholder for Future Speakeasy SDK Sections -->

# Development

## Maturity

This SDK is in beta, and there may be breaking changes between versions without a major version update. Therefore, we recommend pinning usage
to a specific package version. This way, you can install the same version each time without breaking changes unless you are intentionally
looking for the latest version.

## Contributions

While we value open-source contributions to this SDK, this library is generated programmatically.
Feel free to open a PR or a Github issue as a proof of concept and we'll do our best to include it in a future release!

### SDK Created by [Speakeasy](https://docs.speakeasyapi.dev/docs/using-speakeasy/client-sdks)
