import re
from urllib.parse import urlencode
from uuid import uuid4

from deceit.exceptions import ApiException
from deceit.api_client import BackendOauth2Client
from requests import Response


class UpsApiException(ApiException):
    pass


class UpsApi(BackendOauth2Client):
    def __init__(self, conf=None, *args, base_url=None, default_timeout=None,
                 exception_class=None, token_url=None,
                 client_id=None, password=None, scopes=None,
                 transaction_source=None,
                 **kwargs):
        if not base_url and conf and not conf.get('base_url'):
            base_url = 'https://onlinetools.ups.com/api'
        if not token_url and conf and not conf.get('token_url'):
            token_url = f'https://onlinetools.ups.com/security/v1/oauth/token'
        super().__init__(
            conf, *args,
            base_url=base_url,
            default_timeout=default_timeout,
            exception_class=exception_class or UpsApiException,
            token_url=token_url,
            client_id=client_id, password=password, scopes=scopes,
            **kwargs)
        key = 'transaction_source'
        self.transaction_source = transaction_source or conf.get(key)
        self.transaction_source = self.transaction_source or 'pypi.scourge'

    @classmethod
    def valid_tracking_number(cls, tracking_number):
        m = r'(1Z ?[0-9A-Z]{3} ?[0-9A-Z]{3} ?[0-9A-Z]{2} ?[0-9A-Z]{4} ?[0-9A-Z]{3} ?[0-9A-Z]' \
            r'|[\dT]\d{3} ?\d{4} ?\d{3})'
        matcher = re.compile(m)
        return matcher.match(tracking_number)

    def headers(self, *args, transaction_id=None, **kwargs):
        return {
            'transactionSrc': self.transaction_source,
            'transId': transaction_id or uuid4().hex
        }

    @classmethod
    def tracking_url(cls, tracking_number):
        base_url = 'https://www.ups.com/track'
        params = {
            'loc': 'en_US',
            'tracknum': tracking_number,
        }
        q = urlencode(params, doseq=True)
        return f'{base_url}?{q}'

    @classmethod
    def filter_activity(cls, activity, type_, *codes):
        if codes:
            rg = [
                x for x in activity
                if x['status']['type'] == type_
                and x['status']['code'] in codes
            ]
        else:
            rg = [
                x for x in activity
                if x['status']['type'] == type_
            ]
        rg.sort(key=lambda lx: lx['date'])
        return rg

    def track(self, tracking_number, **kwargs):
        """
        https://developer.ups.com/en-us/catalog/tracking/view-track-spec
        Args:
            tracking_number (str): the ups tracking number
            **kwargs:

        Returns: a dict in the below format
        ```yaml
        ---
        tracking_number: tracking_number
        ship_date: date
        delivery_date: date
        created_at: date
        updated_at: date
        status: delivered,in_transit,exception,not_shipped
        ```
        """
        result = self.raw_track(tracking_number, **kwargs)
        if isinstance(result, Response):
            return result
        shipment = result['trackResponse']['shipment'][0]
        activity = []
        # note: in few cases the api is returning a warning message for
        # invalid tracking numbers in which case the isinstance may not work.
        # so we are double checking if package element exists before proceed
        # further, so that we can avoid unknown exceptions.
        is_package_available = True if 'package' in shipment else False
        if not is_package_available:
            return result
        for x in shipment['package']:
            activity += x.get('activity') or []
        activity.sort(key=lambda lx: lx['date'])
        origin_scans = self.filter_activity(activity, 'I', 'OR')
        deliveries = self.filter_activity(activity, 'D')
        delivery = []
        for x in shipment['package']:
            delivery += x.get('deliveryDate') or []
        delivery.sort(key=lambda lx: lx['date'])
        status = 'other'
        if deliveries and origin_scans:
            if len(deliveries) >= len(origin_scans):
                status = 'delivered'
            else:
                status = 'in_transit'
        elif origin_scans:
            status = 'in_transit'
        elif deliveries:
            status = 'delivered'
        else:
            status = 'not_shipped'
        rv = {
            'tracking_number': tracking_number,
            'created_at': activity[0]['date'],
            'updated_at': activity[-1]['date'],
            'ship_date': origin_scans[0]['date'] if origin_scans else None,
            'delivery_date': deliveries[-1]['date'] if deliveries else None,
            'estimated_delivery_date': delivery[0]['date'] if delivery else None,
            'status': status
        }
        return rv

    def raw_track(self, tracking_number, *args, **kwargs):
        """
        calls the ups restful tracking api and returns the output as-is from ups
        https://developer.ups.com/en-us/catalog/tracking/view-track-spec
        https://developer.ups.com/en-us/catalog/tracking/view-track-spec/trackv1detailsinquirynumber
        Args:
            tracking_number (str): the ups tracking number
            *args:
            **kwargs (Dict[Any, Any]): any keyword arguments you'd like to pass
                to the deceitful `get` call.
                `params` - any query parameters
                `raw` - boolean that indicates whether to return a
                  requests.Response or the parsed json back
        Returns: Union[requests.Response, Dict[str, Any]]

        """
        route = f'track/v1/details/{tracking_number}'
        return self.get(route, **kwargs)
