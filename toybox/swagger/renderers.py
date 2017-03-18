from pyramid.renderers import JSON


class ValidatedJSON(JSON):
    SERIALIZWER_ATTR_NAME = "serializer"

    def __call__(self, info):
        """ Returns a plain JSON-encoded string with content-type
        ``application/json``. The content-type may be overridden by
        setting ``request.response.content_type``."""
        def _render(value, system):
            request = system.get('request')
            if request is not None:
                response = request.response
                ct = response.content_type
                if ct == response.default_content_type:
                    response.content_type = 'application/json'
            return self.serialize(request, response, value)
        return _render

    def serialize(self, request, response, value):
        serializer = getattr(request, self.SERIALIZWER_ATTR_NAME, None)
        if serializer is not None:
            value = serializer(response, value)
        default = self._make_default(request)
        return self.serializer(value, default=default, **self.kw)
