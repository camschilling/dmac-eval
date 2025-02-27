# dmac-eval
Evaluates DMAC Headcount


## Contributing

### Set Up
```
# create the virtual environment
python -m venv dmac_venv

# activate the environment
.\dmac_venv\Scripts\Activate.ps1

# use the latest version of pip
pip install --upgrade pip

# install dependencies
pip install -r requirements.txt
```

### Pre Commit Hooks
Includes linting at this stage. `pre-commit run --all-files`

### Linting
Uses ruff. `ruff check . --fix

### Testing
Uses pytest. 
```
pytest -s -v <file_path>
pytest -s -v <file_path>::<test_name>
pytest -s -v <file_path>::<test_name>[<test_parameter>]
```
