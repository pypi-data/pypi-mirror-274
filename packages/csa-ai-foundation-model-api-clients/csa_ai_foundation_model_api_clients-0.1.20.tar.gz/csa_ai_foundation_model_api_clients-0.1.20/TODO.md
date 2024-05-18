# TODO

## Code

* add --api-key support, NAME_OF_KEY_TO_LOOK_FOR, no fall back
* fix arguments to handle strings OR files for command line options
* fix output and move to separate function
* JSON schema for output format, standardize on a single format with options for each backend
* handle error conditions (mostly rate limiting errors)
* can we fix the relative import path so this tool works as a command line tool? Do we simply need to make a seperate .py?
* max_retries (disable retries by default?)
* timeout (120 seocnds?)

Future:

* add batch processing support (https://platform.openai.com/docs/api-reference/batch/object)
* for sub 1000 max_tokens put the "max_tokens: X" into the system prompt at the top
* figure out if we can generate JSON/markdown/etc responses in a more generic way (e.g. system prompt with exmaple output?)
* add option to wrap user data in JSON if it's not already JSON?
* add "use_latest" style option to the prompt/data inputs so it searches for the most recent prompt for example, this will also need a directory passed in when used as a library
* Break out API key code so it can be an env variable, a config file, IAM options
* How to handle multiple round conversations, JSON input?
* Additional tools/inputs (e.g. images)
* Context caching for longer prompts https://ai.google.dev/gemini-api/docs/caching

## Tests

* add pickling/unpickling capability to code for testing, both software, and tools using it
* add tests for dev
* add tests for CI/CD
* Investigate evals integration: https://github.com/openai/evals

## Infra

* move to poetry

Future:

* figure out GitHub trusted publishing to PyPi