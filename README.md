
# Python Virtual Environment Guide
## TO PUSH
```bash
git push origin main
```

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

### A. Getting Started
```bash
################
# Get Eng
################
#1 Check for the name of your Parasha in the Eng Data base
./data/torah_parashot_eng.json

#2 Put that name & data into eng now file
#  Copy from { to } and delete the ,
#  Change       "Name": "Balak", --> "Parasha": "Balak",
./data/now_parasha.json

#3 Run the Eng script, run option 2
python3 new_getEng.py 
Choose an option:
1. Open english Torah Site
2. Get parasha: Balak
3. Get the chapter from a link
4. Get specific parasha details
Please enter a number: 1 through 5.: 2

# SUCCESS
Formatted document saved as: tanakh_docs/eng_docs/Balak/Numbers_25.docx.docx
Have a nice Day !

#4
python3 new_getEng.py

################
# Get Heb
################
#1 Check for the name of your Parasha in the Heb Data base
./data/now_parasha_heb.json:4:      "Name": "Beshalach"

#2 Put that name & data into heb now file
#  Copy from { to } and delete the ,
#  Don't forget to add the num of the Parasha, can be found in "data/ParashaOrder.txt"
./data/now_parasha_heb.json

#3 Run the Heb script, 
python3 new_getHeb.py

Would you like to add notes to the verses? (yes/no): yes
...
# SUCCESS
Document saved and formatted: tanakh_docs/output_docs/Balak_Bamidbar_Numbers Chapter_25 Verses_1_9.docx
File has been updated and saved.
```

