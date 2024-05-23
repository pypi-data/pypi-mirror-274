import re
from urllib.parse import urlencode
from uuid import uuid4
from deceit.exceptions import ApiException
from deceit.api_client import BackendOauth2Client
from requests import Response


class FedexApiException(ApiException):
    pass


class FedexApi(BackendOauth2Client):
    def __init__(self, conf=None, *args, base_url=None, default_timeout=None,
                 exception_class=None, token_url=None,
                 client_id=None, password=None, scopes=None,
                 include_client_id=True, **kwargs):
        if not base_url and conf and not conf.get('base_url'):
            base_url = 'https://apis.fedex.com'
        if not token_url and conf and not conf.get('token_url'):
            token_url = f'{base_url}/oauth/token'
        super().__init__(
            conf, *args,
            base_url=base_url,
            default_timeout=default_timeout,
            exception_class=exception_class or FedexApiException,
            token_url=token_url,
            client_id=client_id, password=password, scopes=scopes,
            include_client_id=include_client_id, **kwargs)

    def headers(self, *args, transaction_id=None, **kwargs):
        return {
            'x-customer-transaction-id': uuid4().hex,
        }

    @classmethod
    def valid_tracking_number(cls, tracking_number):
        m = r'(96\d{20}|\d{15}|\d{12}' \
            r'|((98\d{4}\d?\d{4}|98\d\d) ?\d{4} ?\d{4}}( ?\d{3})?))'
        matcher = re.compile(m)
        return matcher.match(tracking_number)

    def track(self, tracking_number, **kwargs):
        """
        https://developer.fedex.com/api/en-us/guides/api-reference.html
        Args:
            tracking_number (str): the fedex tracking number
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
        invoice: List[str]
        po_number: List[str]
        customer_reference: List[str]
        ```
        """
        from .debug import yaml_to_str
        result = self.raw_track(tracking_number, **kwargs)
        if isinstance(result, Response):
            return result
        result = result['output']['completeTrackResults'][0]
        track_result = result['trackResults'][0]
        dates = {}
        created_at = '2200-01-01'
        updated_at = '1990-01-01'
        status_detail = track_result['latestStatusDetail']
        code = status_detail['code']
        status = 'in_transit'
        if code in ('DL',):
            status = 'delivered'
        elif code in ('DE', 'SE', 'RS', ):
            status = 'exception'
        elif code in ('CA',):
            status = 'canceled'
        elif code in ('OX', 'AP', 'EP', 'OC', 'PD'):
            status = 'not_shipped'
        ids = {}
        for x in track_result['additionalTrackingInfo']['packageIdentifiers']:
            key = x['type']
            values = x['values']
            ids[key] = values

        for x in track_result['dateAndTimes']:
            key = x['type']
            value = x['dateTime'].split('T', 1)[0]
            created_at = min(value, created_at)
            updated_at = max(value, updated_at)
            dt = dates.setdefault(key, value)
            if key == 'ACTUAL_DELIVERY':
                if dt < value:
                    dates[key] = value
            elif key == 'SHIP':
                if dt > value:
                    dates[key] = value
        rv = {
            'created_at': created_at,
            'updated_at': updated_at,
            'delivery_date': dates.get('ACTUAL_DELIVERY'),
            'ship_date': dates.get('SHIP'),
            'status': status,
            'po_number': ids['PURCHASE_ORDER'],
            'invoice': ids['INVOICE'],
            'customer_reference': ids['CUSTOMER_REFERENCE'],
        }
        return rv

    def raw_track(self, *args, include_detailed_scans=True, **kwargs):
        """
        calls the fedex restful tracking api and returns the output as-is from
        fedex

        Args:
            *args: one or more tracking numbers
            include_detailed_scans (bool):
            **kwargs (Dict[Any, Any]): any keyword arguments you'd like to pass
                to the deceitful `get` call.
                `params` - any query parameters
                `raw` - boolean that indicates whether to return a
                  requests.Response or the parsed json back
        Returns: Union[requests.Response, Dict[str, Any]]
        """
        json_data = kwargs.pop('json_data', None) or {}
        json_data.update({
            'includeDetailedScans': include_detailed_scans,
            'trackingInfo': [{
                'trackingNumberInfo': {
                    'trackingNumber': tracking_number,
                }
            } for tracking_number in args]
        })
        route = 'track/v1/trackingnumbers'
        return self.post(route, json_data=json_data, **kwargs)

    @classmethod
    def tracking_url(cls, tracking_number):
        base_url = 'https://www.fedex.com/fedextrack/'
        params = {
            'trknbr': tracking_number,
        }
        q = urlencode(params, doseq=True)
        return f'{base_url}?{q}'

