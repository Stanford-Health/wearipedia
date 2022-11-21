# Welcome to the Wearipedia contributing guide

DISCLAIMER: this contributing guide may be inaccurate; it is just a template for now.

Thank you for investing your time in contributing to our project! Any contribution to this project is greatly appreciated.

This guide is meant to help you get started contributing to the Wearipedia. Feel free to submit new sections, revise existing sections, and make comments on sections that need improvement! We're looking forward to hearing from you as we improve our project.

## Table of contents

* [Community](#community)
* [Development](#development)
* [GitHub](#github)
* [Reporting bugs](#reporting-bugs)
* [Suggesting enhancements](#suggesting-enhancements)
* [Code of conduct](#code-of-conduct)
* [Contributor license agreement](#contributor-license-agreement)

## Community

The Wearipedia community is growing! We're excited to have you on board. Please check out the following resources to get started:

- The [Wearipedia website](https://wearipedia.org/)
- The [Wearipedia blog](https://wearipedia.org/blog/)
- The [Wearipedia forum](https://wearipedia.org/forum/)

## Development

The Wearipedia is built on the [GitHub platform](https://github.com/). The following is a basic overview of GitHub and how you can use it to contribute to this project.

### GitHub

If you're not familiar with GitHub, it's a web-based hosting service for software development projects that use the Git revision control system. GitHub provides a collaborative environment for developers to work on projects together.

If you want to learn more about GitHub, check out the [GitHub Help](https://help.github.com/) page.

tiny change.

### Working with GitHub

In order to start working on the Wearipedia, you'll need to create a GitHub account. Once you have an account, you can [fork](https://help.github.com/articles/fork-a-repo/) the Wearipedia repository. This will create your own copy of the project that you can work on.

Once you've made changes to your fork, you can [submit a pull request](https://help.github.com/articles/using-pull-requests/) to the main Wearipedia repository. This will notify the project maintainers of your changes and give them an opportunity to review and merge your changes into the main project.

## Reporting bugs

If you find a bug in the Wearipedia, we would appreciate it if you would report it. Before reporting a bug, please check the [existing issues](https://github.com/wearipedia/wearipedia/issues) to see if your bug has already been reported.

To report a bug, please [submit a new issue](https://github.com/wearipedia/wearipedia/issues/new) to the Wearipedia repository. Please include as much detail as possible, including:

- A descriptive title
- A description of the problem
- Steps to reproduce the problem
- The expected behavior
- The actual behavior

## Suggesting enhancements

If you have an idea for an enhancement to the Wearipedia, we would love to hear it! Please check the [existing issues](https://github.com/wearipedia/wearipedia/issues) to see if your idea has already been suggested.

To suggest an enhancement, please [submit a new issue](https://github.com/wearipedia/wearipedia/issues/new) to the Wearipedia repository. Please include as much detail as possible, including:

- A descriptive title
- A description of the enhancement
- The expected behavior
- Any additional information that would be helpful

## Code of conduct

The Wearipedia is committed to providing a welcoming and harassment-free experience for everyone. We do not tolerate harassment of participants in any form.

If you are being harassed, notice that someone else is being harassed, or have any other concerns, please contact a member of the Wearipedia team immediately.

The Wearipedia team will be happy to help participants contact law enforcement or otherwise assist those experiencing harassment to feel safe for the duration of the event. We value your attendance.

## Contributor license agreement

In order to contribute to the Wearipedia, you must sign a contributor license agreement (CLA). This agreement gives us permission to use and redistribute your contributions as part of the project.

To sign the CLA, please fill out the form at the following URL:

[https://wearipedia.org/cla/](https://wearipedia.org/cla/)


# How to contribute

## Dependencies

We use `poetry` to manage the [dependencies](https://github.com/python-poetry/poetry).
If you dont have `poetry`, you should install with `make poetry-download`.

To install dependencies and prepare [`pre-commit`](https://pre-commit.com/) hooks you would need to run `install` command:

```bash
make install
make pre-commit-install
```

To activate your `virtualenv` run `poetry shell`.

## Codestyle

After installation you may execute code formatting.

```bash
make codestyle
```

### Checks

Many checks are configured for this project. Command `make check-codestyle` will check black, isort and darglint.
The `make check-safety` command will look at the security of your code.

Comand `make lint` applies all checks.

### Before submitting

Before submitting your code please do the following steps:

1. Add any changes you want
1. Add tests for the new changes
1. Edit documentation if you have changed something significant
1. Run `make codestyle` to format your changes.
1. Run `make lint` to ensure that types, security and docstrings are okay.

## Other help

You can contribute by spreading a word about this library.
It would also be a huge contribution to write
a short article on how you are using this project.
You can also share your best practices with us.
