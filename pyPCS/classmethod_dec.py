
def once_per_arg(func):
    def wrapper(*args, **kwargs):
        # attr1, attr2 = wrapper.attr1, wrapper.attr2
        # if attr1 is None and attr2 is None:
        #     wrapper.attr1, wrapper.attr2 = args[:2]
        # elif attr1 == args[0] and attr2 == args[1]:
        #     pass
        #     # raise ValueError("You have made the same transportation before.")
        return func(*args, **kwargs)
    wrapper.attr1 = None
    wrapper.attr2 = None
    return wrapper
