import requests


class UnifiAuthenticationException(Exception):
    pass


class Unifi:
    """Unifi voucher API wrapper"""

    def __init__(self, username, password, base_url, site='default', ignore_ssl=True, authenticate=True):
        """
        Initialize the Unifi API
        :param ignore_ssl: Ignore Unifi SSL certificate validity
        :param username: Unifi username
        :param password: Unifi password
        :param base_url: Unifi API base URL
        :param site: Site (defaults to the default site)
        :param authenticate: Authenticate after instantiating class
        """
        # Set class-level variables
        self.ignore_ssl = ignore_ssl
        self.username = username
        self.password = password
        self.base_url = base_url
        self.site = site
        self.session = requests.Session()

        if ignore_ssl:
            self.session.verify = False
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        # Authenticate
        if authenticate:
            self.authenticate()

    # Authenticate against the Unifi API
    def authenticate(self):
        """
        Authenticate against the Unifi API
        :return: authentication successful
        """
        self.session.headers.update({'referrer': "%s/login" % self.base_url})
        # Send credentials to API, check if successful
        if self.session.post("%s/api/login" % self.base_url,
                             json={'username': self.username, 'password': self.password}).json().get('meta').get(
            'rc') == 'ok':
            return True
        else:
            raise UnifiAuthenticationException

    # Generate a voucher
    def generate_voucher(self, expire=60, usages=1, note='API generated voucher'):
        """
        Generate a new voucher
        :param note: Note for voucher(s)
        :param expire: Expiry in minutes
        :param n: Amount of vouchers
        :return: API response in JSON
        """
        params = {'cmd': 'create-voucher', 'expire': 'custom', 'expire_number': expire, 'expire_unit': 1, 'n': 1,
                  'note': note, 'quota': usages}

        token = self.session.post("%s/api/s/%s/cmd/hotspot" % (self.base_url, self.site), json=params,
                                  verify=False).json()

        if token.get('meta').get('rc') == 'ok':
            # Successful, get token stats
            vouchers = []
            for n in token.get('data'):
                for v in self.token_stats(n.get('create_time')):
                    vouchers.append(v)
            return vouchers
        return None

    # Retrieve stats about a specific token
    def token_stats(self, create_time):
        """
        Retrieve token statistics
        :param create_time: Create time of the token
        :return: API response as JSON
        """
        stats = self.session.get("%s/api/s/%s/stat/voucher" % (self.base_url, self.site), verify=False).json()
        vouchers = []
        if stats.get('meta').get('rc') == 'ok':
            for voucher in stats.get('data'):
                if voucher.get('create_time') == create_time:
                    vouchers.append(voucher)
        return vouchers if vouchers else False

    # List available vouchers
    def list_vouchers(self):
        """
        Retrieve all vouchers
        :return: API response as JSON
        """
        return self.session.get("%s/api/s/%s/stat/voucher" % (self.base_url, self.site), verify=False).json()
