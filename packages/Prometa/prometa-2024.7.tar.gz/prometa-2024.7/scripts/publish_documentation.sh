#!/usr/bin/env bash
set -euo pipefail

SELF=$(readlink -f "${BASH_SOURCE[0]}")
cd -- "${SELF%/*/*}"

function display_help()
{
  local fd
  if [[ $1 != 0 ]]
  then
    fd=2
  else
    fd=1
  fi

  cat >&$fd << HELP
SYNOPSIS
  Build documentation with Sphinx

USAGE
  ${0##*/} [-h] [-v VENV_DIR]

OPTIONS
  -h
    Display this message and exit.

  -v VENV_DIR
    Install dependencies to the Python virtual enviroment at VENV_DIR. It will
    be created if missing.
HELP
  exit "$1"
}

venv=''
while getopts 'hv:' opt
do
  case "$opt" in
    h) display_help 0 ;;
    v) venv=$OPTARG ;;
    *) display_help 1 ;;
  esac
done

if [[ -n $venv ]]
then
  if [[ ! -e "$venv" ]]
  then
    python3 -m venv "$venv"
    source "$venv/bin/activate"
    pip install -U pip
  else
    source "$venv/bin/activate"
  fi
fi

pip install -U -r doc/requirements.txt
sphinx-apidoc -o doc/source -f -H 'API Documentation' src
mkdir -p public
sphinx-build -b html doc/source public
