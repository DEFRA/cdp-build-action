# Centralized Checkout Action

A centralized wrapper around [actions/checkout](https://github.com/actions/checkout) that manages versions and defaults in one place across all CDP pipelines.

## Purpose

This action provides a single point of control for checkout operations across all CDP workflows. Instead of directly using `actions/checkout` in multiple pipelines, use this wrapper to:

- **Centralize version management**: Update the `actions/checkout` version once here instead of across dozens of workflows
- **Enforce consistent defaults**: Apply standard configurations (like defaulting to `main` branch) across all pipelines
- **Simplify updates**: When GitHub updates `actions/checkout`, update it once here and all pipelines benefit

## Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `fetch-depth` | Number of commits to fetch. `0` indicates all history for full clone | No | `1` |
| `path` | Relative path under `$GITHUB_WORKSPACE` to place the repository | No | `''` (root) |
| `ref` | The branch, tag or SHA to checkout | No | `main` |

## Usage

### Basic Usage

Checkout the repository with default settings (single commit from `main` branch):

```yaml
- name: Checkout code
  uses: ./cdp-build-action/checkout
```

### Checkout a Specific Branch

```yaml
- name: Checkout feature branch
  uses: ./cdp-build-action/checkout
  with:
    ref: feature/my-feature
```

### Full History Clone

Fetch complete git history (useful for changelog generation or git-based versioning):

```yaml
- name: Checkout with full history
  uses: ./cdp-build-action/checkout
  with:
    fetch-depth: 0
```

### Checkout to Custom Path

Place the repository in a subdirectory:

```yaml
- name: Checkout to custom location
  uses: ./cdp-build-action/checkout
  with:
    path: my-repo
```

### Combined Options

```yaml
- name: Checkout specific tag with history
  uses: ./cdp-build-action/checkout
  with:
    ref: v1.2.3
    fetch-depth: 0
    path: releases/v1.2.3
```

## Maintenance

To update the underlying `actions/checkout` version:

1. Edit `action.yml`
2. Update the version in the `uses:` statement (currently `v5`)
3. Commit and push changes
4. All pipelines using this wrapper will automatically use the new version

## Related Documentation

- [actions/checkout Documentation](https://github.com/actions/checkout)
- [GitHub Actions Composite Actions Guide](https://docs.github.com/en/actions/creating-actions/creating-a-composite-action)
