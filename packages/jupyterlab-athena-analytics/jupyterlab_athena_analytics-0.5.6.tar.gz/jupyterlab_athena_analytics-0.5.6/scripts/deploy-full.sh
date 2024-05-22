#!/bin/bash

# pip install build twine hatch

if [ -z "$ATHENA_PYPI_TOKEN" ]
then
  echo "Error: ATHENA_PYPI_TOKEN is not set."
  exit 1
fi

jlpm clean:all && git clean -dfX && python -m build && twine upload dist/*