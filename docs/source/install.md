(installation)=

# Installation

Wearipedia can be installed on virtually any computer with Python. Wearipedia officially supports Python 3.8, 3.9, 3.10, and PyPy.

## Anaconda

[Anaconda](https://www.anaconda.com/download/) is a free Python distribution from Continuum Analytics that includes many useful libraries for scientific computing and data analysis. We recommend using Anaconda if you're new to Python or if you're using Wearipedia for data analysis.


### Install Anaconda (Mac and Linux)

Download the [Anaconda installer](https://www.anaconda.com/download/#macos) for Mac or [Linux](https://www.anaconda.com/download/#linux). Run the installer and follow the prompts.

### Install Anaconda (Windows)

Download the [Anaconda installer](https://www.anaconda.com/download/#windows) for Windows. Run the installer and follow the prompts.

## Miniconda

[Miniconda](https://docs.conda.io/en/latest/miniconda.html) is a minimal version of Anaconda that includes only the conda package manager and Python. In general, Miniconda is much smaller than Anaconda, but Conda should still provide you with all of the libraries you'll need to use Wearipedia. Miniconda is a good choice if you're limited on disk space.

### Install Miniconda (Mac and Linux)

Download the [Miniconda installer](https://docs.conda.io/en/latest/miniconda.html) for Mac or [Linux](https://docs.conda.io/en/latest/miniconda.html). Run the installer and follow the prompts.

### Install Miniconda (Windows)

Download the [Miniconda installer](https://docs.conda.io/en/latest/miniconda.html) for Windows. Run the installer and follow the prompts.

## Conda environment

A Conda environment is a separate Python installation from your system Python. The advantage of using a separate Conda environment is that you can ensure that the Python libraries you're using are exactly the ones you need, and that you can safely upgrade or downgrade these libraries without breaking other software on your computer.

### Create a Conda environment

Use the following command to create a Conda environment with Python 3.8.

```
conda create -n wearipedia python=3.8
```

Replace `wearipedia` with the name of your project and `python=3.8` with the version of Python you wish to use.

To activate your Conda environment, use the following command:

```
conda activate wearipedia
```

To deactivate your Conda environment, use the following command:

```
conda deactivate
```

## Install Wearipedia

Once you have installed Anaconda or Miniconda and have entered your Conda environment, you can install Wearipedia by using the pip command.

To install the latest official release, use the following command:

```
pip install wearipedia
```

To install the latest development version, use the following command:

```
pip install https://github.com/wearipedia/wearipedia/archive/master.zip
```

## Verify Installation

To verify that Wearipedia is installed correctly, navigate to the directory where you wish to create your project and type the following command into a terminal:

```
wearipedia --help
```

If you see a list of Wearipedia commands, as shown, below, your installation was successful.

![wearipedia help](https://raw.githubusercontent.com/wearipedia/wearipedia/master/docs/img/wearipedia-help.png)

To verify that Wearipedia is using the correct version of Python, type the following command:

```
wearipedia --version
```

You should see the version of Python that you are using.

![wearipedia version](https://raw.githubusercontent.com/wearipedia/wearipedia/master/docs/img/wearipedia-version.png)

## Upgrade to the Latest Version

To upgrade to the latest official version of Wearipedia, use the following command:

```
pip install wearipedia --upgrade
```

To upgrade to the latest development version of Wearipedia, use the following command:

```
pip install https://github.com/wearipedia/wearipedia/archive/master.zip --upgrade
```

## Questions

If you have a question about installation, please [open an issue](https://github.com/wearipedia/wearipedia/issues/new/choose) on the Wearipedia GitHub repository.
