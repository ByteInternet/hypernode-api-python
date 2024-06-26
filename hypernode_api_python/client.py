from requests import Session

DEFAULT_USER_AGENT = "hypernode-api-python"
HYPERNODE_API_URL = "https://api.hypernode.com"
HYPERNODE_API_ADDON_LIST_ENDPOINT = "/v2/addon/"
HYPERNODE_API_ADDON_SLA_LIST_ENDPOINT = "/v2/addon/slas/"
HYPERNODE_API_APP_CHECK_PAYMENT_INFORMATION = "/v2/app/{}/check-payment-information/"
HYPERNODE_API_APP_CONFIGURATION_ENDPOINT = "/v2/configuration/"
HYPERNODE_API_APP_CLUSTER_RELATIONS = "/v2/app/{}/relations/"
HYPERNODE_API_APP_DETAIL_ENDPOINT = "/v2/app/{}/?destroyed=false"
HYPERNODE_API_APP_DETAIL_WITH_ADDONS_ENDPOINT = "/v2/app/{}/with_addons?destroyed=false"
HYPERNODE_API_APP_EAV_DESCRIPTION_ENDPOINT = "/v2/app/eav_descriptions/"
HYPERNODE_API_APP_FLAVOR_ENDPOINT = "/v2/app/{}/flavor/"
HYPERNODE_API_APP_FLOWS_ENDPOINT = "/logbook/v1/logbooks/{}/flows"
HYPERNODE_API_APP_NEXT_BEST_PLAN_ENDPOINT = "/v2/app/{}/next_best_plan/"
HYPERNODE_API_APP_ORDER_ENDPOINT = "/v2/app/order/"
HYPERNODE_API_APP_PRODUCT_LIST_ENDPOINT = "/v2/product/app/{}/"
HYPERNODE_API_APP_XGRADE_CHECK_ENDPOINT = "/v2/app/xgrade/{}/check/{}/"
HYPERNODE_API_APP_XGRADE_ENDPOINT = "/v2/app/xgrade/{}/"
HYPERNODE_API_BACKUPS_ENDPOINT = "/v2/app/{}/backup/"
HYPERNODE_API_BLOCK_ATTACK_ENDPOINT = "/v2/app/{}/block_attack/"
HYPERNODE_API_BLOCK_ATTACK_DESCRIPTION_ENDPOINT = "/v2/app/block_attack_descriptions/"
HYPERNODE_API_BRANCHER_APP_ENDPOINT = "/v2/brancher/app/{}/"
HYPERNODE_API_FPM_STATUS_APP_ENDPOINT = "/v2/nats/{}/hypernode.show-fpm-status"
HYPERNODE_API_BRANCHER_ENDPOINT = "/v2/brancher/{}/"
HYPERNODE_API_PRODUCT_APP_DETAIL_ENDPOINT = "/v2/product/app/{}/current/"
HYPERNODE_API_PRODUCT_LIST_ENDPOINT = "/v2/product/"
HYPERNODE_API_PRODUCT_PRICE_DETAIL_ENDPOINT = "/v2/product/{}/with_price/"
HYPERNODE_API_VALIDATE_APP_NAME_ENDPOINT = "/v2/app/name/validate/"
HYPERNODE_API_WHITELIST_ENDPOINT = "/v2/whitelist/{}/"


class HypernodeAPIPython:
    def __init__(self, token, api_url=None, user_agent=None):
        """
        The official Hypernode API client for Python

        :param str token: The API token you're using to talk to the API
        Check out /etc/hypernode/hypernode_api_token on the Hypernode to
        find your token.
        :param str api_url: The URL of the API. Leave None if you wish
        to use the 'real' Hypernode API. For local development you might
        want to override this (if you want to talk to a different API, or
        no real API at all).
        :param str user_agent: The user agent to use when doing the API
        requests. If you leave this None it will default to DEFAULT_USER_AGENT,
        but you may want to enter the name of your application here.
        """
        self.session = Session()
        self.token = token
        self.api_url = api_url if api_url else HYPERNODE_API_URL
        self.authorization_header = "Token {}".format(self.token)
        self.user_agent = user_agent if user_agent else DEFAULT_USER_AGENT

    def requests(self, method, path, *args, **kwargs):
        """
        Some default requests settings. You can override this entire
        method if you wish to set some different defaults.
        """
        kwargs.setdefault("headers", {}).update(
            {
                "Accept": "application/json",
                "Authorization": self.authorization_header,
                "Accept-Language": "en-US",
                "User-Agent": self.user_agent,
            }
        )
        return self.session.request(
            method, HYPERNODE_API_URL.rstrip("/") + path, *args, **kwargs
        )

    def _get_app_endpoint_or_404(self, app_name, endpoint, error_to_raise=None):
        """
        Get the app endpoint and return the response, but if the status_code is
        404 then raise the specified exception. Raises RuntimeError by default
        but if you're using this in for example a Django application you might
        want to raise a django.http.response.Http404 instead.

        :param str app_name: The name of the app to get the endpoint of
        :param str endpoint: The endpoint to get
        :param obj error_to_raise: What error to raise if the name is not
        valid or available. By default, this will be RuntimeError.
        :return obj response: The request response object
        """
        error_to_raise = error_to_raise if error_to_raise else RuntimeError
        response = self.requests("GET", endpoint.format(app_name))

        if response.status_code == 404:
            raise error_to_raise("App {} not found.".format(app_name))
        return response

    def get_app_info_or_404(self, app_name):
        """
        Get information about the specified app. Raises if the status returns 404.
        Example:
        >    client.get_app_info_or_404('yourhypernodeappname').json()
        >    {
        >        'account_user':
        >            {
        >                'email': 'email@example.com',
        >                'first_name': 'Firstname',
        >                'id': 0,
        >                'last_name': 'Lastname',
        >                'username': 'email@example.com'
        >            },
        >        'destroyed': False,
        >        'domainname': 'yourhypernodeappname.hypernode.io',
        >        'flavor': {'name': '2CPU/8GB/60GB (Falcon S 202202)', 'redis_size': '1024'},
        >        'in_production': True,
        >        'ip': '1.2.3.4',
        >        'mysql_version': '8.0',
        >        'name': 'yourhypernodeappname',
        >        'type': 'persistent',
        >        ...
        >    }

        :param str app_name: The name of the app to get information about
        :return obj response: The request response object
        """
        return self._get_app_endpoint_or_404(
            app_name, HYPERNODE_API_APP_DETAIL_ENDPOINT
        )

    def get_next_best_plan_for_app_or_404(self, app_name):
        """
        Ask the API for what the next plan would be for this app
        if it was looking to upgrade. In case you want to implement
        some sort of auto-scaling you need a way to query the API for
        the product code (and product name) of the plan next in line.
        For example, if you are on the Falcon S, doing this API call
        would return you information about the Falcon M. If the information
        for the specified app_name can not be queried due to a 404, this
        method will raise.
        Example:
        >    client.get_next_best_plan_for_app_or_404('yourhypernodeappname').json()
        >    {'name': 'Falcon M', 'code': 'FALCON_M_202203'}

        :param str app_name: The name of the app to get the next best plan for
        :return obj response: The request response object
        """
        return self._get_app_endpoint_or_404(
            app_name, HYPERNODE_API_APP_NEXT_BEST_PLAN_ENDPOINT
        )

    def validate_app_name(self, app_name, error_to_raise=None):
        """
        Check if an app name is valid and available. Before you create
        a new Hypernode you could check if the name is available.

        :param str app_name: The name of the app to check for availability
        :param obj error_to_raise: What error to raise if the name is not
        valid or available. By default, this will be RuntimeError.
        :return NoneType None: If it's valid, we don't raise, but we don't
        return anything either.
        """
        error_to_raise = error_to_raise if error_to_raise else RuntimeError
        response = self.requests(
            "GET", HYPERNODE_API_VALIDATE_APP_NAME_ENDPOINT, params={"name": app_name}
        )
        if response.content and response.content.decode() != "[]":
            data = response.json()
            if isinstance(data, dict):
                raise error_to_raise(data["errors"])
            raise error_to_raise(data)

    def get_app_flavor(self, app_name):
        """
        Get the flavor of an app
        Example:
        >    client.get_app_flavor('yourhypernodeappname').json()
        >    {'name': '2CPU/8GB/60GB (Falcon S 202202)', 'redis_size': '1024'}

        :param str app_name: The name of the app to get the flavor for
        :return obj response: The request response object
        """
        return self.requests("GET", HYPERNODE_API_APP_FLAVOR_ENDPOINT.format(app_name))

    def get_flows(self, app_name):
        """
        List the flows for an app. Take note that this result is paginated and will not
        retrieve all flows. If you are looking to retrieve all flows and not those available
        on just the first page, look at the get_all_flows method instead.

        Example:
        >    client.get_flows('yourhypernodeappname').json()
        >    {'count': 2,
        >     'next': None,
        >     'previous': None,
        >     'results': [{'uuid': '1d1b8437-c8c0-4e96-a28a-26cc311c1f4c',
        >       'state': 'success',
        >       'name': 'update_node',
        >       'created_at': '2023-03-04T14:42:24Z',
        >       'updated_at': '2023-03-04T14:42:57Z',
        >       'progress': {'running': [], 'total': 8, 'completed': 8},
        >       'logbook': 'yourhypernodeappname',
        >       'tracker': {'uuid': '6012bf2c-952d-4cb0-97ff-1022614b50b7',
        >        'description': None}},
        >      {'uuid': 'fe696417-024e-4a57-8442-4967f6df24a3',
        >       'state': 'success',
        >       'name': 'create_backup',
        >       'created_at': '2023-03-04T14:13:00Z',
        >       'updated_at': '2023-03-04T14:13:12Z',
        >       'progress': {'running': [], 'total': 2, 'completed': 2},
        >       'logbook': 'yourhypernodeappname',
        >       'tracker': {'uuid': None, 'description': None}}]
        >    }


        :param str app_name: The name of the app to get the flows for
        :return obj response: The request response object
        """
        return self.requests("GET", HYPERNODE_API_APP_FLOWS_ENDPOINT.format(app_name))

    def get_all_flows(self, app_name, limit=None):
        """
        List all the flows for an app (paginate over the results), or
        retrieve results until we have enough (if limit is specified).
        Note that this method does not return a response object but a
        list of dicts instead.
        Example:
        >    client.get_all_flows('yourhypernodeappname')
        >    [{'uuid': '03bd6e10-5493-4ee8-92fc-cc429faebead',
        >      'state': None,
        >      'name': 'update_node',
        >      'created_at': '2023-03-05T14:01:56Z',
        >      'updated_at': None,
        >      'progress': {'running': [], 'total': 0, 'completed': 0},
        >      'logbook': 'yourhypernodeappname',
        >      'tracker': {'uuid': '0dd83d83-6b9b-4fb5-9665-79fcf8235069',
        >       'description': None}},
        >     {'uuid': 'ace36ab9-323e-4a95-a0c6-46f96945b623',
        >      'state': None,
        >      'name': 'update_node',
        >      'created_at': '2023-03-05T14:01:55Z',
        >      'updated_at': None,
        >      'progress': {'running': [], 'total': 0, 'completed': 0},
        >      'logbook': 'yourhypernodeappname',
        >      'tracker': {'uuid': '0006206e-df48-4af4-8e7b-b3db86d35bb0',
        >       'description': None}},
        >     ...
        >    ]

        :param str app_name: The name of the app to get all the flows for
        :param int limit: How many flows to get. If None is specified all
        available flows will be retrieved.
        :return list flows: A list of all flows
        """
        flows = []
        next_url = HYPERNODE_API_APP_FLOWS_ENDPOINT.format(app_name)
        while next_url:
            if limit and len(flows) >= limit:
                break
            response = self.requests("GET", next_url.replace(HYPERNODE_API_URL, ""))
            response_data = response.json()
            results = response_data["results"]
            flows.extend(results)
            next_url = response_data["next"]
        return flows[:limit]

    def get_slas(self):
        """
        List the available SLAs
        Example:
        >    client.get_slas().json()
        >    [{'billing_period': 1,
        >    'billing_period_unit': 'month',
        >    'code': 'sla-standard',
        >    'id': 123,
        >    'name': 'SLA Standard',
        >    'price': 1234},
        >    ..]

        :return obj response: The request response object
        """
        return self.requests("GET", HYPERNODE_API_ADDON_SLA_LIST_ENDPOINT)

    def get_sla(self, sla_code):
        """
        List a specific SLA
        Example:
        >    client.get_sla("sla-standard").json()
        >    {'billing_period': 1,
        >     'billing_period_unit': 'month',
        >     'code': 'sla-standard',
        >     'id': 123,
        >     'name': 'SLA Standard',
        >     'price': 1234}

        :return obj response: The request response object
        """
        return self.requests("GET", HYPERNODE_API_ADDON_LIST_ENDPOINT + sla_code + "/")

    def get_available_backups_for_app(self, app_name):
        """
        Lists the available backups for the specified app
        Example:
        >    client.get_available_backups_for_app('yourhypernodeappname').json()
        >    {
        >        'count': 11,
        >        'next': None,
        >        'previous': None,
        >        'results': [
        >            {
        >                'backup_created_at': '2022-09-30T13:26:01+02:00',
        >                'backup_id': '12341234-1234-1234-1234-123412341234',
        >                'expired_at': '2022-10-28T13:26:01+02:00',
        >                'type': 'periodic'
        >            },
        >            ...
        >        ]
        >    }

        :param str app_name: The app to look up the available backups for
        :return obj response: The request response object
        """
        return self.requests("GET", HYPERNODE_API_BACKUPS_ENDPOINT.format(app_name))

    def get_app_eav_description(self):
        """
        List all the available EAV settings that are available. These are
        the same settings as you'd be able to configure using the command-line
        tool on the Hypernode itself (hypernode-systemctl settings).
        Example:
        >    client.get_app_eav_description().json()
        >    {
        >        'varnish_enabled': [True, False],
        >        'php_version': ['8.0', '8.1'],
        >        ...
        >    }

        :return obj response: The request response object
        """
        return self.requests("GET", HYPERNODE_API_APP_EAV_DESCRIPTION_ENDPOINT)

    # TODO: add entrypoint for this method in bin/ and commands.py
    def set_app_setting(self, app_name, attribute, value):
        """
        Update a setting on the app, like the PHP or MySQL version. See
        get_app_eav_description for all possible values. This is similar
        to hypernode-systemctl settings.
        Example:
        >    client.get_app_eav_description().json()
        >    {
        >        'varnish_enabled': [True, False],
        >        'php_version': ['8.0', '8.1'],
        >        ...
        >    }

        :param str app_name: The app to configure the setting for
        :param str attribute: The setting to configure, like 'php_version'
        :param str || bool value: The value to set it to, like '8.1'
        :return obj response: The request response object
        """
        data = {attribute: value}
        return self.requests(
            "PATCH", HYPERNODE_API_APP_DETAIL_ENDPOINT.format(app_name), data=data
        )

    def get_app_configurations(self):
        """
        List all the available app configurations. These are the available
        configurations you can select when ordering a new Hypernode. For example
        if you'd use the Magento 2 app configuration you'd get a certain PHP version
        and specific Magento 2 NGINX configurations.
        Example:
        >    client.get_app_configurations().json()
        >    {
        >        'count': 2,
        >        'next': None,
        >        'previous': None,
        >        'results': [
        >            {
        >                'allow_preinstall': True,
        >                'composer_version': '2.x',
        >                'name': 'Akeneo 4.0',
        >                'elasticsearch_enabled': True,
        >                'elasticsearch_version': '7.x',
        >                ...
        >            },
        >            ...
        >        ]
        >    }

        :return obj response: The request response object
        """
        return self.requests("GET", HYPERNODE_API_APP_CONFIGURATION_ENDPOINT)

    def get_cluster_relations(self, app_name):
        """
        List all relations for the specified app. This will return all the
        relations that are currently configured for the specified app.

        Example:
        >    client.get_cluster_relations('mytestappweb').json()
        >    {'children': [],
        >     'parents': [{'child': 'mytestappweb',
        >                  'cluster_description': None,
        >                  'id': 182,
        >                  'parent': 'mytestappdb',
        >                  'relation_type': 'mysql'},
        >                 {'child': 'mytestappweb',
        >                  'cluster_description': None,
        >                  'id': 180,
        >                  'parent': 'mytestapp',
        >                  'relation_type': 'loadbalancer'},
        >                 {'child': 'mytestappweb',
        >                  'cluster_description': None,
        >                  'id': 181,
        >                  'parent': 'mytestapp',
        >                  'relation_type': 'nfs'}]}
        """
        return self.requests(
            "GET", HYPERNODE_API_APP_CLUSTER_RELATIONS.format(app_name)
        )

    def get_product_info_with_price(self, product_code, error_to_raise=None):
        """
        Get information about a specific product
        :param str product_code: The code of the product to get information of
        :param obj error_to_raise: What error to raise if the product does not
        exist. By default this will be RuntimeError.
        Example:
        >    client.get_product_info_with_price('MAGG201909').json()
        >    {
        >        'backups_enabled': True,
        >        'code': 'FALCON_S_202203',
        >        'is_development': False,
        >        'name': 'Grow',
        >        'price': 1234,
        >        'provider': 'combell',
        >        'related_product': {
        >            'backups_enabled': True,
        >            'code': 'FALCON_S_202203DEV',
        >            'is_development': True,
        >            'name': 'Grow Development',
        >            'price': 4321,
        >            'provider': 'combell',
        >            'storage_size_in_gb': 44,
        >            'supports_sla': False,
        >            'varnish_supported': False
        >        },
        >        'storage_size_in_gb': 44,
        >        'supports_sla': True,
        >        'varnish_supported': False
        >    }

        :return obj response: The request response object
        """
        error_to_raise = error_to_raise if error_to_raise else RuntimeError
        response = self.requests(
            "GET", HYPERNODE_API_PRODUCT_PRICE_DETAIL_ENDPOINT.format(product_code)
        )
        if response.status_code == 404:
            raise error_to_raise
        return response

    def get_block_attack_descriptions(self):
        """
        Get the block attack descriptions. These can be used to block attacks
        by automatically placing an NGINX snippet in /data/web/nginx if the
        specified block is compatible with the current NGINX configuration.
        Example:
        >    client.get_block_attack_descriptions().json()
        >    {
        >        'BlockSqliBruteForce': 'Attempts to deploy NGINX rules to block suspected (blind) SQL injection attack',
        >        ...
        >    }

        :return obj response: The request response object
        """
        return self.requests("GET", HYPERNODE_API_BLOCK_ATTACK_DESCRIPTION_ENDPOINT)

    def block_attack(self, app_name, attack_name):
        """
        Attempts to deploy one of the block attack rules. The list of rules can be retrieved with the
        get_block_attack_descriptions method. This will place an NGINX snippet to block the specified attack
        in /data/web/nginx. If the nginx-config-validator detects that the new config is valid, it will leave
        the newly placed config. Otherwise it will be removed again.

        Example:
        >    client.block_attack('yourhypernodeappname', 'BlockSqliBruteForce').ok
        >    True

        :param str app_name: The name of the Hypernode you want to deploy the block attack nginx configuration on
        :param str attack_name: The specific attack you want to block. See get_block_attack_descriptions for options.
        :return obj response: The request response object
        """
        return self.requests(
            "POST",
            HYPERNODE_API_BLOCK_ATTACK_ENDPOINT.format(app_name),
            data={"attack_name": attack_name},
        )

    def get_whitelist_options(self, app_name):
        """
        Get whitelist options for app. Retrieve the options for specifying
        whitelist information for this Hypernode. See hypernode-systemctl
        for an implementation example of how this can be used to configure
        the firewall using the Hypernode API.
        Example:
        >    client.get_whitelist_options('yourhypernodeappname').json())
        >    {'actions':
        >        {'POST':
        >            {'description':
        >                {
        >                    'label': 'Description',
        >                    'read_only': False,
        >                    'required': False,
        >                    'type': 'string'
        >                },
        >                'ip': {
        >                    'label': 'Ip',
        >                    'read_only': False,
        >                    'required': True,
        >                    'type': 'string'
        >                },
        >                'type': {
        >                    'choices': [
        >                        {
        >                            'display_name': 'waf',
        >                            'value': 'waf'
        >                        },
        >                        {
        >                            'display_name': 'database',
        >                            'value': 'database'
        >                        },
        >                        {
        >                            'display_name': 'ftp',
        >                            'value': 'ftp'
        >                        }
        >                    ],
        >                    'label': 'Type',
        >                    'read_only': False,
        >                    'required': True,
        >                    'type': 'choice'
        >                }
        >            }
        >        },
        >        'description': '',
        >        'name': 'Whitelist',
        >        'parses': [
        >            'application/json',
        >            'application/x-www-form-urlencoded',
        >            'multipart/form-data'
        >        ],
        >        'renders': ['application/json']
        >    }

        :param str app_name: The name of the app to get the whitelist information for
        :return obj response: The request response object
        """
        return self.requests(
            "OPTIONS", HYPERNODE_API_WHITELIST_ENDPOINT.format(app_name)
        )

    def get_whitelist_rules(self, app_name, filter_data=None):
        """
        Get the whitelist rules currently configured for the specified app
        Example:
        >    client.get_whitelist_rules('yourhypernodeappname').json())
        >    [
        >        {
        >            'created': '2022-10-23T14:49:06Z',
        >            'description': '',
        >            'domainname': 'yourhypernodeappname.hypernode.io',
        >            'id': 1234,
        >            'ip': '1.2.3.4',
        >            'type': 'waf'
        >        },
        >        ...
        >    ]

        :param str app_name: The name of the Hypernode you want to get the
        currently configured whitelist information for.
        :param dict filter_data: Filter the results based on this filter
        An example filter to specify could be: {'type': 'waf'}
        :return obj response: The request response object
        """
        filter_data = filter_data or {}
        return self.requests(
            "GET", HYPERNODE_API_WHITELIST_ENDPOINT.format(app_name), filter_data
        )

    def get_current_product_for_app(self, app_name):
        """
        Retrieve information about the product the specified App is currently on.
        Example:
        >    client.get_current_product_for_app('yourhypernodeappname').json()
        >    {
        >        'backups_enabled': True,
        >        'code': 'FALCON_S_202203',
        >        'flavor': {
        >            'name': '2CPU/8GB/60GB (Falcon S 202202)', 'redis_size': '1024'
        >        },
        >        'is_active': True,
        >        'is_development': False,
        >        'name': 'Falcon S',
        >        'price': 1234,
        >        'provider_flavors': [
        >            {
        >                'disk_size_in_gb': 1234,
        >                'exact_disk_size_in_kb': 1234,
        >                'inodes': 1234,
        >                'provider': {
        >                    'display_name': 'Combell OpenStack',
        >                    'name': 'combell'
        >                },
        >                'ram_in_mb': 8192,
        >                'vcpus': 2
        >            }
        >        ],
        >        'related_product': {
        >            'backups_enabled': True,
        >            'code': 'FALCON_S_202203DEV',
        >            'flavor': {
        >                'name': '2CPU/8GB/60GB (Falcon S 202202)',
        >                'redis_size': '1024'
        >            },
        >            'is_active': True,
        >            'is_development': True,
        >            'name': 'Falcon S Development',
        >            'price': 1234,
        >            'provider_flavors': [
        >                {
        >                    'disk_size_in_gb': 1234,
        >                    'exact_disk_size_in_kb': 1234,
        >                    'inodes': 1234,
        >                    'provider': {
        >                        'display_name': 'Combell '
        >                                        'OpenStack',
        >                        'name': 'combell'
        >                    },
        >                    'ram_in_mb': 8192,
        >                    'vcpus': 2
        >                }
        >            ],
        >            'supports_sla': False,
        >            'varnish_supported': True
        >        },
        >        'supports_sla': True,
        >        'varnish_supported': True
        >    }

        :param str app_name: The name of the Hypernode to retrieve the product
        information for.
        :return obj response: The request response object
        """
        return self.requests(
            "GET", HYPERNODE_API_PRODUCT_APP_DETAIL_ENDPOINT.format(app_name)
        )

    def check_payment_information_for_app(self, app_name):
        """
        Get the payment information that is currently configured for this Hypernode
        Example:
        >    client.check_payment_information_for_app('yourhypernodeappname').json()
        >    {
        >        'has_valid_vat_number': True,
        >        'has_valid_payment_method': True,
        >    }

        :param str app_name: The Hypernode to check the payment information for
        :return obj response: The request response object
        """
        return self.requests(
            "GET", HYPERNODE_API_APP_CHECK_PAYMENT_INFORMATION.format(app_name)
        )

    def get_active_products(self):
        """
        Retrieve the list of products that are currently available. You can
        change the plan of your Hypernode to these products. Doing so would
        start a migration and change your subscription to the specified plan.
        Example:
        >    client.get_active_products().json()
        >    [
        >        {'backups_enabled': True,
        >         'code': 'FALCON_XS_202203',
        >         'flavor': {
        >             'name': '2CPU/4GB/60GB (Falcon XS 202202)', 'redis_size': '768'
        >         },
        >         'is_active': True,
        >         'is_development': False,
        >         'name': 'Falcon XS',
        >         'price': 1234,
        >         'provider_flavors': [
        >             {'disk_size_in_gb': 1234,
        >              'exact_disk_size_in_kb': 1234,
        >              'inodes': 1234,
        >              'provider': {
        >                  'display_name': 'Combell OpenStack',
        >                  'name': 'combell'
        >              },
        >              'ram_in_mb': 4096,
        >              'vcpus': 2
        >              }
        >         ],
        >         'related_product': {
        >             'backups_enabled': True,
        >             'code': 'FALCON_XS_202203DEV',
        >             'flavor': {
        >                 'name': '2CPU/4GB/60GB (Falcon XS 202202)',
        >                 'redis_size': '768'
        >             },
        >             'is_active': True,
        >             'is_development': True,
        >             'name': 'Falcon XS Development',
        >             'price': 1234,
        >             'provider_flavors': [
        >                 {
        >                     'disk_size_in_gb': 1234,
        >                     'exact_disk_size_in_kb': 1234,
        >                     'inodes': 1234,
        >                     'provider': {
        >                         'display_name': 'Combell '
        >                                         'OpenStack',
        >                         'name': 'combell'
        >                     },
        >                     'ram_in_mb': 4096,
        >                     'vcpus': 2
        >                 }
        >             ],
        >             'supports_sla': False,
        >             'varnish_supported': False
        >         },
        >         'supports_sla': True,
        >         'varnish_supported': False
        >         },
        >        ...
        >    ]

        :return obj response: The request response object
        """
        return self.requests("GET", HYPERNODE_API_PRODUCT_LIST_ENDPOINT)

    def check_xgrade(self, app_name, product_code):
        """
        Checks if the Hypernode 'is going to fit' on the new product. Retrieves some
        information about what a plan change to the specified product would look like for
        the specified app. If it does not fit because the disk space currently in use is too
        high, then we can find out here. Also, whether the IP will change, or if the volume
        would entail a rsync migration or a more sophisticated volume swap cloud action which
        would mean a significantly shorter migration time (depending on how much space is used).
        Example:
        >    client.check_xgrade('yourhypernodeappname', 'FALCON_S_202203').json()
        >    {
        >        'has_valid_vat_number': True,
        >        'has_valid_payment_method': True,
        >        'will_change_ip': False,
        >        'will_do_volswap': True,
        >        'will_disk_fit': True
        >    }

        :param str app_name: The name of the Hypernode to check the xgrade for
        :param str product_code: The destination product we're checking. So if we'd xgrade
        to this product, what would that mean? The response will tell us.
        :return obj response: The request response object
        """
        return self.requests(
            "GET",
            HYPERNODE_API_APP_XGRADE_CHECK_ENDPOINT.format(app_name, product_code),
        )

    def xgrade(self, app_name, data):
        """
        Change the product of a Hypernode to a different plan. This will initiate
        a migration of the Hypernode to a larger or smaller Hypernode, depending on
        what product you specify. Progress of the migration can be tracked on the
        hypernode by running hypernode-log (or getting that information from the API
        directly as well). This API call does not result any output, on success the
        response.text will be an empty string and the status_code will be 200.

        :param str app_name: The name of the Hypernode to change the product of
        :param dict data: Data regarding what product the Hypernode should be changed
        to. An example could be: {'product': 'FALCON_S_202203'}. You can also specify a
        scheduled_at time in case you want to perform the migration at a scheduled
        moment. That could look something like this:
        {'product': 'FALCON_S_202203', 'scheduled_at': '2022-11-25T01:00:00+03:00'}
        :return obj response: The request response object
        """
        return self.requests(
            "PATCH", HYPERNODE_API_APP_XGRADE_ENDPOINT.format(app_name), data=data
        )

    # TODO: add entrypoint for this method in bin/ and commands.py
    def order_hypernode(self, data):
        """
        Orders a new Hypernode. Note that you can not do this with the API permissions
        of the API token of a Hypernode. If you wish to programmatically order Hypernodes
        please contact support@hypernode.com, and we'll set up an API token with appropriate
        permissions for you. Also, if this is something you're actively working on, we'd love
        to hear about your use-case.

        :param dict data: Data regarding the Hypernode that should be newly created
        This should be something like:
        {
            'app_name': 'mynewhypernodeappnameofmax16chars',
            'product': 'FALCON_S_202203',
            'initial_app_configuration': 'magento_2',
        }
        :return obj response: The request response object
        """
        return self.requests("POST", HYPERNODE_API_APP_ORDER_ENDPOINT, data=data)

    def get_active_branchers(self, app_name):
        """
        List all active brancher nodes of your Hypernode.
        Example:
        >    client.get_active_branchers("yourhypernodeappname").json()
        >    {
        >        "monthly_total_time": 6397,
        >        "monthly_total_cost": 109,
        >        "branchers": [
        >            {
        >                "id": 21,
        >                "name": "yourhypernodeappname-eph123456",
        >                "cost": 131,
        >                "created": "2019-08-24T14:15:22Z"
        >                "ip": "127.0.0.1",
        >                "end_time": None,
        >                "elapsed_time": 7824,
        >                "labels": {"description": "php upgrade test", "label without equal sign": None},
        >            },
        >            {
        >                "id": 22,
        >                "name": "yourhypernodeappname-eph654321",
        >                "cost": 121,
        >                "ip": "52.68.96.58",
        >                "created": "2019-08-24T14:15:22Z"
        >                "end_time": None,
        >                "elapsed_time": 7224,
        >                "labels": {},
        >            }
        >        ]
        >    }

        :param str app_name: The name of the Hypernode to get your active branchers for
        :return obj response: The request response object
        """
        return self.requests(
            "GET", HYPERNODE_API_BRANCHER_APP_ENDPOINT.format(app_name)
        )

    def get_fpm_status(self, app_name):
        """
        Get the status of the FPM service for the specified app
        Example:
        >    client.get_fpm_status("yourhypernodeappname").json()
        {
          "message": null,
          "data": "50570 IDLE   0.0s -  phpfpm    127.0.0.1       GET  magweb/status.php   (python-requests/2.28.1)\n50571 IDLE   0.0s -  phpfpm    127.0.0.1       GET  magweb/status.php   (python-requests/2.28.1)\n",
          "status": 200
        }

        :param str app_name: The name of the Hypernode to get the FPM status for
        :return obj response: The request response object
        """
        return self.requests(
            "POST", HYPERNODE_API_FPM_STATUS_APP_ENDPOINT.format(app_name)
        )

    def create_brancher(self, app_name, data):
        """
        Create a new branch (server replica) of your Hypernode.

        :param str app_name: The name of the Hypernode to create the branch from
        :param dict data: Data regarding the branch to be created. An example could be:
        {'clear_services': ['mysql', 'cron']}.
        :return obj response: The request response object
        """
        return self.requests(
            "POST", HYPERNODE_API_BRANCHER_APP_ENDPOINT.format(app_name), data=data
        )

    def destroy_brancher(self, brancher_name):
        """
        Destroy an existing brancher node of your Hypernode.

        :param str brancher_name: The name of the brancher node to destroy.
        :return obj response: The request response object
        """
        return self.requests(
            "DELETE", HYPERNODE_API_BRANCHER_ENDPOINT.format(brancher_name)
        )
