def const(cls):
    # Replace a class's attributes with properties,
    # and itself with an instance of its doppelganger.
    is_special = lambda name: (name.startswith("__") and name.endswith("__"))
    class_contents = {n: getattr(cls, n) for n in vars(cls) if not is_special(n)}
    def unbind(value):  # Get the value out of the lexical closure.
        return lambda self: value
    propertified_contents = {name: property(unbind(value))
                             for (name, value) in class_contents.items()}
    receptor = type(cls.__name__, (object,), propertified_contents)
    return receptor()  # Replace with an instance, so properties work.


