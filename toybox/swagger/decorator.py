import marshmallow
import logging
from functools import partial
from collections import ChainMap
from pyramid import httpexceptions
from pyramid.interfaces import IRequest
from zope.interface import implementer


logger = logging.getLogger(__name__)


@implementer(IRequest)
class WrappedRequest(object):
    def __init__(self, request, serializer=None):
        self.request = request
        self.serializer = serializer

    def __getattr__(self, name):
        return getattr(self.request, name)

    def set_wrapped(self, name, value, wrapper=ChainMap):
        setattr(self, name, wrapper(value, getattr(self.request, name)))

    @property
    def __class__(self):
        return self.request.__class__


class ValidatedViewDecorator(object):
    def __init__(self, input, output, view):
        # todo: string support
        self.input = input
        self.output = output
        self.view = view

    def __call__(self, context, request):
        method_name = "{}{}".format(request.method[0].upper(), request.method[1:].lower())
        if hasattr(self.input, method_name):
            request = self.wrap_request(request, method_name)
        response = self.view(context, request)
        return response

    INPUT_MAPPING = [
        ("Path", "matchdict"),
        ("Query", "GET"),
        ("Header", "headers"),
        ("Body", "json"),
        ("Form", "POST"),
    ]

    def wrap_request(self, request, method_name):
        input = getattr(self.input, method_name)
        wr = WrappedRequest(request, serializer=self.make_serialize(request, method_name))
        for schema_name, req_attr in self.INPUT_MAPPING:
            schema_cls = getattr(input, schema_name, None)
            if schema_cls is None:
                continue
            try:
                schema = schema_cls(strict=True)
                deserialized, _ = schema.load(getattr(request, req_attr))
                wr.set_wrapped(req_attr, deserialized)
            except marshmallow.ValidationError as e:
                return self.on_input_error(wr, e, as_json=True)
            except Exception as e:
                return self.on_input_error(wr, e)
        return wr

    def make_serialize(self, request, method_name):
        def serialize(response, value):
            status_code = response.status_code
            output_name = "{}{}".format(method_name, status_code)
            schema_cls = getattr(self.output, output_name, None)
            if schema_cls is None:
                logger.debug("skip: output schema %s is not found.", output_name)
                return value
            try:
                schema = schema_cls(strict=True)
                serialized, _ = schema.dump(value)
                # marshmallow's validation is only when deserialization.
                schema.load(value)
                return serialized
            except marshmallow.ValidationError as e:
                return self.on_output_error(response, value, e, as_json=True)
            except Exception as e:
                return self.on_output_error(response, value, e)
        return serialize

    def on_input_error(self, wrequest, e, as_json=False):
        exc = httpexceptions.HTTPBadRequest()
        if as_json:
            exc.body_template_obj = _ThroughBodyTemplate(e.messages)
        raise exc

    def on_output_error(self, response, value, e, as_json=False):
        exc = httpexceptions.HTTPInternalServerError()
        if as_json:
            exc.body_template_obj = _ThroughBodyTemplate(e.messages)  # with e.data?
        raise exc


class _ThroughBodyTemplate:  # hack: for json respont
    def __init__(self, value):
        self.value = value

    def substitute(self, args):
        return self.value


def withswagger(input, output, cls=ValidatedViewDecorator):
    return partial(cls, input, output)
