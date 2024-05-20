# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class AntdCopyText(Component):
    """An AntdCopyText component.


Keyword arguments:

- id (string; optional)

- afterIcon (a list of or a singular dash component, string or number; optional)

- aria-* (string; optional):
    `aria-*`格式属性通配.

- beforeIcon (a list of or a singular dash component, string or number; optional)

- className (string | dict; optional)

- data-* (string; optional):
    `data-*`格式属性通配.

- key (string; optional)

- loading_state (dict; optional)

    `loading_state` is a dict with keys:

    - component_name (string; optional):
        Holds the name of the component that is loading.

    - is_loading (boolean; optional):
        Determines if the component is loading or not.

    - prop_name (string; optional):
        Holds which property is loading.

- locale (a value equal to: 'zh-cn', 'en-us'; default 'zh-cn')

- style (dict; optional)

- text (string; default '')"""
    _children_props = ['beforeIcon', 'afterIcon']
    _base_nodes = ['beforeIcon', 'afterIcon', 'children']
    _namespace = 'feffery_antd_components'
    _type = 'AntdCopyText'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, className=Component.UNDEFINED, style=Component.UNDEFINED, key=Component.UNDEFINED, locale=Component.UNDEFINED, text=Component.UNDEFINED, beforeIcon=Component.UNDEFINED, afterIcon=Component.UNDEFINED, loading_state=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'afterIcon', 'aria-*', 'beforeIcon', 'className', 'data-*', 'key', 'loading_state', 'locale', 'style', 'text']
        self._valid_wildcard_attributes =            ['data-', 'aria-']
        self.available_properties = ['id', 'afterIcon', 'aria-*', 'beforeIcon', 'className', 'data-*', 'key', 'loading_state', 'locale', 'style', 'text']
        self.available_wildcard_properties =            ['data-', 'aria-']
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(AntdCopyText, self).__init__(**args)
