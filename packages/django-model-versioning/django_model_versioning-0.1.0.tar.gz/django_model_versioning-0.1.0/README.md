# Django Model Versioning
This library is used to create a model that get automatically versioned when specific fields are updated. When creating a relationship to such amodel you can choose if you want to create a standard relationship, that will connect your record to that specific version of the model, or create a relationship that will always point to the most updated version of the versioned entity instead.

## Usage
1. First create the model you'd like to version like you'd normally do.
```python
# myproject/taxes/models.py
from django.db.models import Model, CharField, DateTimeField, DecimalField


class Tax(Model):
    name = CharField(max_length=255, blank=False, null=False)
    percentage_value = DecimalField(max_digits=10, decimal_places=2, default=0)

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
```
2. Then within your app create a `versioning.py` file
```python
from lib.register import register
from lib.versioning_options import VersioningOptions
from taxes.models import Tax


@register(Tax)
class TaxVersioningOptions(VersioningOptions):
    versioned_fields = ('percentage_value',)
```
* We user `@register(Tax)` to tell django that these versioning options refer to the `Tax` model.
* The name of the class is unimportant, but it has to inherit from `VersioningOptions`
* Then we create the `versioned_fields` property and we specify which fields from the `Tax` model (or whatever model you register these options for) should be versioned. Whenever a versioned_field gets updated, a new version of the model is created and all references get updated.
3. Now we create a model that refers to that specific instance. We can just use a standard `ForeignKey` since the nehaviour we need here is the stadard one for Django references
```python
from django.db.models import Model, IntegerField, DO_NOTHING, DateTimeField, ForeignKey

from taxes.models import Tax


class Payment(Model):
    amount = IntegerField()

    tax = ForeignKey(Tax, on_delete=DO_NOTHING)

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
```
So in this case, each `Payment` we created will always refer to the same version of `Tax`
4. Now we create another model. This time we ant our new model to always refer to the last version of `Tax`
```python
from django.db.models import Model, CharField, IntegerField, DateTimeField, DO_NOTHING

from lib.versioned_foreign_key import VersionedForeignKey
from taxes.models import Tax


class Product(Model):
    name = CharField(max_length=255, null=False, blank=False)
    price = IntegerField(null=False, default=0)

    tax = VersionedForeignKey(Tax, on_delete=DO_NOTHING)

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
```
As we can see in the example, this time we don't use a `ForeignField` but rather a `VersionedForeignField`