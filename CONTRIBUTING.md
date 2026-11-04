# Contribution guidelines

Contributing to this project should be as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features

## Github is used for everything

Github is used to host code, to track issues and feature requests, as well as accept pull requests.

Pull requests are the best way to propose changes to the codebase.

1. Fork the repo and create your branch from `main`.
2. If you've changed something, update the documentation.
3. Make sure your code lints (using `scripts/lint`).
4. Test you contribution.
5. Issue that pull request!

## Any contributions you make will be under the MIT Software License

In short, when you submit code changes, your submissions are understood to be under the same [MIT License](http://choosealicense.com/licenses/mit/) that covers the project. Feel free to contact the maintainers if that's a concern.

## Report bugs using Github's [issues](../../issues)

GitHub issues are used to track public bugs.
Report a bug by [opening a new issue](../../issues/new/choose); it's that easy!

## Write bug reports with detail, background, and sample code

**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can.
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

People *love* thorough bug reports. I'm not even kidding.

## Use a Consistent Coding Style

Use [black](https://github.com/ambv/black) to make sure the code follows the style.

## Test your code modification

This custom component is based on [integration_blueprint template](https://github.com/ludeeus/integration_blueprint).

It comes with development environment in a container, easy to launch
if you use Visual Studio Code. With this container you will have a stand alone
Home Assistant instance running and already configured with the included
[`configuration.yaml`](./config/configuration.yaml)
file.

## Releasing

1. Run the **Prepare release** workflow from the Actions tab, picking the version part to
   bump and whether it is a beta. It bumps `manifest.json` on a `release/<version>` branch
   and opens a draft PR with the changelog GitHub generates from the merged PRs.
2. The **Release notes** agent ([`release-notes.md`](.github/workflows/release-notes.md),
   a [gh-aw](https://github.com/github/gh-aw) workflow) rewrites the PR description into
   notes for users within a few minutes, then marks the PR ready for review. Review and
   edit the notes in the PR. If the agent fails, rewrite them yourself and mark the PR
   ready by hand. After changing
   `release-notes.md`, run `gh aw compile` and commit the regenerated `.lock.yml`.
3. Merge the PR. The **Publish release** workflow tags `v<version>` and creates the GitHub
   release with the PR description as its notes; betas become pre-releases.

## License

By contributing, you agree that your contributions will be licensed under its MIT License.
