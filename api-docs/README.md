# CDP API docs

All-in-one action for Docusaurus tenants using the shared API docs builder.

It:

1. resolves the release tag and whether docs changed (`api-docs-version`)
2. builds `latest` and the tagged version (`api-docs-build`)
3. publishes both folders (`publish-api-docs`)

## Example

```yaml
- name: Publish API docs
  uses: DEFRA/cdp-build-action/api-docs@main
  with:
    builder-version: latest
```

`fetch-depth: 0` is required on checkout so tags are available.
