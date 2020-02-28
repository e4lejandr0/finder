#!/bin/bash

THIS_DIR="$(readlink -f "$(dirname "${BASH_SOURCE[0]}")")"
export PROJECT_DIR="$(readlink -f "${THIS_DIR}/..")"
export PATH="${THIS_DIR}/bin:${PATH}"
exec pipenv shell
