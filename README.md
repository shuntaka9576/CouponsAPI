CouponsAPI
====
[![CircleCI](https://circleci.com/gh/shuntaka9576/CouponsAPI/tree/master.svg?style=shield)](https://circleci.com/gh/shuntaka9576/CouponsAPI/tree/master)
[![codecov](https://codecov.io/gh/shuntaka9576/CouponsAPI/branch/master/graph/badge.svg?token=fl4LunL5u7)](https://codecov.io/gh/shuntaka9576/CouponsAPI)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

## Requirements
* python(3.7.x)
* sam
* pip
* pipenv
* make
* docker
* docker-compose
* aws cli

## Test
```bash
docker-compose up -d # Launch localstack
./script/createDynamo.sh localstack # Create the required local stack environment
cd ./lambdaFunctions
make dep-dev # Install python libs
make test # Run pytest
```

## Deploy
```bash
make deploy
```

## SwaggerUI
### Local
Launch SwaggerUI container at http://localhost:1000.
```bash
make swagger
```

### Live demo
Put a following URL in [SwaggerUI](https://petstore.swagger.io/?_ga=2.95204319.279429875.1555660631-1287431053.1555660631).
```
https://raw.githubusercontent.com/shuntaka9576/CouponsAPI/master/swagger/generate_prod_swagger.json
```
