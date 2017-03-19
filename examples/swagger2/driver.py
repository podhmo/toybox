from functools import partial
from pyramid_swagger_router.driver import Driver as _Driver
from pyramid_swagger_router.codegen import Codegen
from pyramid_swagger_router.codegen import Context
from swagger_marshmallow_codegen.langhelpers import clsname_from_path


class UnRepr(object):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return self.value


class MyContext(Context):
    SCHEMA_MODULE_NAME = "schema"

    def build_view_setting(self, pattern, route, method, here, renderer="vjson"):
        here.from_(".", self.SCHEMA_MODULE_NAME)
        here.from_("toybox.swagger", "withswagger")
        d = super().build_view_setting(pattern, route, method, renderer=renderer)
        cls_prefix = clsname_from_path(pattern)
        input = "{}.{}Input".format(self.SCHEMA_MODULE_NAME, cls_prefix)
        output = "{}.{}Output".format(self.SCHEMA_MODULE_NAME, cls_prefix)
        d["decorator"] = UnRepr("withswagger({input}, {output})".format(input=input, output=output))
        return d


class Driver(_Driver):
    codegen_factory = partial(Codegen, context_factory=MyContext)
