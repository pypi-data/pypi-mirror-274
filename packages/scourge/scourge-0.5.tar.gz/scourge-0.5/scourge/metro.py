from deceit.exceptions import ApiException
from deceit.api_client import ApiClient


class MetroApiException(ApiException):
    pass


class MetroApi(ApiClient):
    def __init__(self, conf, *args, key=None, base_url=None,
                 default_timeout=None, **kwargs):
        super().__init__(
            conf=conf,
            *args,
            base_url=base_url or conf.get('base_url'),
            default_timeout=default_timeout or conf.get('default_timeout'),
            **kwargs)
        self.key = key or conf.get('key')

    def headers(self, *args, **kwargs):
        return {
            'authorization': self.key,
        }

    def raw_track(self, tracking_number, **kwargs):
        route = 'GetTrackingSummary'
        json_data = {
            'trackingNumber': tracking_number,
        }
        return self.post(route, json_data=json_data, **kwargs)

    def transit_history(self, tracking_number, timezone='America/Los_Angeles', **kwargs):
        route = 'GetTransitHistory'
        json_data = {
            'trackingNumber': tracking_number,
            'timezone': timezone
        }
        return self.post(route, json_data=json_data, **kwargs)

    def tracking_details(self, tracking_number, **kwargs):
        route = 'GetTrackingDetails'
        json_data = {
            'trackingNumber': tracking_number,
        }
        return self.post(route, json_data=json_data, **kwargs)
