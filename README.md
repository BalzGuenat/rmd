# `rmd` - Remote Markdown

`rmd` is a python script that acts as a markdown compiler by calling a `api.github.com/markdown`-like API.
It is built on top of `requests`.

# `rmds` - Remote Markdown Server

`rmds` is a python script that acts as a server that provides a `api.github.com/markdown`-like API.
It uses `pandoc` as its underlying compiler.

## Installing the Server

1. Install `pandoc`.
2. `git clone https://github.com/BalzGuenat/rmd.git`

## Starting the Server

`python rmds.py`

## Calling the API

### With `rmd`

Write the generated HTML to a file:

`python rmd.py README.md -o README.html`

Without the `-o` option, the HTML is written to `stdout` and can be piped (this can result in encoding errors on Windows):

`python rmd.py README.md > README.html`

If you want to call a different API:

`python rmd.py -url https://api.github.com/markdown README.md`

Get more info on usage with:

`python rmd.py -h`

### With `curl`

If the `'Content-type'` header is set to `text/markdown`, you don't need to wrap the markdown in a JSON. This makes calling the API with curl relatively easy:

`curl -H 'Content-type: text/markdown' --data-binary @README.md http://localhost:8001 > README.html`
