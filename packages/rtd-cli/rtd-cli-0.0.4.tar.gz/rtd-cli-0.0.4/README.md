# `rtd`: simple [Readthedocs] CLI

## Install
```bash
pip install rtd-cli
# Set this env var, or write the token to ~/.config/rtd-cli/token
 RTD_TOKEN=your_token
```

## Usage
```bash
rtd --help
# Usage: rtd [OPTIONS] COMMAND [ARGS]...
#
#   Simple CLI wrapper for the Readthedocs REST API.
#
# Options:
#   --help  Show this message and exit.
#
# Commands:
#   api         Make a request to the Readthedocs REST API.
#   deactivate  Deactivate one or more versions
#   hide        Hide one or more versions

rtd api --help
# Usage: rtd api [OPTIONS] ENDPOINT
#
#   Make a request to the Readthedocs REST API.
#
#   RTD API docs: https://docs.readthedocs.io/en/stable/api/v3.html
#
# Options:
#   -b, --body TEXT     JSON string to send in the body of a PATCH request; if
#                       absent, a GET request is sent
#   -u, --show-updated  After a PATCH request (with -b/--body), send a GET to
#                       the same endpoint, to verify the updated state of the
#                       resource
#   --help              Show this message and exit.
```

## Examples

List projects:
```bash
rtd api projects
# {
#   "count": …,
#   "next": null,
#   "previous": null,
#   "results": [
#     …
#   ]
# }
```

Hide all versions except for a specific list:

```bash
project=your_project
keep=(latest 1.11.)  # grep patterns to keep
limit=100

# Exclude `keep` patterns above, when calling `rtd hide` below
grep_args=(-v)
for v in "${keep[@]}"; do
  grep_args+=(-e "$v")
done

rtd api "projects/$project/versions?limit=$limit&active=true&built=true" \
| jq -r '.results[] | select(.hidden | not) | .slug' \
| grep "${grep_args[@]}" \
| xargs rtd hide -p $p
```

[Readthedocs]: https://readthedocs.org
