import typing as t


class BaseRegistryError(Exception):
    pass


class ChildMissingLocator(BaseRegistryError):
    pass


class ChildMissingLocatorValue(BaseRegistryError):
    pass


class ChildNotFound(BaseRegistryError):
    pass


class RegistriesMixin:

    __registries: dict[str, dict[t.Any, type]] = {}

    __registry_type__: str  # default: class name
    __registry_locator__: str

    @classmethod
    def __get_type(cls):
        return getattr(cls, "__registry_type__", cls.__name__)

    @classmethod
    def __get_loc(cls):
        loc = getattr(cls, "__registry_locator__", None)
        if loc is None:
            raise ChildMissingLocator(cls)
        return loc

    @classmethod
    def __get_loc_val(cls):
        value = getattr(cls, cls.__get_loc(), None)
        if value is None:
            raise ChildMissingLocatorValue(cls)
        return value

    def __init_subclass__(cls, **kwargs: t.Any):
        super().__init_subclass__(**kwargs)
        mixin = RegistriesMixin

        if mixin in cls.__bases__:
            cls.__registry_type__ = cls.__get_type()  # enrich
            cls.__get_loc()  # validation
        else:
            store = mixin.__registries.setdefault(cls.__get_type(), {})
            store[cls.__get_loc_val()] = cls

    @classmethod
    def get_child_for(cls, locator_value: t.Any) -> type:
        store = cls.__registries[cls.__registry_type__]
        if locator_value not in store:
            raise ChildNotFound(locator_value)
        return store[locator_value]
