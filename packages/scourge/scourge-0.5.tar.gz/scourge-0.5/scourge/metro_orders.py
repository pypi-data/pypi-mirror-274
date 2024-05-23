import time
from deceit.api_client import ApiClient
from deceit.exceptions import ApiException


class MetroApiException(ApiException):
    pass


class MetroApiOrders(ApiClient):
    def __init__(self, conf, *args, base_url=None, password=None, client_id=None,
                 username=None, default_timeout=None, **kwargs):
        base_url = base_url or conf.get('base_url')
        super().__init__(*args, base_url=base_url or conf.get('base_url'),
                         default_timeout=default_timeout or conf.get('default_timeout'),
                         exception_class=MetroApiException, **kwargs)
        self.username = username or conf.get('user')
        self.password = password or conf.get('password')
        self.client_id = client_id or conf.get('client_id')
        self.base_url = base_url
        self.token = None
        self.token_expiry = None

    def authenticate(self):
        if self.token and self.token_expiry and time.time() < self.token_expiry:
            return  # Token is still valid, no need to re-authenticate

        route = f'{self.base_url}/token'
        form_data = {
            'grant_type': 'password',
            'username': self.username,
            'password': self.password,
            'client_id': self.client_id
        }

        # Set headers directly for authentication to avoid recursion
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        # Use the session's post method directly for authentication to bypass
        # the custom headers logic
        response = self.session.post(route, data=form_data, headers=headers)
        self.log.info('response: %s', response.status_code)
        if response.status_code == 200:
            response_data = response.json()
            self.token = response_data['access_token']
            self.token_expiry = time.time() + response_data['expires_in']
        else:
            raise MetroApiException(f"Authentication failed: {response.text}")

    def headers(self, *args, **kwargs):
        self.authenticate()  # Ensure we have a valid token before proceeding
        return {
            'Authorization': f"Bearer {self.token}",
            'Content-Type': 'application/json; charset=utf-8'
        }

    def invoice_data(self, tracking_number, **kwargs):
        route = f'{ self.base_url }/GetOrderInvoiceData'
        json_data = {'trackingNumber': tracking_number}
        return self.post(route, json_data=json_data, **kwargs)
