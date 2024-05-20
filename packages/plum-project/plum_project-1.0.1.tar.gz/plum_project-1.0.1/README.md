# Plum Project

An in house ETL framework for moving data to where it has to go.

## References

Here are the repository references for quick access.

### Project Maintainers

- [Automated Testing](./docs/project/automated-testing.md)

## Development

You need to supply a `.env` file under `test_databases/postgres` for the database setup.

Running the postgres database independantly...

```sh
docker rmi postgres-postgres -f && \
docker system prune -f && \
docker compose -f ./test_databases/postgres/docker-compose.yml up
```
## Building Package

The below command will build the package locally.

```sh
python setup.py sdist bdist_wheel
```

## Releasing To PyPi

The below command will release the package to PyPi leverage a secrets file stored locally in `$HOME/.pypirc`.

```sh
python -m twine upload dist/*
```

Below is a example of the `.pypirc` file contents. The password aka token is provided from PyPi.

```
[pypi]
username = __token__
password = pypi-XXXX
```