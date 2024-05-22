# mstache

Mustache for Python.

Documentation: [mstache.readthedocs.io](https://mstache.readthedocs.io)

## License

[MIT License](./LICENSE)

## Installation

```python
pip install mstache
```

## Usage

Python:

```python
import mstache

print(mstache.render('Hello {{v}}', {'v': 'World!'}))
# Hello World!
```

Command line:

```sh
$ mstache -j data.json -o output.html template.mustache
```

## Highlights

- The fastest pure-python Mustache implementation to this date.
- Command line interface.
- Spec compliant, but also highly compatible with `Mustache.js`.
- Small codebase, efficiently rendering to `str` or `bytes`,
  either buffered or streaming.
- Fully customizable behavior: cache, property getter, partial resolver,
  stringification, escaping and lambdas.
- No dynamic code generation, both jit and transpiler friendly.

## Considerations

For inter-compatibility with JavaScript (especially `Mustache.js`, enabling
client-side rendering with the same templates), **mstache** must behave
somewhat atypically for a `Python` template engine:

- Mustache blocks stick to JavaScript truthyness
  (`Mustache.js` truthyness emulation):
  - Empty mappings (such as `dict`) are unconditionally truthy.
  - `NaN`/`-NaN` are falsy.
- Mustache blocks loop through any iterable other than mappings and strings
  (`Mustache.js` `Array` handling).
- Non-mapping sized objects will expose a virtual `length` property
  (JavaScript `Array.length` emulation, customizable via `getter` parameter).
- Mapping keys containing dot (`.`) or whitespace (` `) are unreachable,
  (`Mustache.js` property limitation, customizable via `getter` parameter).
- Sequence elements are accessible by positive index in the same way mapping
  integer-keyed items are also accessible when no string key conflicts, as
  properties (JavaScript `Object` emulation, customizable via `getter` parameter).

## Syntax

Check out the [mustache(5) manual](https://mustache.github.io/mustache.5.html).

For quick reference, here is a quick overview of the Mustache syntax.

Template (`template.mustache`):
```handlebars
{{!comment}}
<ul>
{{#object}}<li>{{property}}</li>{{/object}}
{{^object}}<li>As <b>object</b> is truthy, this won't be shown</li>{{/object}}
{{^null}}<li><b>null</b> is falsy</li>{{/null}}
{{#array}}<li>{{property}}</li>
{{/array}}
{{^array}}<li>Array isn't empty, this won't be shown.</li>{{/array}}
{{#empty_array}}<li>Empty Array, this won't be shown</li>{{/empty_array}}
{{^empty_array}}<li>empty_array is empty</li>{{/empty_array}}
{{&unescaped_html}}
</ul>
```

Data (`data.json`):
```json
{
  "object": {
    "property": "Object property value"
  },
  "null": null,
  "array": [
    {"property": "Array item1 property"},
    {"property": "Array item2 property"},
    {"property": "Array item3 property"}
  ],
  "empty_array": [],
  "unescaped_html": "<li>this is unescaped html</li>"
}
```

Command:
```sh
$ mstache -j data.json -o output.html template.mustache
```

Output:
```html
<ul>
<li>Object property value</li>
<li><b>null</b> is falsy</li>
<li>Array item1 property</li>
<li>Array item2 property</li>
<li>Array item3 property</li>
<li>empty_array is empty</li>
<li>this is unescaped html</li>
</ul>
```
