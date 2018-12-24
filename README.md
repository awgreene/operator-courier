# Operator Courier

The Operator Courier is used to build, validate and push Operator Artifacts.

## Building and running the tool locally with pip
```bash
# The `-e` option will reflect code changes in `operator-courier` calls without a rebuild
$ pip install --user  -e .

$ operator-courier
```

## Testing
### Prereqs
Install [Nose](https://nose.readthedocs.io/en/latest/)
```bash
$ pip install nose
```

### Running the tests
```bash 
$ python3 setup.py test
```
