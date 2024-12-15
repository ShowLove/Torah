#################
# TO ACTIVATE
#################
source ~/.venv/bin/activate

#################
# TO DEACTIVATE
#################
deactivate

#################
# TO INSTALL
#################
python3 -m pip install xyz

#################
# PROBLEM
#################
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

#################
# SOLUTION
#################

mkdir ~/.venv

# create a virtual environment named .venv in your home directory.
python3 -m venv ~/.venv

# to activate the venv
source ~/.venv/bin/activate

# now you can install new packages in this virtual env
python3 -m pip install <module name>

# to deactivate the venv
# source ~/.venv/bin/activate# Torah
