# A simple Wordle solver

An action that solves unofficial [wordle](https://www.powerlanguage.co.uk/wordle/) puzzles provided by [my API](https://github.com/k2bd/wordle-api).

## Quickstart

```yml
name: Solve daily puzzles
on:
  schedule:
    - cron: "0 8 * * *"  # At 8am

jobs:
  wordler:
    runs-on: ubuntu-latest
    steps:
      - uses: k2bd/wordler@v1
        with:
          puzzleSize: 6
```

## Action Specification

### `wordleApiUrl`

*Optional* - default `https://v1.wordle.k2bd.dev`

URL of the wordle API

### `puzzleSize`

*Optional* - default 5

Size of the puzzle to solve


## Developing

Install [Poetry](https://python-poetry.org/) and `poetry install` the project

### Useful Commands

Note: if Poetry is managing a virtual environment for you, you may need to use `poetry run poe` instead of `poe`

- `poe autoformat` - Autoformat code
- `poe lint` - Linting
- `poe test` - Run Tests

### Testing the action

The action can be tested locally by building the Dockerfile, e.g.

```sh
docker run -e INPUT_HELLONAME=k2bd -e INPUT_REPEATS=2 $(docker build -q .)
```

Additionally, there is a manual invocation action on the repo called "Test Action" that can be used to invoke the repo's version of the action from the Actions tab of the repo.

### Releasing

Release a new version by creating a new annotated semver tag e.g. `git tag -a v1.2.3 -m "Release version 1.2.3"` and pushing it (`git push --tags`). Then create a new release from that tag in GitHub.

There is an autoversioning action that keeps major version tags (`v1`, `v2`, ...) and `latest` up-to-date when a new release is published.
