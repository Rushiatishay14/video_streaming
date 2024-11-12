import json
import logging
from django.http import HttpRequest, HttpResponse
from django.utils.timezone import now
from django.utils.deprecation import MiddlewareMixin
from .models import UserActivityTracking  # Update the import path accordingly

logger = logging.getLogger('api_logger')

class APILoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        # Start timer
        start_time = now()

        # Initialize log data for the request
        log_data = {
            'timestamp': str(start_time),
            'path': request.path,
            'method': request.method,
            'user_agent': request.META.get('HTTP_USER_AGENT', ''),
            'referer': request.META.get('HTTP_REFERER', ''),
            'ip_address': self.get_client_ip(request),
            'user': request.user.email if request.user.is_authenticated else 'Anonymous',
            'request_data': self.get_request_data(request)
        }

        # Log request headers (optional)
        log_data['headers'] = dict(request.headers)

        # Log the request
        logger.info(f"Request: {json.dumps(log_data, indent=2)}")

        # Get response
        response = self.get_response(request)

        # Calculate response time
        response_time = (now() - start_time).total_seconds() * 1000  # in milliseconds

        # Log response details
        response_log_data = {
            'status_code': response.status_code,
            'response_time': response_time,
            'response_data': self.get_response_data(response),
            'headers': dict(response.headers)
        }

        # Log the response
        logger.info(f"Response: {json.dumps(response_log_data, indent=2)}")

        # Save logged data to the UserActivityTracking model (optional)
        if request.user.is_authenticated:
            UserActivityTracking.objects.create(
                user=request.user,
                ip_address=log_data['ip_address'],
                url=log_data['path'],
                request_type=log_data['method'],
                request_data=log_data['request_data'],
                user_agent=log_data['user_agent'],
                referer=log_data['referer'],
                city=request.user.city if hasattr(request.user, 'city') else '',
                state=request.user.state if hasattr(request.user, 'state') else '',
                country=request.user.country if hasattr(request.user, 'country') else '',
                pincode=request.user.pincode if hasattr(request.user, 'pincode') else '',
                status_code=response.status_code,
                response_time=response_time,
                response=response_log_data['response_data']
            )

        return response

    def get_request_data(self, request: HttpRequest):
        try:
            return json.loads(request.body.decode('utf-8')) if request.body else None
        except json.JSONDecodeError:
            return None

    def get_response_data(self, response: HttpResponse):
        try:
            return json.loads(response.content.decode('utf-8')) if response.content else None
        except json.JSONDecodeError:
            return None

    def get_client_ip(self, request: HttpRequest):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')

class CustomHeaderMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        response['Cross-Origin-Opener-Policy'] = 'same-origin'
        response['Cross-Origin-Embedder-Policy'] = 'require-corp'
        return response
