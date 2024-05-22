"""
mstache module.

This module alone implements the entire mstache library, including its
minimal command line interface.

The main functions are considered to be :func:`cli`, :func:`render` and
:func:`stream`, and they expose different approaches to template rendering:
command line interface, buffered and streaming rendering API, respectively.

Other functionality will be considered **advanced**, exposing some
implementation-specific complexity and potentially non-standard behavior
which could reduce compatibility with other mustache implementations and
future major mstache revisions.

"""
"""
mstache, Mustache for Python
============================

See `README.md`_, `project documentation`_ and `project repository`_.

.. _README.md: https://mstache.readthedocs.io/en/latest/README.html
.. _project documentation: https://mstache.readthedocs.io
.. _project repository: https://gitlab.com/ergoithz/mstache


License
-------

Copyright (c) 2021-2024, Felipe A Hernandez.

MIT License (see `LICENSE`_).

.. _LICENSE: https://gitlab.com/ergoithz/mstache/-/blob/master/LICENSE

"""

import codecs
import collections
import collections.abc
import math
import types
import typing

__author__ = 'Felipe A Hernandez'
__email__ = 'ergoithz@gmail.com'
__license__ = 'MIT'
__version__ = '0.2.0'
__all__ = (
    # api
    'tokenize',
    'stream',
    'render',
    'cli',
    # exceptions
    'TokenException',
    'ClosingTokenException',
    'UnclosedTokenException',
    'DelimiterTokenException',
    'TemplateRecursionError',
    # defaults
    'default_recursion_limit',
    'default_resolver',
    'default_getter',
    'default_stringify',
    'default_escape',
    'default_lambda_render',
    'default_tags',
    'default_cache',
    'default_cache_make_key',
    'default_virtuals',
    # types
    'TString',
    'PartialResolver',
    'PropertyGetter',
    'StringifyFunction',
    'EscapeFunction',
    'LambdaRenderFunctionConstructor',
    'VirtualPropertyFunction',
    'VirtualPropertyMapping',
    'TagsTuple',
    'TagsByteTuple',
    'CompiledToken',
    'CompiledTemplate',
    'CompiledTemplateCache',
    'CacheMakeKeyFunction',
    )

K = typing.TypeVar('K')
"""Generic."""

T = typing.TypeVar('T')
"""Generic."""

D = typing.TypeVar('D')
"""Generic."""

TString = typing.TypeVar('TString', str, bytes)
"""String/bytes generic."""

PartialResolver = collections.abc.Callable[[typing.AnyStr], typing.AnyStr]
"""Template partial tag resolver function interface."""

PropertyGetter = collections.abc.Callable[
    [typing.Any, collections.abc.Sequence, typing.AnyStr, typing.Any],
    typing.Any,
    ]
"""Template property getter function interface."""

StringifyFunction = collections.abc.Callable[[bytes, bool], bytes]
"""Template variable general stringification function interface."""

EscapeFunction = collections.abc.Callable[[bytes], bytes]
"""Template variable value escape function interface."""

LambdaRenderFunctionConstructor = collections.abc.Callable[
    ...,
    collections.abc.Callable[..., typing.AnyStr],
    ]
"""Lambda render function constructor interface."""

LambdaRenderFunctionFactory = LambdaRenderFunctionConstructor
"""
.. deprecated:: 0.1.3
    Use :attr:`LambdaRenderFunctionConstructor` instead.

"""

VirtualPropertyFunction = collections.abc.Callable[[typing.Any], typing.Any]
"""Virtual property implementation callable interface."""

VirtualPropertyMapping = collections.abc.Mapping[str, VirtualPropertyFunction]
"""Virtual property mapping interface."""

TagsTuple = tuple[typing.AnyStr, typing.AnyStr]
"""Mustache tag tuple interface."""

TagsByteTuple = tuple[bytes, bytes]
"""Mustache tag byte tuple interface."""

CompiledToken = tuple[bool, bool, bool, bytes, bytes, int]
"""
Compiled template token.

Tokens are tuples containing a renderer decision path, key, content and flags.

``type: bool``
    Decision for rendering path node `a`.

``type: bool``
    Decision for rendering path node `b`.

``type: bool``
    Decision for rendering path node `c`

``key: bytes``
    Template substring with token scope key.

``content: bytes`
    Template substring with token content data.

``flags: int``
    Token flags.

    - Unused: ``-1`` (default)
    - Variable flags:
        - ``0`` - escaped
        - ``1`` - unescaped
    - Block start flags:
        - ``0`` - falsy
        - ``1`` - truthy
    - Block end value: block content index.

"""

CompiledTemplate = tuple[CompiledToken, ...]
"""
Compiled template interface.

.. seealso::

    :py:attr:`mstache.CompiledToken`
        Item type.

    :py:attr:`mstache.CompiledTemplateCache`
        Interface exposing this type.

"""


class CompiledTemplateCache(typing.Protocol):
    """
    Cache object protocol.

    .. seealso::

        :py:attr:`mstache.CompiledTemplate`
            Item type.

        :py:attr:`mstache.CacheMakeKeyFunction`
            Cache key function interface.

    """

    def get(self, key: K) -> CompiledTemplate | None:
        """Get compiled template from key, if any."""

    def __setitem__(self, key: K, value: CompiledTemplate) -> None:
        """Assign compiled template to key."""


CacheMakeKeyFunction = typing.Callable[
    [tuple[bytes, bytes, bytes, bool]],
    collections.abc.Hashable,
    ]
"""
Cache mapping key function interface.

.. seealso::

    :py:attr:`mstache.CompiledTemplateCache`
        Interface exposing this type.

"""


class LRUCache(collections.OrderedDict, typing.Generic[T]):
    """Capped mapping discarding least recently used elements."""

    def __init__(self, maxsize: int, *args, **kwargs) -> None:
        """
        Initialize.

        :param maxsize: maximum number of elements will be kept

        Any parameter excess will be passed straight to dict constructor.

        """
        self.maxsize = maxsize
        super().__init__(*args, **kwargs)

    def get(self, key: collections.abc.Hashable, default: D = None) -> T | D:
        """
        Get value for given key or default if not present.

        :param key: hashable
        :param default: value will be returned if key is not present
        :returns: value if key is present, default if not

        """
        try:
            return self[key]
        except KeyError:
            return default  # type: ignore

    def __getitem__(self, key: collections.abc.Hashable) -> T:
        """
        Get value for given key.

        :param key: hashable
        :returns: value if key is present
        :raises KeyError: if key is not present

        """
        self.move_to_end(key)
        return super().__getitem__(key)

    def __setitem__(self, key: collections.abc.Hashable, value: T) -> None:
        """
        Set value for given key.

        :param key: hashable will be used to retrieve values later on
        :param value: value for given key

        """
        super().__setitem__(key, value)
        try:
            self.move_to_end(key)
            while len(self) > self.maxsize:
                self.popitem(last=False)
        except KeyError:  # race condition
            pass


default_recursion_limit = 1024
"""
Default number of maximum nested renders.

A nested render happens whenener the lambda render parameter is used or when
a partial template is injected.

Meant to avoid recursion bombs on templates.

"""

default_tags = b'{{', b'}}'
"""Tuple of default mustache tags as in `tuple[bytes, bytes]`."""

default_cache: CompiledTemplateCache = LRUCache(1024)
"""
Default template cache mapping, keeping the 1024 most recently used
compiled templates (LRU expiration).
"""

default_cache_make_key: CacheMakeKeyFunction = tuple
"""
Defaut template cache key function, :py:class:`tuple`, so keys would be
as in `tuple[bytes, bytes, bytes, bool]` containing the relevant
:py:func:`mstache.tokenizer` parameters.
"""


def virtual_length(ref: collections.abc.Sized) -> int:
    """
    Resolve virtual length property.

    :param ref: any non-mapping object implementing `__len__`
    :returns: number of items
    :raises TypeError: if ref is mapping or has no `__len__` method

    """
    if isinstance(ref, collections.abc.Mapping):
        raise TypeError
    return len(ref)


default_virtuals: VirtualPropertyMapping = types.MappingProxyType({
    'length': virtual_length,
    })
"""
Immutable mapping with default virtual properties.

The following virtual properties are implemented:

- **length**, for non-mapping sized objects, returning ``len(ref)``.

"""

TOKEN_TYPES = tuple({
    **dict.fromkeys(range(0x100), (True, False, True, False)),
    0x21: (False, False, False, False),  # '!'
    0x23: (False, True, True, False),  # '#'
    0x26: (True, True, True, True),  # '&'
    0x2F: (False, True, False, False),  # '/'
    0x3D: (False, False, False, True),  # '='
    0x3E: (False, False, True, False),  # '>'
    0x5E: (False, True, True, True),  # '^'
    0x7B: (True, True, False, True),  # '{'
    }.values())
"""ASCII-indexed tokenizer decision matrix."""

COMMON_FALSY: tuple = None, False, 0, '', b'', (), [], frozenset()
NON_LOOPING_TYPES: tuple = str, bytes, collections.abc.Mapping
EMPTY = b''
SELF_SCOPE = frozenset((b'.', '.'))
MISSING = object()


class TokenException(SyntaxError):
    """Invalid token found during tokenization."""

    _fmt = 'Invalid tag {tag} at line {row} column {column}'

    @classmethod
    def from_template(
            cls,
            template: bytes,
            start: int,
            end: int,
            ) -> 'TokenException':
        """
        Create exception instance from parsing data.

        :param template: template bytes
        :param start: character position where the offending tag starts at
        :param end: character position where the offending tag ends at
        :returns: exception instance

        """
        tag = template[start:end].decode(errors='replace')
        row = 1 + template[:start].count(b'\n')
        column = 1 + start - max(0, template.rfind(b'\n', 0, start))
        return cls(cls._fmt.format(tag=tag, row=row, column=column))


class ClosingTokenException(TokenException):
    """Non-matching closing token found during tokenization."""

    _fmt = 'Non-matching tag {tag} at line {row} column {column}'


class UnclosedTokenException(ClosingTokenException):
    """Unclosed token found during tokenization."""

    _fmt = 'Unclosed tag {tag} at line {row} column {column}'


class DelimiterTokenException(TokenException):
    """
    Invalid delimiters token found during tokenization.

    .. versionadded:: 0.1.1

    """

    _fmt = 'Invalid delimiters {tag} at line {row} column {column}'


class TemplateRecursionError(RecursionError):
    """Template rendering exceeded maximum render recursion."""


def default_stringify(data: typing.Any, text: bool) -> bytes:
    """
    Convert arbitrary data to bytes.

    :param data: value will be serialized
    :param text: whether running in text mode or not (bytes mode)
    :returns: template bytes

    """
    return (
        data if isinstance(data, bytes) and not text else
        f'{data}'.encode()
        )


def default_escape(data: bytes) -> bytes:
    """
    Convert bytes conflicting with HTML to their escape sequences.

    :param data: bytes containing text
    :returns: escaped text bytes

    """
    return (
        data
        .replace(b'&', b'&amp;')
        .replace(b'<', b'&lt;')
        .replace(b'>', b'&gt;')
        .replace(b'"', b'&quot;')
        .replace(b"'", b'&#x60;')
        .replace(b'`', b'&#x3D;')
        )


def default_resolver(name: typing.AnyStr) -> bytes:
    """
    Mustache partial resolver function (stub).

    :param name: partial template name
    :returns: empty bytes

    """
    return EMPTY


def default_getter(
        scope: typing.Any,
        scopes: collections.abc.Iterable,
        key: typing.AnyStr,
        default: typing.Any = None,
        *,
        virtuals: VirtualPropertyMapping = default_virtuals,
        ) -> typing.Any:
    """
    Extract property value from scope hierarchy.

    :param scope: uppermost scope (corresponding to key ``'.'``)
    :param scopes: parent scope sequence
    :param key: property key
    :param default: value will be used as default when missing
    :param virtuals: mapping of virtual property callables
    :returns: value from scope or default

    .. versionadded:: 0.1.3
       *virtuals* parameter.

    Both :class:`AttributeError` and :class:`TypeError` exceptions
    raised by virtual property implementations will be handled as if
    that property doesn't exist, which can be useful to filter out
    incompatible types.

    """
    if key in SELF_SCOPE:
        return scope

    binary_mode = not isinstance(key, str)
    components = key.split(b'.' if binary_mode else '.')  # type: ignore
    for ref in (*scopes, scope)[::-1]:
        for name in components:
            if binary_mode:
                try:
                    ref = ref[name]
                    continue
                except (KeyError, TypeError, AttributeError):
                    pass

                try:
                    name = name.decode()  # type: ignore
                except UnicodeDecodeError:
                    break

            try:
                ref = ref[name]
                continue
            except (KeyError, TypeError, AttributeError):
                pass

            if name.isdigit():
                try:
                    ref = ref[int(name)]
                    continue
                except (TypeError, KeyError, IndexError):
                    pass
            else:
                try:
                    ref = getattr(ref, name)  # type: ignore
                    continue
                except AttributeError:
                    pass

            try:
                ref = virtuals[name](ref)  # type: ignore
                continue
            except (KeyError, TypeError, AttributeError):
                pass

            break

        else:
            return ref

    return default


def default_lambda_render(
        scope: typing.Any,
        **kwargs,
        ) -> collections.abc.Callable[[TString], TString]:
    r"""
    Generate a template-only render function with fixed parameters.

    :param scope: current scope
    :param \**kwargs: parameters forwarded to :func:`render`
    :returns: template render function

    """

    def lambda_render(template: TString) -> TString:
        """
        Render given template to string/bytes.

        :param template: template text
        :returns: rendered string or bytes (depending on template type)

        """
        return render(template, scope, **kwargs)

    return lambda_render


def tokenize(
        template: bytes,
        *,
        tags: TagsByteTuple = default_tags,
        comments: bool = False,
        cache: CompiledTemplateCache = default_cache,
        cache_make_key: CacheMakeKeyFunction = default_cache_make_key,
        ) -> CompiledTemplate:
    """
    Compile mustache template as a tuple of token tuples.

    :param template: template as utf-8 encoded bytes
    :param tags: mustache tag tuple (open, close)
    :param comments: whether yield comment tokens or not (ignore comments)
    :param cache: mutable mapping for compiled template cache
    :param cache_make_key: key function for compiled template cache
    :returns: tuple of token tuples

    :raises UnclosedTokenException: if token is left unclosed
    :raises ClosingTokenException: if block closing token does not match
    :raises DelimiterTokenException: if delimiter token syntax is invalid

    """
    tokenization_key = cache_make_key((template, *tags, comments))

    if cached := cache.get(tokenization_key):
        return cached

    template_find = template.find

    stack: list[tuple[bytes | None, int, int, int]] = []
    stack_append = stack.append
    stack_pop = stack.pop
    scope_label = None
    scope_head = 0
    scope_start = 0
    scope_index = 0

    empty = EMPTY
    start_tag, end_tag = tags
    end_literal = b'}' + end_tag
    end_switch = b'=' + end_tag
    start_len = len(start_tag)
    end_len = len(end_tag)

    token_types = TOKEN_TYPES
    recording: list[CompiledToken] = []
    record = recording.append

    text_start, text_end = 0, template_find(start_tag)
    while text_end != -1:
        if text_start < text_end:  # text
            record((
                False, True, False,
                empty,
                template[text_start:text_end],
                -1,
                ))

        tag_start = text_end + start_len
        try:
            a, b, c, d = token_types[template[tag_start]]
        except IndexError:
            raise UnclosedTokenException.from_template(
                template=template,
                start=text_end,
                end=tag_start,
                ) from None

        if a:  # variables
            tag_start += b

            if c:  # variable
                tag_end = template_find(end_tag, tag_start)
                text_start = tag_end + end_len

            else:  # triple-keyed variable
                tag_end = template_find(end_literal, tag_start)
                text_start = tag_end + end_len + 1

            record((
                False, True, True,
                template[tag_start:tag_end].strip(),
                empty,
                d,
                ))

        elif b:
            tag_start += 1
            tag_end = template_find(end_tag, tag_start)
            text_start = tag_end + end_len

            if c:  # block
                stack_append((scope_label, text_end, scope_start, scope_index))
                scope_label = template[tag_start:tag_end].strip()
                scope_head = text_end
                scope_start = text_start
                scope_index = len(recording) + 1
                record((
                    True, False, True,
                    scope_label,
                    empty,
                    d,
                    ))

            elif scope_label != template[tag_start:tag_end].strip():
                raise ClosingTokenException.from_template(
                    template=template,
                    start=text_end,
                    end=text_start,
                    )

            else:  # close / loop
                record((
                    True, True, True,
                    scope_label,
                    template[scope_start:text_end].strip(),
                    scope_index,
                    ))
                scope_label, scope_head, scope_start, scope_index = stack_pop()

        elif c:  # partial
            tag_start += 1
            tag_end = template_find(end_tag, tag_start)
            text_start = tag_end + end_len
            record((
                True, False, False,
                template[tag_start:tag_end].strip(),
                empty,
                -1,
                ))

        elif d:  # tags
            tag_start += 1
            tag_end = template_find(end_switch, tag_start)
            text_start = tag_end + end_len + 1

            try:
                start_tag, end_tag = template[tag_start:tag_end].split(b' ')
            except ValueError:
                raise DelimiterTokenException.from_template(
                    template=template,
                    start=text_end,
                    end=text_start,
                    ) from None

            if not (start_tag and end_tag):
                raise DelimiterTokenException.from_template(
                    template=template,
                    start=text_end,
                    end=text_start,
                    )

            end_literal = b'}' + end_tag
            end_switch = b'=' + end_tag
            start_len = len(start_tag)
            end_len = len(end_tag)
            start_end = tag_start + start_len
            end_start = tag_end - end_len

            record((
                False, False, True,
                template[tag_start:start_end].strip(),
                template[end_start:tag_end].strip(),
                -1,
                ))

        else:  # comment
            tag_start += 1
            tag_end = template_find(end_tag, tag_start)
            text_start = tag_end + end_len

            if comments:
                record((
                    False, False, False,
                    empty,
                    template[tag_start:tag_end].strip(),
                    -1,
                    ))

        if tag_end < 0:
            raise UnclosedTokenException.from_template(
                template=template,
                start=tag_start,
                end=tag_end,
                )

        text_end = template_find(start_tag, text_start)

    if stack:
        raise UnclosedTokenException.from_template(
            template=template,
            start=scope_head,
            end=scope_start,
            )

    if (tail := template[text_start:]) or not recording:
        record((False, True, False, empty, tail, -1))  # text

    tokens = cache[tokenization_key] = tuple(recording)
    return tokens


def process(
        template: TString,
        scope: typing.Any,
        *,
        scopes: collections.abc.Iterable = (),
        resolver: PartialResolver = default_resolver,
        getter: PropertyGetter = default_getter,
        stringify: StringifyFunction = default_stringify,
        escape: EscapeFunction = default_escape,
        lambda_render: LambdaRenderFunctionConstructor = default_lambda_render,
        tags: TagsTuple = default_tags,
        cache: CompiledTemplateCache = default_cache,
        cache_make_key: CacheMakeKeyFunction = default_cache_make_key,
        recursion_limit: int = default_recursion_limit,
        ) -> collections.abc.Generator[bytes, None, None]:
    """
    Generate rendered mustache template byte chunks.

    :param template: mustache template string
    :param scope: root object used as root mustache scope
    :param scopes: iterable of parent scopes
    :param resolver: callable will be used to resolve partials (bytes)
    :param getter: callable will be used to pick variables from scope
    :param stringify: callable will be used to render python types (bytes)
    :param escape: callable will be used to escape template (bytes)
    :param lambda_render: lambda render function constructor
    :param tags: mustache tag tuple (open, close)
    :param cache: mutable mapping for compiled template cache
    :param cache_make_key: key function for compiled template cache
    :param recursion_limit: maximum number of nested render operations
    :returns: byte chunk generator

    :raises UnclosedTokenException: if token is left unclosed
    :raises ClosingTokenException: if block closing token does not match
    :raises DelimiterTokenException: if delimiter token syntax is invalid
    :raises TemplateRecursionError: if rendering recursion limit is exceeded

    """
    if recursion_limit < 0:
        message = 'Template rendering exceeded maximum render recursion'
        raise TemplateRecursionError(message)

    text_mode = isinstance(template, str)
    next_recursion_level = recursion_limit - 1

    # encoding
    data: bytes = (
        template.encode() if text_mode else  # type: ignore
        template
        )
    current_tags: TagsByteTuple = tuple(  # type: ignore
        tag.encode() if isinstance(tag, str) else tag
        for tag in tags[:2]
        )

    # current context
    siblings: collections.abc.Iterator | None = None
    callback = False
    silent = False

    # context stack
    stack: list[tuple[collections.abc.Iterator | None, bool, bool]] = []
    stack_append = stack.append
    stack_pop = stack.pop

    # scope stack
    scopes = list(scopes)
    scopes_append = scopes.append
    scopes_pop = scopes.pop

    # locals
    decode: typing.Callable[[bytes], typing.AnyStr] = (
        bytes.decode if text_mode else  # type: ignore
        bytes
        )
    isnan = math.isnan
    missing = MISSING
    falsies = COMMON_FALSY
    non_looping = NON_LOOPING_TYPES
    mappings = collections.abc.Mapping

    start = 0
    tokens = tokenized = tokenize(
        data,
        tags=current_tags,
        cache=cache,
        cache_make_key=cache_make_key,
        )
    while True:
        for a, b, c, token_name, token_content, token_option in tokens:
            if silent:
                if a:
                    if b:  # close / loop
                        closing_scope = scope
                        closing_callback = callback

                        scope = scopes_pop()
                        siblings, callback, silent = stack_pop()

                        if closing_callback and not silent:
                            yield stringify(
                                closing_scope(
                                    decode(token_content),
                                    lambda_render(
                                        scope=scope,
                                        scopes=scopes,
                                        resolver=resolver,
                                        getter=getter,
                                        stringify=stringify,
                                        escape=escape,
                                        lambda_render=lambda_render,
                                        tags=current_tags,
                                        cache=cache,
                                        cache_make_key=cache_make_key,
                                        recursion_limit=next_recursion_level,
                                        ),
                                    ),
                                text_mode,
                                )

                    elif c:  # block
                        scopes_append(scope)
                        stack_append((siblings, callback, silent))

            elif a:
                if b:  # close / loop
                    if siblings:
                        try:
                            scope = next(siblings)
                            callback = callable(scope)
                            silent = callback

                            if start != token_option:
                                start = token_option
                                tokens = tokenized[start:]

                            break  # restart
                        except StopIteration:
                            scope = scopes_pop()
                            siblings, callback, silent = stack_pop()
                    else:
                        scope = scopes_pop()
                        siblings, callback, silent = stack_pop()

                elif c:  # block
                    curr = scope
                    scope = getter(curr, scopes, decode(token_name), None)

                    scopes_append(curr)
                    stack_append((siblings, callback, silent))

                    falsy = (
                        hasattr(scope, '__float__') and isnan(scope)
                        if scope else
                        scope in falsies or not isinstance(scope, mappings)
                        )
                    if token_option:  # falsy block
                        siblings = None
                        callback = False
                        silent = not falsy
                    elif falsy:  # truthy block with falsy value
                        siblings = None
                        callback = False
                        silent = True
                    elif (hasattr(scope, '__iter__')
                          and not isinstance(scope, non_looping)):  # loop
                        try:
                            siblings = iter(scope)
                            scope = next(siblings)  # type: ignore
                            callback = callable(scope)
                            silent = callback
                        except StopIteration:
                            siblings = None
                            scope = None
                            callback = False
                            silent = True
                    else:  # truthy block with truthy value
                        siblings = None
                        callback = callable(scope)
                        silent = callback

                else:  # partial
                    value = resolver(decode(token_name))
                    if value:
                        yield from process(
                            template=value,
                            scope=scope,
                            scopes=scopes,
                            resolver=resolver,
                            getter=getter,
                            stringify=stringify,
                            escape=escape,
                            lambda_render=lambda_render,
                            tags=current_tags,
                            cache=cache,
                            cache_make_key=cache_make_key,
                            recursion_limit=next_recursion_level,
                            )

            elif b:
                if c:  # variable
                    value = getter(scope, scopes, decode(token_name), missing)
                    if value is not missing:
                        yield (
                            stringify(value, text_mode) if token_option else
                            escape(stringify(value, text_mode))
                            )

                else:  # text
                    yield token_content

            elif c:  # tags
                current_tags = token_name, token_content

            # else comment

        else:
            break


def stream(
        template: TString,
        scope: typing.Any,
        *,
        scopes: collections.abc.Iterable = (),
        resolver: PartialResolver = default_resolver,
        getter: PropertyGetter = default_getter,
        stringify: StringifyFunction = default_stringify,
        escape: EscapeFunction = default_escape,
        lambda_render: LambdaRenderFunctionConstructor = default_lambda_render,
        tags: TagsTuple = default_tags,
        cache: CompiledTemplateCache = default_cache,
        cache_make_key: CacheMakeKeyFunction = default_cache_make_key,
        recursion_limit: int = default_recursion_limit,
        ) -> collections.abc.Generator[TString, None, None]:
    """
    Generate rendered mustache template chunks.

    :param template: mustache template (str or bytes)
    :param scope: current rendering scope (data object)
    :param scopes: list of precedent scopes
    :param resolver: callable will be used to resolve partials (bytes)
    :param getter: callable will be used to pick variables from scope
    :param stringify: callable will be used to render python types (bytes)
    :param escape: callable will be used to escape template (bytes)
    :param lambda_render: lambda render function constructor
    :param tags: tuple (start, end) specifying the initial mustache delimiters
    :param cache: mutable mapping for compiled template cache
    :param cache_make_key: key function for compiled template cache
    :param recursion_limit: maximum number of nested render operations
    :returns: generator of bytes/str chunks (same type as template)

    :raises UnclosedTokenException: if token is left unclosed
    :raises ClosingTokenException: if block closing token does not match
    :raises DelimiterTokenException: if delimiter token syntax is invalid
    :raises RenderingRecursionError: if rendering recursion limit is exceeded

    """
    chunks = process(
        template=template,
        scope=scope,
        scopes=scopes,
        resolver=resolver,
        getter=getter,
        stringify=stringify,
        escape=escape,
        lambda_render=lambda_render,
        tags=tags,
        cache=cache,
        cache_make_key=cache_make_key,
        recursion_limit=recursion_limit,
        )
    return (
        codecs.iterdecode(chunks, 'utf8') if isinstance(template, str) else
        chunks
        )


def render(
        template: TString,
        scope: typing.Any,
        *,
        scopes: collections.abc.Iterable = (),
        resolver: PartialResolver = default_resolver,
        getter: PropertyGetter = default_getter,
        stringify: StringifyFunction = default_stringify,
        escape: EscapeFunction = default_escape,
        lambda_render: LambdaRenderFunctionConstructor = default_lambda_render,
        tags: TagsTuple = default_tags,
        cache: CompiledTemplateCache = default_cache,
        cache_make_key: CacheMakeKeyFunction = default_cache_make_key,
        recursion_limit: int = default_recursion_limit,
        ) -> TString:
    """
    Render mustache template.

    :param template: mustache template
    :param scope: current rendering scope (data object)
    :param scopes: list of precedent scopes
    :param resolver: callable will be used to resolve partials (bytes)
    :param getter: callable will be used to pick variables from scope
    :param stringify: callable will be used to render python types (bytes)
    :param escape: callable will be used to escape template (bytes)
    :param lambda_render: lambda render function constructor
    :param tags: tuple (start, end) specifying the initial mustache delimiters
    :param cache: mutable mapping for compiled template cache
    :param cache_make_key: key function for compiled template cache
    :param recursion_limit: maximum number of nested render operations
    :returns: rendered bytes/str (type depends on template)

    :raises UnclosedTokenException: if token is left unclosed
    :raises ClosingTokenException: if block closing token does not match
    :raises DelimiterTokenException: if delimiter token syntax is invalid
    :raises TemplateRecursionError: if rendering recursion limit is exceeded

    """
    data = b''.join(process(
        template=template,
        scope=scope,
        scopes=scopes,
        resolver=resolver,
        getter=getter,
        stringify=stringify,
        escape=escape,
        lambda_render=lambda_render,
        tags=tags,
        cache=cache,
        cache_make_key=cache_make_key,
        recursion_limit=recursion_limit,
        ))
    return data.decode() if isinstance(template, str) else data


def cli(argv: collections.abc.Sequence[str] | None = None) -> None:
    """
    Render template from command line.

    Use `python -m mstache --help` to check available options.

    :param argv: command line arguments, :attr:`sys.argv` when None

    """
    import argparse
    import json
    import sys

    arguments = argparse.ArgumentParser(
        description='Render mustache template.',
        )
    arguments.add_argument(
        'template',
        metavar='PATH',
        type=argparse.FileType('r'),
        help='template file',
        )
    arguments.add_argument(
        '-j', '--json',
        metavar='PATH',
        type=argparse.FileType('r'),
        default=sys.stdin,
        help='JSON file, default: stdin',
        )
    arguments.add_argument(
        '-o', '--output',
        metavar='PATH',
        type=argparse.FileType('w'),
        default=sys.stdout,
        help='output file, default: stdout',
        )
    args = arguments.parse_args(argv)
    try:
        args.output.write(render(args.template.read(), json.load(args.json)))
    finally:
        args.template.close()
        for fd, std in ((args.json, sys.stdin), (args.output, sys.stdout)):
            if fd is not std:
                fd.close()


if __name__ == '__main__':
    cli()
