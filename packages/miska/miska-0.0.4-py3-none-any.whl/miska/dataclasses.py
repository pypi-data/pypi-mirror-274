import dataclasses


_K_PRIVATE = "private"
_K_METADATA = "metadata"
_BASE_MODEL_INIT_FLAG = "_BASE_MODEL_INIT_FLAG"


def private_field(**kwargs) -> dataclasses.Field:
    kwargs.setdefault(_K_METADATA, {})[_K_PRIVATE] = True
    return dataclasses.field(**kwargs)


class BaseModel:

    __PRIVATES = {}

    as_tuple = dataclasses.astuple
    as_dict =  dataclasses.asdict

    def __post_init__(self):
        self._mark_init_finished()

    def _mark_init_finished(self):
        setattr(self, _BASE_MODEL_INIT_FLAG, False)

    def _setattr(self, key, value):
        return super().__setattr__(key, value)

    def __setattr__(self, key, value):
        if getattr(self, _BASE_MODEL_INIT_FLAG, True):
            return super().__setattr__(key, value)

        privates = self.__PRIVATES.get(self.__class__)
        if privates is None:
            privates = {field.name: field.metadata.get(_K_PRIVATE, False)
                        for field in dataclasses.fields(self)}
            self.__PRIVATES[self.__class__] = privates

        if privates[key]:
            msg = f"Forbidden to modify private attribute: {key}"
            raise AttributeError(msg)

        return super().__setattr__(key, value)
