# lam

Lam is a `jq` transpiling tool for Laminar.

## Quickstart

Install the dependencies.

```bash
brew install jq
# or
sudo apt-get install jq
make setup
```

Run the CLI tool.

> Note: ARGS is used to pass arguments to the CLI tool via `make`.

```bash
make cli ARGS="<program> <input>"
```

## Install

Install in Dockerfile with:

```
RUN pip3 install git+https://${GITHUB_USER}:${GITHUB_TOKEN}@github.com/user/project.git@{version}
```

### Examples

```bash
make cli ARGS="run test/simple/program.lam test/simple/data.json"
```

Run the `test/simple` example, it should return:

```json
{
  "value": 6
}
{
  "value": 8
}
{
  "value": 9
}
```

## Setup (manual)

Create a virtual environment and install the dependencies.

```bash
python3 -m venv ./venv
source ./venv/bin/activate
pip install -r requirements.txt
```

Running the CLI tool.

```bash
python3 ./lam/lam.py run <program> <input>
```

## Dependencies

Make sure to update the `requirements.txt` file when adding new dependencies.

```bash
pip3 install <package>
pip3 freeze > requirements.txt
```

## Releases

PyPI CI handles most stuff. Sometimes it'll push the test version to test PyPI which will cause the CI to "fail" but really we just need to make sure that the PyPI version on the proper distro site is correct [https://pypi.org/project/lam-cli/](https://pypi.org/project/lam-cli/).

Before releasing make sure to update the package version in `setup.py`.

```python
setup(
    name="lam-cli",
    version="0.0.<x>",
    ...
)
```

Don't add the `-<increment>` to the version number in `setup.py`. This is added when creating a tag.

You can release with:

```bash
git tag v<version>-<increment>

# Example
git tag v0.0.1-1
```

Then push the tag.

```bash
git push origin v<version>-<increment>

# Example
git push origin v0.0.1-1
```

The CI will handle the rest!