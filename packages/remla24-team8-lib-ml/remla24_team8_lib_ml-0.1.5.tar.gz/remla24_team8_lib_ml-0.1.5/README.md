# lib-ml

Contains the pre-processing logic for data that is used for training or queries.
Is automatically versioned and uploaded to PyPi. Uses a tokenizer hosted on Google Drive, but can also load from local or create a new tokenizer and save it.

## Usage

Install with

```
pip install remla24-team8-lib-ml

```

Use as

```
from lib_ml import DataProcessor 

data_processor = DataProcessor()

```

## Publish a release

To publish a new release, simply create a new release in GitHub with the appropriate tag name. Be sure that this tag name matches the version in the `pyproject.toml`. GitHub Actions will then automatically release and publish this. If the release failed, then remove the tag while in the Git repo using `git push origin --delete <tag name>`, after which you can then re-release the (now draft) release on GitHub.

When using Poetry, you can also depend on the latest commit using the following dependency:

```
remla24-team8-lib-ml = { git = "https://github.com/remla24-team8/lib-ml.git", branch = "main" }
```

### PyPi organization

For now it is owned by tmtenbrink on PyPI, but hopefully we get an organization so we can put it there.