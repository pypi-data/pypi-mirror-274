def _get_recursive_subclasses(cls):
    """Return list of all subclasses for a class, including subclasses of direct subclasses"""
    return cls.__subclasses__() + [g for s in cls.__subclasses__() for g in _get_recursive_subclasses(s)]


def _get_full_qualname(cls):
    """Return fully qualified class name"""
    return cls.__module__ + '.' + cls.__name__


def discover_wrapper(wrapped_func):
    """
    Return a function that returns a dictionary of autodiscovered classtypes based on a wrapped_func
    Args:
        wrapped_func: Function() ->
            [
                "import_path.to.classes",
                BaseClassToSearchFor,
                Function(cls_inst) -> unique_name:str | None, to exclude from list
            ]

    Returns:
        {
            "cls1": Class1,
            ..
        }

    """
    import pkgutil
    import importlib

    imp_path, bscls, cmd_uniq = wrapped_func()

    mod = importlib.import_module(imp_path)

    modules = pkgutil.iter_modules(mod.__path__, mod.__name__ + ".")
    for mod in modules:
        importlib.import_module(mod.name)

    commands = dict()
    for cmd in _get_recursive_subclasses(bscls):
        unique_name = cmd_uniq(cmd)
        if unique_name is None:
            continue  # Skip this one

        existing_cmd = commands.get(unique_name)
        if existing_cmd:
            raise ValueError("Duplicate command name '{}'! Already loaded '{}' Will not load '{}'".format(
                cmd.name,
                _get_full_qualname(existing_cmd),
                _get_full_qualname(cmd)
            ))
        else:
            commands[unique_name] = cmd

    # Remember that this is a wrapper func, still need to return a function
    return lambda: commands

