(installation)=

# Installation

Wearipedia can be installed on virtually any computer with Python.

<!--The SymPy CAS can be installed on virtually any computer with Python.
SymPy does require [mpmath] Python library to be installed first.  The
recommended method of installation is through Anaconda, which includes
mpmath, as well as several other useful libraries.  Alternatively, some Linux
distributions have SymPy packages available.-->

Wearipedia officially supports Python 3.8, 3.9, 3.10, and PyPy.

## Anaconda

[Anaconda](https://www.anaconda.com/download/) is a free Python distribution from
Continuum Analytics that includes SymPy, Matplotlib, IPython, NumPy, and many
more useful packages for scientific computing. This is recommended because
many nice features of SymPy are only enabled when certain libraries are
installed.  For example, without Matplotlib, only simple text-based plotting
is enabled.  With the IPython notebook or qtconsole, you can get nicer
$\mathrm{\LaTeX}$ printing by running `init_printing()`.

If you already have Anaconda and want to update Wearipedia to the latest version,
use:

```
conda update wearipedia
```

(installation-git)=
## Git

If you wish to contribute to Wearipedia or like to get the latest updates as they
come, install Wearipedia from git. To download the repository, execute the
following from the command line:

```
git clone https://github.com/sympy/wearipedia.git
```

To update to the latest version, go into your repository and execute:

```
git pull origin master
```

If you want to install Wearipedia, but still want to use the git version, you can run
from your repository:

```
python setupegg.py develop
```

This will cause the installed version to always point to the version in the git
directory.

## Other Methods

You may also install Wearipedia using pip or from source. In addition, most Linux
and Python distributions have some Wearipedia version available to install using
their package manager. Here is a list of several such Python distributions:

- [Anaconda](https://www.anaconda.com/download/)
- [Enthought Canopy](https://www.enthought.com/product/canopy/)
- [ActivePython](https://www.activestate.com/activepython)
- [Spack](https://spack.io/)

## Run Wearipedia

After installation, it is best to verify that your freshly-installed Wearipedia
works. To do this, start up Python and import the Wearipedia libraries:

```
$ python
>>> from wearipedia import *
```

From here, execute some simple Wearipedia statements like the ones below:

```
>>> device = wearipedia.get_device("whoop/whoop_4")
>>> limit(sin(x)/x, x, 0)
1
>>> integrate(1/x, x)
log(x)
```

For a starter guide on using Wearipedia effectively, refer to the {ref}`intro-tutorial`.

(mpmath-install)=
## mpmath

Versions of SymPy prior to 1.0 included [mpmath], but it now depends on it as
an external dependency.  If you installed SymPy with Anaconda, it will already
include mpmath. Use:

```
conda install mpmath
```

to ensure that it is installed.

If you do not wish to use Anaconda, you can use `pip install mpmath`.

If you use mpmath via `sympy.mpmath` in your code, you will need to change
this to use just `mpmath`. If you depend on code that does this that you
cannot easily change, you can work around it by doing:

```
import sys
import mpmath
sys.modules['sympy.mpmath'] = mpmath
```

before the code that imports `sympy.mpmath`. It is recommended to change
code that uses `sympy.mpmath` to use `mpmath` directly wherever possible.

## Questions

If you have a question about installation or SymPy in general, feel free to
visit our chat on [Gitter]. In addition, our [mailing list] is an excellent
source of community support.

If you think there's a bug or you would like to request a feature, please open
an [issue ticket].

[downloads site]: https://github.com/sympy/sympy/releases
[gitter]: https://gitter.im/sympy/sympy
[issue ticket]: https://github.com/sympy/sympy/issues
[mailing list]: https://groups.google.com/forum/#!forum/sympy
[mpmath]: http://mpmath.org/
