from requests import Session
from deceit.adapters import RetryAdapter
from deceit.api_client import ApiClient
from deceit.api_client import ApiException
from zeep.cache import Base as BaseCache
from zeep.client import Client
from zeep.plugins import HistoryPlugin
from zeep.proxy import OperationProxy
from zeep.proxy import ServiceProxy as ZeepServiceProxy
from zeep.settings import Settings
from zeep.transports import Transport


class SoapTransport(Transport):
    def __init__(self, session=None):
        # operation timeout specifies how long we are  willing to wait
        # for netsuite to get back to us
        # some operations can take a while, so we may need to adjust this.
        # the worst offenders are the custom list actions
        super().__init__(
            session=session,
            timeout=24 * 60 * 60,
            operation_timeout=600)


class PilotRestException(ApiException):
    pass

class PilotRestApi(ApiClient):
    def __init__(self,
                 conf=None, api_key=None, base_url=None,
                 exception_class=None, tariff_header_id=None,
                 location_id=None, **kwargs):
        base_url = base_url or 'https://www.pilotssl.com/pilotapi/v1/'
        exception_class = exception_class or PilotRestException
        super().__init__(
            base_url=base_url,
            exception_class=exception_class,
            **kwargs)
        if not api_key and conf:
            api_key = conf.api_key
        if not tariff_header_id and conf:
            tariff_header_id = conf.tariff_header_id
        if not location_id and conf:
            location_id = conf.location_id
        self.api_key = api_key
        self.tariff_header_id = tariff_header_id
        self.location_id = location_id

    def headers(self, *args, **kwargs):
        return {
            'content-type': 'application/json',
            'api-key': self.api_key,
            'accept': 'application/json'
        }

    def quote(self, location_id, tariff_header_id, from_zip, to_zip,
              lines, json=None):
        """
        lines is a list of dictionaries, where each of the dictionaries
        should be formatted as follows:
        {
          'Pieces': '',
          'Weight': '',
          'Description': '',
          'Length': '',
          'Width': '',
          'Height': '',
        }
        """
        d = json or {}
        rating = d.setdefault('Rating', {})
        rating.setdefault('TariffHeaderID', tariff_header_id)
        rating.setdefault('LocationID', location_id)
        shipper = rating.setdefault('Shipper', {})
        shipper.setdefault('Zipcode', from_zip)
        consignee = rating.setdefault('Consignee', {})
        consignee.setdefault('Zipcode', to_zip)
        rating.setdefault('LineItems', lines)
        return self.post('Ratings', json_data=d)


class PilotApi:
    def __init__(self, conf, user=None, password=None, **kwargs):
        self.username = user or conf.get('user')
        self.password = password or conf.get('password')
        zeep_settings = Settings(strict=False)
        self.base_url = f'https://www.pilotssl.com/pilotpartnertracking.asmx'
        self.wsdl_url = f'{self.base_url}?WSDL'
        self.session = Session()
        self.adapter = RetryAdapter(max_retries=5, timeout=300)
        self.session.mount('https://', self.adapter)
        self.transport = SoapTransport(session=self.session)

        # for debugging raw xml envelopes
        self._history = None
        self._enable_history = conf.get('history')
        plugins = None
        if self._enable_history:
            self._history = HistoryPlugin()
            plugins = [self._history, ]

        self.client = Client(
            self.wsdl_url, transport=self.transport,
            settings=zeep_settings, plugins=plugins)

    @property
    def factory(self):
        return self.client.type_factory('https://www.pilotssl.com')

    def validation(self):
        return self.factory.PilotTrackingRequestValidation(
            UserID=self.username,
            Password=self.password)

    @property
    def service(self):
        return self.client.service

    def hello(self):
        return self.service.HelloWorld()

    def raw_track(self, tracking_number):
        tr = self.factory.PilotTrackingRequest(
            Validation=self.validation(),
            APIVersion=1.0,
        )
        tr.TrackingNumber.append(tracking_number)
        return self.service.PilotAPITracking(tr=tr)

