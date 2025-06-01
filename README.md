# wearipedia

<div align="center">

[![Build status](https://github.com/Stanford-Health/wearipedia/workflows/build/badge.svg?branch=master&event=push)](https://github.com/Stanford-Health/wearipedia/actions?query=workflow%3Abuild)
[![Python Version](https://img.shields.io/pypi/pyversions/wearipedia.svg)](https://pypi.org/project/wearipedia/)
[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/Stanford-Health/wearipedia/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/Stanford-Health/wearipedia/blob/master/.pre-commit-config.yaml)
[![Semantic Versions](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--versions-e10079.svg)](https://github.com/Stanford-Health/wearipedia/releases)
[![License](https://img.shields.io/github/license/Stanford-Health/wearipedia)](https://github.com/Stanford-Health/wearipedia/blob/master/LICENSE)
![Coverage Report](assets/images/coverage.svg)

</div>

<h3 align="center">
    <p>A one-stop shop for wearable device data extraction and simulation</p>
</h3>

Wearipedia provides a one-stop shop for accessing and extracting data from wearable devices.

Data from these devices may be used for:

* Clinical research
* Personal health monitoring
* Health coaching
* Health product development
* Wearable device development

Wearipedia is developed and maintained by the [Snyder Lab](https://med.stanford.edu/snyderlab.html) at the Stanford University.

## Accessing data from wearable devices

The data from these devices is accessed using an easy-to-use API. In order to use this API, you will need to import the `wearipedia` module:

```python
import wearipedia
```

Once you have imported the `wearipedia` module, accessing data from any wearable device is as easy as:

```python
device = wearipedia.get_device("whoop/whoop_4")
device.authenticate({"email": "joesmith@gmail.com", "password": "foobar"})

# data is a DataFrame
data = device.get_data("metrics")
```

If you don't have access to your device, or need to demo data from a device without revealing your sensitive data or getting a device yourself, you can generate synthetic data, as shown below:

```python
device = wearipedia.get_device("whoop/whoop_4")

# data is an automatically generated DataFrame
data = device.get_data("metrics")
```

and you're done!

## Installing

The easiest way to install wearipedia is to use pip:

`pip install wearipedia`

We currently support Python 3.10, 3.11, and 3.12.

## Supported Devices

The full list of devices and associated notebooks can be found in [this page](https://wearipedia.readthedocs.io/en/latest/notebooks/index.html) of the documentation.

## Documentation

For more information on how to use wearipedia, please refer to our [documentation](https://wearipedia.readthedocs.io).

## Citing

A paper is in progress!

## Disclaimer

This project is currently in *alpha*. This means that test coverage is limited, and the codebase is still really a prototype. Moreover, the API is unstable, as we are still rapidly iterating on it. Expect for most things to work, but also small bugs, rough edges, and sparse documentation.

## Contributing

As Wearipedia is still at an early stage, we are not yet accepting contributions from the broader community. Once Wearipedia reaches its first stable release, we will begin accepting contributions.

## License

Wearipedia is released under the MIT license.

## Credits [![🚀 Your next Python package needs a bleeding-edge project structure.](https://img.shields.io/badge/python--package--template-%F0%9F%9A%80-brightgreen)](https://github.com/TezRomacH/python-package-template)

This project was generated with [`python-package-template`](https://github.com/TezRomacH/python-package-template)
