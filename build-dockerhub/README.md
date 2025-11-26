# CDP Build Action (DockerHub)

Handles publishing a docker build to docker hub.

## What does it do?

- Builds the project's `Dockerfile` (overridable)
- Handles publishing the image to the platform's DockerHub

### When to use it

This action is intended for publishing non-service artifacts to dockerhub, such as test fixtures, stubs etc.
Images pushed to DockerHub are only available locally or inside of GitHub workflows, you will not be able to deploy anything built with this action to the platform.

### Example usage

```yaml
jobs:
  build:
    name: CDP-build-workflow
    runs-on: ubuntu-latest
    steps:
      - name: Check out code
        uses: actions/checkout@v4
      
      - name: Build and Publish
        uses: defra/cdp-build-action/build@main
        with:
          version: 'latest'
          image-name: 'my-service-stub'
```

If any steps are required before building the image, they can be inserted as steps between checking the code out and calling the build action.

## Inputs

`version`

If you wish to use your own versioning systems for whatever reason (maybe a custom one that bumps the package.json version etc), you can override the version number via the version input.

`image-name`

Overrides the name of the docker image.
By default it will use the name of the github repository, but in some use cases (repositories being renamed, multi-project repos, etc.) it may be required to override this value.

`dockerfile`

Overrides the Dockerfile used to build the image. (Default `./Dockerfile`)

`context`

Overriddes the docker context path. (Default `.`)

`push`

Sets whether the image will be published to the docker registries.
Defaults to `true`, setting this value to `false` allows the build action to be used as a dry-run or build test.

