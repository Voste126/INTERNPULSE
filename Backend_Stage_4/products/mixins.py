from django.core.cache import cache

class RateLimitBodyMixin:
    """
    Mixin to add dynamic rate-limit information into the response body.
    It calculates the current request count using the throttle's cache key.
    """
    def finalize_response(self, request, response, *args, **kwargs):
        # Call parent's finalize_response() to get the original response.
        response = super().finalize_response(request, response, *args, **kwargs)
        
        if isinstance(response.data, dict):
            rate_headers = {}
            # Iterate through throttles (assumes one throttle is used, e.g., AnonRateThrottle)
            for throttle in self.get_throttles():
                rate = throttle.get_rate()
                if rate is not None:
                    try:
                        # Example rate: "100/min"
                        limit_str, period = rate.split('/')
                        limit = int(limit_str)
                        period = period.lower()
                        if period == 'min':
                            duration = 60
                        elif period == 'sec':
                            duration = 1
                        elif period == 'hour':
                            duration = 3600
                        else:
                            duration = 60  # fallback
                    except Exception:
                        continue

                    # Use get_cache_key() to retrieve the cache key.
                    cache_key = throttle.get_cache_key(request, self)
                    current_requests_val = cache.get(cache_key, [])
                    # If the cache value is a list, use its length; otherwise, assume it's an int.
                    if isinstance(current_requests_val, list):
                        current_requests = len(current_requests_val)
                    else:
                        current_requests = current_requests_val

                    remaining = max(limit - current_requests, 0)

                    # Attempt to call throttle.wait(); if it fails, default to duration.
                    try:
                        wait_time = throttle.wait()
                        if wait_time is None:
                            wait_time = duration
                        else:
                            wait_time = int(wait_time)
                    except AttributeError:
                        wait_time = duration
                    
                    rate_headers = {
                        "X-RateLimit-Limit": limit,
                        "X-RateLimit-Remaining": remaining,
                        "X-RateLimit-Reset": wait_time,
                    }
                    break

            # Wrap the original response data into the standardized structure.
            new_data = {
                "product": response.data,
                "status": "success",
                "message": "Request processed successfully.",
                "headers": rate_headers,
            }
            response.data = new_data
        return response
