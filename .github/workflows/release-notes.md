---
# Release notes writer: rewrites the changelog GitHub generates on a release PR into
# notes Home Assistant users can read. Started by the Prepare release workflow.
#
# Engine: uses the repo default (GitHub Copilot). To use Claude or Codex instead,
# add e.g. `engine: claude` and provide the matching secret (ANTHROPIC_API_KEY).
on:
  workflow_dispatch:
    inputs:
      pr:
        description: "Number of the release PR to write notes for"
        required: true
        type: string

permissions:
  contents: read
  pull-requests: read
  copilot-requests: write # authenticates the default Copilot engine (no secret needed)

tools:
  github:
    toolsets: [repos, pull_requests]

safe-outputs:
  update-pull-request:
    target: ${{ github.event.inputs.pr }}
    title: false
    operation: replace
    # The PR description becomes the published release notes.
    footer: false
    max: 1
  mark-pull-request-as-ready-for-review:
    target: ${{ github.event.inputs.pr }}
    max: 1

concurrency:
  job-discriminator: ${{ github.event.inputs.pr }}

timeout-minutes: 15
---

# Release notes

This repository is **Ollama Cloud**, a Home Assistant custom integration that lets Assist
and AI tasks use models hosted on Ollama Cloud. Pull request
#${{ github.event.inputs.pr }} releases a new version. Its description currently holds the
changelog GitHub generated: one line per merged PR, a "New Contributors" section and a
"Full Changelog" link. When the PR is merged, its description is published unchanged as the
GitHub release notes, which HACS shows to users before they update.

Your job is to replace that description with release notes a Home Assistant user can read
in a minute and act on.

## Gather the facts

1. Read PR #${{ github.event.inputs.pr }}: its title gives the version, its description the
   generated changelog.
2. For every PR the changelog lists, read its title, description and changed files, so you
   describe what changed for users rather than repeat the title. Do not skip a PR because
   its title looks minor.
3. Read the latest published release of this repository and match its structure and tone.
   It is the style reference.

## Write the notes

- Start with `## What's changed`, then these sections, leaving out any that would be empty:
  - `### Breaking changes`: anything users must act on, such as a higher minimum Home
    Assistant version, removed options or changed defaults. Say what to do.
  - `### Fixes`: bugs users could hit, described by the symptom they saw.
  - `### Changes`: new features and changes in behaviour.
  - `### Development`: tests, CI, tooling and dependency bumps, summed up in one or two
    bullets. Bot dependency bumps need no bullet of their own.
- Each bullet opens with a **bold sentence** that says the outcome, then at most two plain
  sentences of detail, then the PR numbers in brackets, like `(#67)`. Merge bullets that
  describe the same change.
- Write for users, not developers: no file or function names unless a user would type them.
- Credit outside contributors in the bullet (`thanks @name`). Keep a `## New contributors`
  section for people who are not bots, and leave it out if there are none.
- End with the `**Full Changelog**` line from the generated changelog, unchanged.
- If the version contains `-beta`, add one line under the heading saying this is a
  pre-release for testing, which HACS only offers to users who enabled beta versions.
- Only state what the PRs show. If a change's effect on users is unclear, describe it
  plainly rather than guess.
- Do not mention that the notes were written or rewritten by AI.

## Output

1. Update PR #${{ github.event.inputs.pr }} once, replacing its description with the notes.
   Do not change its title, and do not touch any other PR or issue.
2. Then mark the same PR as ready for review, with the reason `Release notes rewritten.`
   It opens as a draft so it cannot be merged, and published, with the raw changelog.
