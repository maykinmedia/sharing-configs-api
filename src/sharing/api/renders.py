import json

from rest_framework.renderers import BaseRenderer


class BinaryFileRenderer(BaseRenderer):
    media_type = "application/octet-stream"
    format = "binary"
    charset = None
    render_style = "binary"

    def render(self, data, media_type=None, renderer_context=None):
        # When trying to download a non-existing file, `data` contains a string or a dict instead of binary data.
        if isinstance(data, dict):
            data = json.dumps(data)

        if isinstance(data, str):
            return data.encode("utf-8")
        return data
