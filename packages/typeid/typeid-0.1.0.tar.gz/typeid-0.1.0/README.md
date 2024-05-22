# UUID-compatible Typed IDs with prefixes.

`typid` is a python library that allows to create specific id types much like
stripe uses them across their platform to distinguish different data models from
their id already. `typeid` is compatible to the UUID library and as such can act
as a drop-in replacement.

A type id has the following string representation:

    user_nnv5rr3rfk3hgry6xrygr
    └──┘ └───────────────────┘
    type    uuid (base58)

## How to use `typeid`

First generate the Types using generate(...), then use them like so:

```python
from uuid_extensions import uuid7
from typeid import generate

# Generate a bunch of new id types
generate("sk", "pk", "user", "apikey")

# Now they can be used with SkId, PkId, UserId, and ApikeyId
assert str(SkId(uuid7().hex)).startswith("sk_")
assert str(PkId(uuid7().hex)).startswith("pk_")
assert str(UserId(uuid7().hex)).startswith("user_")
assert str(ApikeyId(uuid7().hex)).startswith("apikey_")

# Obviously, loading a prefixed type id in the correct Type works just fine
assert (UserId("user_nnv5rr3rfk3hgry6xrygr").hex == "0664c4135ed83faabd4bc0dc33839c9f")

# Use custom suffixes, just in case you need them
generate("admin", suffix="IdUseWithCare")
assert str(AdminIdUseWithCare(uuid7().hex)).startswith("admin_")
```
