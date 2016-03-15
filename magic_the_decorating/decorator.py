class DecorateNotImplemented(Exception):
    """
    Simple exception that is raised when the base class method
        ._decorate is called.
    """
    pass


class Base(object):
    """
    Includes many convenience methods common to most decorators.
    Decorators should subclass this class.

    """
    def __init__(self, signature):
        """
        Inits the base decorator.

        @param signature - String signature for decorator

        """
        self._set_signature(signature)

    def _set_signature(self, signature):
        """
        Sets the decorators signature.

        @param signature - String similar to '__this_is_a_signature__'.
            The '__' prefrix and suffix will be added automatically if not
            present.
        """
        affix = '__'
        if not signature.startswith(affix):
            signature = affix + signature
        if not signature.endswith(affix):
            signature = signature + affix
        self._signature = signature

    def _set_decorated(self, o):
        """
        Signs the object o with a signature.

        @param o - Object

        """
        setattr(o, self._signature, True)

    def _has_decorated(self, o):
        """
        Checks the object o for the signature.

        @param o - Object

        """
        return hasattr(o, self._signature)

    def _decorate(self, obj, config):
        """
        Raise an exception. Subclasses need to implement this.

        @param obj - Object to decorate
        @param config - Dict
        @raises DecorateNotImplemented.

        """
        raise DecorateNotImplemented(
            "need to implement _decorate in subclasses"
        )

    def __call__(self, obj, config):
        """
        Makes instances callable.

        @param obj - Object to decorate
        @param config - Dictionary configuring the calling.
        @return - Returns the decorated object

        """
        if self._has_decorated(obj):
            return obj
        obj = self._decorate(obj, config)
        self._set_decorated(obj)
        return obj
