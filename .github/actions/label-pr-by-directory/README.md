# Label PR by Directory

A custom GitHub Action that automatically labels pull requests based on the directories that contain changed files.

## Features

- 🏷️ Automatically adds labels to PRs based on top-level directories with changes
- 🎨 Creates labels with predefined colors for common directories (src, test, docs, etc.)
- 🚀 Runs on every pull request event
- 📊 Provides outputs with added labels and changed directories

## How it works

1. When a pull request is opened or updated, the action retrieves all changed files
2. It extracts the top-level directory from each file path
3. Creates repository labels for each directory (if they don't already exist)
4. Adds the appropriate labels to the pull request

## Example Labels

- `src` - Changes in source code (blue)
- `test` - Changes in test files (purple)
- `docs` - Changes in documentation (green)
- `config` - Changes in configuration files (yellow)
- `.github` - Changes in GitHub workflows/actions (dark blue)
- `root` - Changes in root-level files (light yellow)

## Inputs

### `github-token`

**Required** GitHub token for API access. Default: `${{ github.token }}`

### `label-prefix`

**Optional** Prefix to add to directory labels. Default: `''`

## Outputs

### `labels-added`

Comma-separated list of labels that were added to the PR.

### `directories-changed`

Comma-separated list of directories that had changes.

## Usage

```yaml
- name: Label PR by directory
  uses: ./.github/actions/label-pr-by-directory
  with:
    github-token: ${{ secrets.GITHUB_TOKEN }}
    label-prefix: 'area: '  # Optional: adds "area: " prefix to labels
```

## Integration

This action is automatically integrated into the CI workflow and runs on all pull requests to the main branch.