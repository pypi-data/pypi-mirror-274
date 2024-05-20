# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class AntdWatermark(Component):
    """An AntdWatermark component.


Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    The content of the tab - will only be displayed if this tab is
    selected.

- id (string; optional)

- aria-* (string; optional):
    `aria-*`格式属性通配.

- className (string; optional)

- content (string | list of strings; optional)

- data-* (string; optional):
    `data-*`格式属性通配.

- fontColor (string; optional)

- fontSize (number; default 16)

- gapX (number; default 212)

- gapY (number; default 222)

- height (number; optional)

- image (string; optional)

- key (string; optional)

- loading_state (dict; optional)

    `loading_state` is a dict with keys:

    - component_name (string; optional):
        Holds the name of the component that is loading.

    - is_loading (boolean; optional):
        Determines if the component is loading or not.

    - prop_name (string; optional):
        Holds which property is loading.

- markClassName (string; optional)

- markStyle (dict; optional)

- rotate (number; default -22)

- style (dict; optional)

- width (number; optional)

- zIndex (number; optional)"""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'feffery_antd_components'
    _type = 'AntdWatermark'
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, key=Component.UNDEFINED, className=Component.UNDEFINED, style=Component.UNDEFINED, markClassName=Component.UNDEFINED, markStyle=Component.UNDEFINED, content=Component.UNDEFINED, rotate=Component.UNDEFINED, zIndex=Component.UNDEFINED, fontColor=Component.UNDEFINED, fontSize=Component.UNDEFINED, gapX=Component.UNDEFINED, gapY=Component.UNDEFINED, image=Component.UNDEFINED, width=Component.UNDEFINED, height=Component.UNDEFINED, loading_state=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'aria-*', 'className', 'content', 'data-*', 'fontColor', 'fontSize', 'gapX', 'gapY', 'height', 'image', 'key', 'loading_state', 'markClassName', 'markStyle', 'rotate', 'style', 'width', 'zIndex']
        self._valid_wildcard_attributes =            ['data-', 'aria-']
        self.available_properties = ['children', 'id', 'aria-*', 'className', 'content', 'data-*', 'fontColor', 'fontSize', 'gapX', 'gapY', 'height', 'image', 'key', 'loading_state', 'markClassName', 'markStyle', 'rotate', 'style', 'width', 'zIndex']
        self.available_wildcard_properties =            ['data-', 'aria-']
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        super(AntdWatermark, self).__init__(children=children, **args)
