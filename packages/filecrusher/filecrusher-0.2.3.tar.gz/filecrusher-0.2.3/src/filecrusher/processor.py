from functools import wraps


def processor(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        for handler in self.event_handlers:
            if hasattr(handler, "preprocess"):
                handler.preprocess(*args, **kwargs)

        try:
            ret = method(self, *args, **kwargs)
        except Exception as e:
            raise RuntimeError(f"[!] Processing Failed during {self.__class__.__name__} stage.") from e

        for handler in self.event_handlers:
            if hasattr(handler, "postprocess"):
                handler.postprocess(*args, **kwargs)
        return ret

    return wrapper
