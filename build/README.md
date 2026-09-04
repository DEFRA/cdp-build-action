# CDP Build Action

Services that are intended to be deployed to the CDP platform should be built using the CDP Build action as part of their workflow.

The action is designed to be language agnostic and deals purely with Dockerfiles. It is assumed your project will have a single `Dockerfile` in the root of the project.


## What does it do?

- Increments the version number of the release (minor version by default, see below for more details of [major/patch](#major-and-patch-releases)
- Builds the project's `Dockerfile`
- Appends various labels and metadata to the docker image so it can be surfaced in the CDP Portal
- Handles cross building the image so it can be used locally on X86 and AMD64 (apple M) systems
- Handles publishing the image to the platform's Docker Registries

### Example usage

```yaml
jobs:
  build:
    name: CDP-build-workflow
    runs-on: ubuntu-latest
    steps:
      - name: Check out code
        uses: actions/checkout@v5
      
      - name: Build and Publish
        uses: DEFRA/cdp-build-action/build@main
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

If any steps are required before building the image, they can be inserted as steps between checking the code out and calling the build action.

## Inputs

`version`

If you wish to use your own versioning systems for whatever reason (maybe a custom one that bumps the package.json version etc), you can override the version number via the version input.

`github-token`

This should always be set to `${{ secrets.GITHUB_TOKEN }}`.
It’s used to tag the repository when the version is incremented

`image-name`

Overrides the name of the docker image.
By default it will use the name of the github repository, but in some use cases (repositories being renamed, multi-project repos, etc.) it may be required to override this value.

`push`

Sets whether the image will be published to the docker registries.
Defaults to `true`, setting this value to `false` allows the build action to be used as a dry-run or build test.

`push-dockerhub`

When set to `false` prevents the repo pushing a copy of the build to the public DEFRA digital dockerhub.
Defaults to `true` when not set.


`build-secrets`

Newline separated `ID=VALUE` pairs exposed to the docker build as BuildKit secrets, including any build stages this action pushes.

```yaml
        with:
          build-secrets: |
            nuget_pat=${{ secrets.GITHUB_TOKEN }}
```

Read them in the Dockerfile with a secret mount:

```dockerfile
RUN --mount=type=secret,id=nuget_pat \
    export DEFRA_NUGET_PAT="$(cat /run/secrets/nuget_pat)" && \
    dotnet restore
```

Unlike a build argument, the value is available only for that `RUN` instruction and is not written to the image history, the image config, or the layer, so it does not travel with the pushed image.

Note that a secret is only consumed where the Dockerfile mounts it. A repository moving off writing credentials into a config file before the build has to add the mount at the same time, or the build will fail to authenticate.

## Major and Patch releases

By default, each build will bump the minor version (e.g. `0.1.0` → `0.2.0`). To do a major or patch release, simply include `#major` or `#patch` in the commit message.

```shell
git commit -m "bump to #major"
```

Would result in `0.55.0` → `1.0.0`, while

```shell
git commit -m "possible bug fix #patch"
```

Would result in `0.55.0` → `0.55.1`.
