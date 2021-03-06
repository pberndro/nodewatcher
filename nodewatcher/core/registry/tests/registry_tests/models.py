from django.db import models

from nodewatcher.core.registry import registration, fields


class Thing(models.Model):
    foo = models.CharField(max_length=30, null=True)
    bar = models.IntegerField(null=True)

registration.create_point(Thing, 'first')
registration.create_point(Thing, 'second')


class AnotherRegistryItem(registration.bases.ThingFirstRegistryItem):
    interesting = models.CharField(max_length=30, default='nope', null=True)

    class RegistryMeta:
        registry_id = 'foo.another'

registration.point('thing.first').register_item(AnotherRegistryItem)


class SimpleRegistryItem(registration.bases.ThingFirstRegistryItem):
    interesting = models.CharField(max_length=30, default='nope', null=True)
    level = fields.RegistryChoiceField('thing.first', 'foo.simple#level', null=True)

    class RegistryMeta:
        registry_id = 'foo.simple'

registration.point('thing.first').register_choice('foo.simple#level', registration.Choice('level-x', "Level 0"))
registration.point('thing.first').register_choice('foo.simple#level', registration.Choice('level-a', "Level 1"))
registration.point('thing.first').register_choice('foo.simple#level', registration.Choice('level-m', "Level 2"))
registration.point('thing.first').register_item(SimpleRegistryItem)


class ChildRegistryItem(SimpleRegistryItem):
    additional = models.IntegerField(null=True)

registration.point('thing.first').register_item(ChildRegistryItem)


class RelatedModel(models.Model):
    name = models.CharField(max_length=30)
    level = fields.RegistryChoiceField('thing.first', 'foo.simple#level', null=True)


class DoubleChildRegistryItem(ChildRegistryItem):
    another = models.IntegerField(null=True, default=17)
    related = models.ForeignKey(RelatedModel, null=True)

    class RegistryMeta(ChildRegistryItem.RegistryMeta):
        lookup_proxies = ['another']

registration.point('thing.first').register_item(DoubleChildRegistryItem)


class MultipleRegistryItem(registration.bases.ThingSecondRegistryItem):
    foo = models.IntegerField(null=True)

    class RegistryMeta:
        registry_id = 'foo.multiple'
        multiple = True

registration.point('thing.second').register_item(MultipleRegistryItem)


class FirstSubRegistryItem(MultipleRegistryItem):
    bar = models.IntegerField(null=True)

registration.point('thing.second').register_item(FirstSubRegistryItem)


class SecondSubRegistryItem(MultipleRegistryItem):
    moo = models.IntegerField(null=True)

registration.point('thing.second').register_item(SecondSubRegistryItem)


class ThirdSubRegistryItem(MultipleRegistryItem):
    moo = models.IntegerField(null=True)

registration.point('thing.second').register_item(ThirdSubRegistryItem)
