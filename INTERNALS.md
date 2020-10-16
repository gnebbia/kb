# Internals #

This section details the internal mechanisms of kb (specifically relating to the API).

# Return Codes #

Within many of the functions of kb, core functionality may return a return code, indicating its' status upon completion.
This section explains those return codes and their meaning. Note that this is in addition to any data that may be returned from those functions.

|-------|-------|
| Code | Description |
|-------|-------|
| -200 | The function was carried out successfully |
| -301 | The function found more than one match for the criteria |    ** SHOULD BE USING 300 HERRE **
| -302 | The function was attempted, but could find no artifacts with the search criteria (does not include by ID) | ** SHOULD BE USING 406 HERRE **
| -404 | The function errored |


Most of these return codes are presented to the API in the form of an HTTP response code.


# HTTP Response Codes #

In general, the internal response codes descibed above relate to the API HTTP response codes (described below) however, some codes have additional information added to them in the description. These descriptions differ according to the function (they are documented separately).

|-------|-------|
| Code | Description |
|-------|-------|
| 200 | The function was carried out successfully |
| 301 | The function found more than one match for the criteria |   ** SHOULD BE USING 300 HERRE **
| 302 | The function was attempted, but could find no artifacts with the search criteria (does not include by ID) | ** SHOULD BE USING 406 HERRE **
| 401 | Login credentials required |
| 404 | The function errored |
| 405 | Method not implemented
