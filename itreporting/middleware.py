from django.shortcuts import redirect
from django.contrib import messages

class RestrictUnauthorizedAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Define restricted paths (add more as necessary)
        restricted_paths = [
            '/module_list/',  # Example: Module list page
            '/courses/',      # Example: Courses page
        ]

        # Redirect to home page if the user is not authenticated
        if not request.user.is_authenticated and request.path in restricted_paths:
            messages.warning(request, "Unauthorized access. Please log in to access this page.")
            return redirect('home')  # Replace 'home' with your home page URL name

        response = self.get_response(request)
        return response
