from lxml import etree

_XPATH_FUNCS = {}
_HASCLASS_EXPR = 'contains(concat(" ", @class, " "), " {} ")'


def register(func):
    fname = func.func_name.replace('_', '-')
    _XPATH_FUNCS[fname] = func
    return func


def setup():
    fns = etree.FunctionNamespace(None)
    for name, func in _XPATH_FUNCS.items():
        fns[name] = func


@register
def has_class(context, *classes):
    """has-class function."""
    expr = ' and '.join([_HASCLASS_EXPR.format(cls) for cls in classes])
    xpath = 'self::*[%s]' % expr
    return bool(context.context_node.xpath(xpath))
