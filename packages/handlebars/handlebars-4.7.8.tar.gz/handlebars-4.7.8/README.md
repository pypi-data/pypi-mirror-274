# handlebars-py
[handlebars.js](https://github.com/handlebars-lang/handlebars.js) transpiled to python with [js2py](https://github.com/PiotrDabkowski/Js2Py)

## Usage
```python
#!pip install handlebars
from handlebars import Handlebars
template = Handlebars.compile( "Name: {{name}}" )
template({ "name": "Jane" })
# returns: 'Name: Jane'
```


## Development
```bash
pip install -e .[dev]
```
