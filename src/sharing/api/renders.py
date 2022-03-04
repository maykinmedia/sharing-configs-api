from rest_framework.renderers import BaseRenderer


class BinaryFileRenderer(BaseRenderer):
    media_type = "application/octet-stream"
    format = "binary"
    charset = None
    render_style = "binary"

    def render(self, data: bytes, media_type=None, renderer_context=None):
        return data
