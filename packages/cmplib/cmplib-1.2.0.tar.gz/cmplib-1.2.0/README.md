# cmplib

cmplib is a library used for writing composable matchers for your tests,
validators etc. cmplib's matchers are compared for equality (or inequality)
against your values.

Each matcher provides a human-readable string representation (implemented
by `__repr__` dunder method).

## List of Matchers

### Eq, Ne, Gt, Ge, Lt, Le, Not

Check whether a checked-against value is equal to value stored in matcher,
not equal, greater than, greater or equal, less than or less or equal. Using
of `Not` negates the meaning of stored sub-matcher or value.

```python
assert "abc" == Eq("abc")
assert "abc" == Eq(And(Contains("b"), Len(3)))
assert 1 != Eq(2)
assert 1 == Gt(0)

assert False == Not(Truish())
assert True != Not(Truish())
assert 1 == Not(Gt(1))
assert 1 == Not(2)
```

### Is

Check whether a value is the same object as the one stored in a matcher.

```python
obj = object()

assert obj == Is(obj)
assert list() != Is(list())
```

### IsNone

Check whether a value is `None`.

```python
assert None == IsNone()
assert 0 == Not(IsNone())
assert [] != IsNone()
```

### And, Or

Check whether all sub-matchers match the value (for `All`), or any of them
(for `Or`).

```python
l = [1, 2, 3]
assert l == And(Contains(1), Contains(2))
assert l != And(Contains(1), Contains(2), Contains(3), Contains(4))
assert l == Or(Contains(5), Contains(2))
assert l != Or(Contains(5), Contains(6), Contains(7), Contains(8))
```

Instead of passing matchers directly to `And` or `Or`, they can be composed
with bitwise and operator (`&`) and bitwise or operator (`|`).

```python
l = [1, 2, 3]
assert l == Contains(1) & Contains(2)
assert l == Contains(5) | Contains(2)
```

### Truish

Check whether value casts to `True` boolean, as in `bool(value)`.

```python
assert True == Truish()
assert 1 == Truish()
assert "foo" == Truish()
assert False != Truish()
```

### Len

Check whether container's size matches the matcher.

```python
assert [] == Len(0)
assert [1, 2, 3, "aaa"] == Len(And(Gt(0), Lt(5)))
assert [1, 2, 3, "aaa"] != Len(And(Gt(0), Lt(4)))
```

### IsEmpty

Check whetner container is empty (it's size is 0).

```python
assert [] == IsEmpty()
assert "" == IsEmpty()
assert dict() == IsEmpty()

assert [1] != IsEmpty()
assert "a" != IsEmpty()
```

### Each

Check whether each element of iterable matches the stored sub-matcher or
value.

```python
assert [1, 1, 1] == Each(1)
assert [1, 2, 3] == Each(Not(0))
```

### Values

Check whether iterable contains at least 1 value which matches a stored value
or sub-matcher. Number of required matching values may be changed with
keyword-only argument `at_least`.

_Implementation detail_: for checking whether a container contains a single
value, it's better to use `Contains` which will perform better for
certain types of containers (like sets or dictionaries).

```python
assert [0, 2, 3, 1, 2] == Values(1)
assert [] == Values(1, at_least=0)
assert [0, 2, 3, 1, 2] == Values(Gt(1), at_least=2)

assert [] != Values(1)
assert [0, 2, 3, 1, 2] != Values(1, at_least=2)
```

### Contains

Check whether iterable contains a value which matches stored value or
sub-matcher.

```python
assert [1, 2, 3] == Contains(1)
assert [1, 2, 3] == Contains(Or("a", 2, "b"))
```

### Unordered

Check whether iterable matches stored values or matchers. Each item must
match exactly one matcher, but matching order doesn't matter.

```python
assert [] == Unordered()
assert [1, 2, 3] == Unordered(3, 2, 1)
assert [1, 2, 3] == Unordered(Eq(3), Or(7, 2), 1)

assert [1, 2, 3] != Unordered("1", "2", "3")
```

To perform ordered search, simply construct an iterable of matchers.

```python
assert [1, 2, 3] == [Eq(1), Or(7, 2), 3]
assert [1, 2, 3] != [Eq(3), Or(7, 2), 1]
```

### KeyEq, AttrEq

For `KeyEq` check whether a object stores a value under a key. Key can be
either a key in a dict-like object, or index in a list-like or tuple-like
objects.

```python
d = {"foo": "bar", "baz": "blah"}
assert d == KeyEq("foo", "bar")
assert d == KeyEq("foo", Not(IsEmpty()))
assert d == KeyEq("foo", Not(Contains("h")) & Contains("b") & Contains("a"))


lst = ["foo", "bar"]
assert lst == KeyEq(1, "bar")
assert lst == KeyEq(-1, "bar")
```

For `AttrEq` check whether an object stores a value under attribute.

```python
@dataclass
class Foo:
    foo: str = "bar"
    baz: str = "blah"

o = Foo()

assert o == AttrEq("foo", "bar")
assert o != AttrEq("foo", "blah")
```

### IsInstance

Check whether a value is an instance of a given type.

```python
assert 1 == IsInstance(int)
assert datetime.now() == IsInstance(datetime)
```

### Object, DictFields

Composes a matcher from a keyword-only arguments. Each of these arguments
must match a corresponding attribute (for `Object`) or key (for `DictFields`)
of checked item.

`Object` additionally accepts a single optional, non-keyword argument, which
matches against a type of matched item.

These are convenience matchers. The same effect can be accomplished by using
bare `AttrEq` and `KeyEq` matchers.

```python
@dataclass
class Foo:
    foo: int = 1
    bar: int = 2
    baz: str = "s"
    o: Optional["Foo"] = None

assert Foo() == Object(foo=1, bar=Ge(2))
assert Foo(o=Foo()) == Object(foo=1, o=Object(bar=2, o=None))

assert Foo() != Object(dict, foo=1)
assert Foo() != Object(nonexisting=1)

d = {"foo": 1, "bar": 2, "baz": "s", "o": {"foo": 1}}
assert d == DictFields(foo=1, bar=Ge(2))
assert d == DictFields(foo=1, o=DictFields(foo=1))

assert d != DictFields(foo=1, o=DictFields(foo=2))
assert d != DictFields(foo=1, o=DictFields(nonexisting=2))
```

### Items

Composes a matcher from a index-matcher pairs. Each matcher must match a
value in the compared container under the corresponding index.

```python
lst = ["foo", "bar", "baz", "blah"]
assert lst == Items((0, "foo"), (-1, "blah"))
assert lst == Items((-1, "blah"), (0, "foo"))

assert lst != Items((0, "foo"), (-1, "blah2"))
assert lst != Items((0, "foo"), (100, "foo"))
```

### CanBeTimestamp

Test whether a value can be converted to a UNIX timestamp. UNIX timestamps
are floating point numbers, so this means that any value which can be
converted to the correct float are considered as such.

```python
assert 0 == CanBeTimestamp()
assert "0" == CanBeTimestamp()
assert "0.123" == CanBeTimestamp()
assert datetime.now().timestamp() == CanBeTimestamp()

assert "" != CanBeTimestamp()
assert datetime.now() != CanBeTimestamp()
```

### IsIsoDateTime

Check whether a value represents a valid datetime (either a `date` or
`datetime` object or is a value which follows ISO 8601 format and can be
converted to such value).

```python
assert datetime.now() == IsIsoDateTime()
assert datetime.today() == IsIsoDateTime()
assert datetime.now().isoformat() == IsIsoDateTime()
assert datetime.today().isoformat() == IsIsoDateTime()
assert "2021-01-01" == IsIsoDateTime()

assert "2022-03" != IsIsoDateTime()
```

### IsUnique

Caches values which were already checked against `IsUnique` and matches them
as long as no such value was previously matched. It is possible to specify a
cache name which should hold values. Values are only compared against other
values stored in the same cache. It is possible to clear a particular cache
or all caches

```python
assert 1 == IsUnique("cache-1")
assert 1 == IsUnique("cache-2")
assert 2 == IsUnique("cache-1")

assert 1 != IsUnique("cache-1")

IsUnique.clear("cache-1")
assert 1 == IsUnique("cache-1")
assert 1 != IsUnique("cache-2")

IsUnique.clear()
assert 1 == IsUnique("cache-1")
assert 1 == IsUnique("cache-2")
```

Creating `IsUnique` without a cache name results in generating a new cache
for each instance created this way.

```python
U = IsUnique()
assert 1 == U
assert 1 != U

assert 1 == IsUnique()
assert 1 == IsUnique()
assert [1, 2, 3, 4] == Each(IsUnique())
assert [1, 2, 3, 4, 1, 1, 7] != Each(IsUnique())
```

### Fn

Matches true when a function called with a value passed as the first argument
returns True. When `coerce` is set to True, stored function doesn't have to
return a boolean, but instead its return value is casted to boolean.

```python
assert 1 == Fn(lambda x: x == 1)
assert "1" == Fn((lambda x: x), coerce=True)
```

### SKIP

`SKIP` is a sentinel which always matches true and can be used to mark not
interesing items.

```python
assert [1, 2, 3] == [SKIP, SKIP, SKIP]
assert [1, 2, 3] == [1, SKIP, SKIP]
```

## License

cmplib is licensed under the terms of LGPLv3.
