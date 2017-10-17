**Note:** The instructions are Mac specific (may work for linux as well. Install `py2app`

### Update standalone app:
Update the script (`result_analyzer.py`) as needed and run the following commands:

remove the dist and build directory if exists:  
`rm -rf build dist`

create updated app:  
`python setup.py py2app`


### Setup

install `py2app`

install `virtualenv`


Navigate to the root directory after cloning the repo.


Make virtual env:  
`virtualenv venv`


Activate the virtual env:  
`. venv/bin/activate`