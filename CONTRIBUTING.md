# Contributing

Thanks for helping out! Bug reports, fixes and feature ideas are all welcome.

- **Bugs and ideas:** [open an issue](../../issues/new/choose) with one of the templates. For
  bugs, include your Home Assistant version, the model you used, and the logs.
- **Code:** fork the repository, branch from `main`, and open a pull request.

## Project layout

```text
custom_components/ollama_cloud/
  __init__.py        # set-up, API client and key validation
  config_flow.py     # API key flow and per-agent options (model, prompt, tools, thinking)
  entity.py          # shared chat logic: streaming, tool calls, message history
  conversation.py    # conversation agent entity
  ai_task.py         # AI Task entity (generate data, structured output)
  models.py          # message roles and chat history types
  const.py           # constants and defaults
  strings.json       # UI text (keep translations/ in sync)
  manifest.json      # version and Python requirements
tests/               # pytest suite using pytest-homeassistant-custom-component
hacs.json            # minimum Home Assistant version for HACS and the Marketplace
```

## Set up

You need Python 3.13 or newer, and Docker if you want to run Home Assistant locally. `make help`
lists every task.

```bash
python3 -m venv .venv && source .venv/bin/activate
make setup   # install the test and dev dependencies
```

## Run it in Home Assistant

```bash
make dev      # start Home Assistant at http://localhost:8123 and follow the logs
make restart  # pick up your code changes
make down     # stop and remove the container
```

The integration folder is mounted read-only into the container. Home Assistant writes its runtime
files to `config/`, which git ignores except for `configuration.yaml`.

## Check your change

```bash
make format  # auto-format and auto-fix with ruff
make lint    # what CI runs: ruff check and format check
make test    # pytest with coverage
```

CI runs the tests against three Home Assistant versions: the minimum in `hacs.json`, the version
pinned in `requirements.test.txt`, and the latest one. If you use a Home Assistant API that is
newer than the minimum, keep a fallback for older versions. CI also runs `hassfest` and the HACS
validation.

When you bump `homeassistant` in `requirements.txt`, bump `pytest-homeassistant-custom-component`
in `requirements.test.txt` to the release that matches it.

## Pull requests

- Keep each PR focused on one thing, and add or update tests for any change in behaviour.
- Update `README.md` when users would notice the change.
- Leave the version in `manifest.json` as it is. The release workflow bumps it.
- PR titles and descriptions feed the release notes, so describe the change for users.

## Releasing (maintainers)

1. Run the **Prepare release** workflow from the Actions tab, picking the version part to bump and
   whether it is a beta. It bumps `manifest.json` on a `release/<version>` branch and opens a draft
   PR with the changelog GitHub generates from the merged PRs.
2. Within a few minutes, the **Release notes** agent
   ([`release-notes.md`](.github/workflows/release-notes.md), a
   [gh-aw](https://github.com/github/gh-aw) workflow) rewrites the PR description as notes for
   users and marks the PR ready for review. Review and edit the notes in the PR. If the agent
   fails, write the notes yourself and mark the PR ready by hand. After changing
   `release-notes.md`, run `gh aw compile` and commit the regenerated `.lock.yml`.
3. Merge the PR. The **Publish release** workflow tags `v<version>` and creates the GitHub release
   with the PR description as its notes. Betas become pre-releases.

## License

By contributing, you agree that your contributions are licensed under the project's
[MIT License](LICENSE).
