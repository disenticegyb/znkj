import traceback
from functools import wraps
from django.http import HttpResponse, JsonResponse


def handle_exceptions(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        try:
            response = view_func(request, *args, **kwargs)
            if isinstance(response, HttpResponse):
                return response
            else:
                return JsonResponse(response, safe=False)
        except Exception as e:
            print(e)
            traceback.print_exc()
            error_message = str(e)
            return HttpResponse(error_message, status=500)
    return wrapped_view

