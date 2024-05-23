m = {}


def distribute(func):
    def _deal(name, msg):
        cal = m.get(name)
        if cal is not None:
            return cal(msg)
        else:
            return func(msg)

    return _deal


# 只是编译时执行
def add(name):
    def _add_m(func):
        m[name] = func

    return _add_m


@distribute
def target_fun(msg):
    print('other', msg)
