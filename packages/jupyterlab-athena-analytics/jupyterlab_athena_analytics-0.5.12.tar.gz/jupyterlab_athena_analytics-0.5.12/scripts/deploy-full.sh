#!/bin/bash

# pip install build twine hatch

if [ -z "$ATHENA_PYPI_TOKEN" ]
then
  echo "Error: ATHENA_PYPI_TOKEN is not set."
  exit 1
fi

export TWINE_PASSWORD=$ATHENA_PYPI_TOKEN
# hatch version patch && jlpm clean:all && git clean -dfX && python -m build && twine upload dist/*
python -m build && twine upload dist/*