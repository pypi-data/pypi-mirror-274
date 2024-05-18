# Testing Publishing PyPi Package

Very cool indeed.


## Setup
##### Create virtual environment
`python -m venv venv`
`source venv/bin/activate`
`pip install -r requirements.txt`
##### Create virtual environment (publishing)
`python -m venv venv_publish`
`source venv_publish/bin/activate`
`pip install wheel twine`

##### Publish first version of the package
Set version to "0.0.1" `setup.py`.
`source venv_publish/bin/activate`
`python setup.py sdist bdist_wheel`
`twine upload dist/*`


## Testing
##### Activate virtual environment
`source venv/bin/activate`
##### Run all tests
`python -m unittest discover -v tests`
##### Run specific test
`python -m unittest -v tests.xxx`


## Publishing
##### Publish new version of the package
Increment version in `setup.py`.
`source venv_publish/bin/activate`
`python setup.py sdist bdist_wheel`
`twine upload dist/*`