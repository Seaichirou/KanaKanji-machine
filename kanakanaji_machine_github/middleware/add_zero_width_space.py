# middleware/add_zero_width_space.py

class AddZeroWidthSpaceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST' and 'text' in request.POST:
            text = request.POST.get('text', '')
            if not text.startswith('\u200B'):
                request.POST = request.POST.copy()
                request.POST['text'] = '\u200B' + text
        
        response = self.get_response(request)
        return response
