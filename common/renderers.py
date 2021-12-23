from rest_framework.renderers import JSONRenderer


class CustomRenderer(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context['response'].status_code
        response = {
            'code': status_code,
            'message': renderer_context['response'].status_text,
            'data': data,
        }

        renderer_context['response'].status_code = 200
        renderer_context['response'].data = response

        return super().render(response, accepted_media_type, renderer_context)
