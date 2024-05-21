# a Jupyter server extension that supports file globbing

This extension allows you to use file globbing in Jupyter.

You issue a URL like `/api/globbing/some/path/*.ipynb`
and it returns a list of all the files that match the glob pattern

## Installation

```bash
pip install jupyter-server-globbing
```

## Usage

```javascript
// from the browser console
response = await fetch("/api/globbing/some/path/*.ipynb")
files = await response.json()
```
the result is a list of objects with the following structure:

```json
  {
    "path": "some/path/file1.ipynb",  // relative to the server root
    "type": "file" // or "directory"
  }
```
