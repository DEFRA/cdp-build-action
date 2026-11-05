# CDP API docs version

Resolves two values for API docs workflows:

- `version`: the exact git tag on `HEAD`
- `changed`: whether API docs inputs changed since the previous tag

## Example

```yaml
- name: Resolve API docs version and changes
  id: docs
  uses: DEFRA/cdp-build-action/api-docs-version@main
  with:
    paths: |
      docs/
      .github/workflows/publish-api-docs.yml

- name: Show values
  run: |
    echo "Version: ${{ steps.docs.outputs.version }}"
    echo "Changed: ${{ steps.docs.outputs.changed }}"
```

The action expects checkout with tags (`fetch-depth: 0`).
