
# Python Virtual Environment Guide

## TO ACTIVATE
```bash
source ~/.venv/bin/activate
```

## TO DEACTIVATE
```bash
deactivate
```

## TO INSTALL A PACKAGE
```bash
python3 -m pip install xyz
```

## PROBLEM

When attempting to install a package using `pip3 install`, you might encounter the following error:

```bash
dushyant.bansal@blr-dushyant pyprojects % pip3 install yaml
error: externally-managed-environment

× This environment is externally managed
╰─> To install Python packages system-wide, try brew install
    xyz, where xyz is the package you are trying to
    install.

    If you wish to install a Python library that isn't in Homebrew,
    use a virtual environment:

    python3 -m venv path/to/venv
    source path/to/venv/bin/activate
    python3 -m pip install xyz

    If you wish to install a Python application that isn't in Homebrew,
    it may be easiest to use 'pipx install xyz', which will manage a
    virtual environment for you. You can install pipx with

    brew install pipx

    You may restore the old behavior of pip by passing
    the '--break-system-packages' flag to pip, or by adding
    'break-system-packages = true' to your pip.conf file. The latter
    will permanently disable this error.

    If you disable this error, we STRONGLY recommend that you additionally
    pass the '--user' flag to pip, or set 'user = true' in your pip.conf
    file. Failure to do this can result in a broken Homebrew installation.

    Read more about this behavior here: <https://peps.python.org/pep-0668/>
```

## SOLUTION

To resolve this issue, create and use a virtual environment:

### 1. Create a virtual environment
```bash
mkdir ~/.venv
python3 -m venv ~/.venv
```

### 2. Activate the virtual environment
```bash
source ~/.venv/bin/activate
```

### 3. Install packages in the virtual environment
```bash
python3 -m pip install <module_name>
```

### 4. Deactivate the virtual environment
```bash
deactivate
```

Now, you can safely manage and install Python packages without encountering the "externally-managed-environment" error.

