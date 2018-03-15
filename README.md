# `rmd` - Remote Markdown

`rmd` is a python script that acts as a markdown compiler by calling a `api.github.com/markdown`-like API.

# `rmds` - Remote Markdown Server

`rmds` is a python script that acts as a server that provides a `api.github.com/markdown`-like API.
It uses `pandoc` as its underlying compiler.

## Installing the Server

1. Install `pandoc`.
2. `git clone <this repo>`

## Starting the Server

`python rmds.py`

## Calling the API

### With `rmd`

`python rmd.py`

### With `curl`

`curl -H 'Content-type: text/markdown' --data-binary @README.md http://localhost:8001 > README.html`
