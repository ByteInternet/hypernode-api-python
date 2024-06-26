import json
from os import environ, EX_OK, EX_UNAVAILABLE
from argparse import ArgumentParser, RawTextHelpFormatter
from hypernode_api_python.client import HypernodeAPIPython


def get_client():
    """
    Instantiates the HypernodeAPIPython client with the token from the environment.
    :return obj HypernodeAPIPython: The instantiated client
    """
    api_token = environ.get("HYPERNODE_API_TOKEN")
    if not api_token:
        raise ValueError(
            "HYPERNODE_API_TOKEN environment variable not set. "
            "Try running `export HYPERNODE_API_TOKEN=yourapitoken`"
        )
    client = HypernodeAPIPython(environ["HYPERNODE_API_TOKEN"])
    return client


def get_app_name():
    """
    Gets the app name from the environment.
    :return str app_name: The app name
    """
    app_name = environ.get("HYPERNODE_APP_NAME")
    if not app_name:
        raise ValueError(
            "HYPERNODE_APP_NAME environment variable not set. "
            "Try running `export HYPERNODE_APP_NAME=yourhypernodeappname`"
        )
    return app_name


def print_response(response):
    """
    Pretty prints the JSON response.
    :param obj response: The response object
    :return NoneType None: None
    """
    print(json.dumps(response.json(), indent=2))


def get_app_info(args=None):
    parser = ArgumentParser(
        description="""
Get information about the Hypernode app.

Example:
$ ./bin/get_app_info
{
  "name": "yourhypernodeappname",
  "type": "persistent",
  "product": {
    "code": "FALCON_M_202203",
    "name": "Falcon M",
    "backups_enabled": true,
    "storage_size_in_gb": 75,
    "price": 1234,
    "is_development": false,
    "provider": "combell",
    "varnish_supported": true,
    "supports_sla": true
  },
  "domainname": "yourhypernodeappname.hypernode.io",
  ...
}
""",
        formatter_class=RawTextHelpFormatter,
    )
    parser.parse_args(args=args)
    client = get_client()
    app_name = get_app_name()
    print_response(client.get_app_info_or_404(app_name))


def get_next_best_plan_for_app(args=None):
    parser = ArgumentParser(
        description="""
Get the plan that is the first bigger plan than the current plan for this Hypernode.
This is convenient for if you want to upgrade your Hypernode to a bigger plan using the
xgrade feature and you need to know which plan to upgrade to.

Example:
$ ./bin/get_next_best_plan_for_app
{
  "code": "FALCON_L_202203",
  "name": "Falcon L"
}
""",
        formatter_class=RawTextHelpFormatter,
    )
    parser.parse_args(args=args)
    client = get_client()
    app_name = get_app_name()
    print_response(client.get_next_best_plan_for_app_or_404(app_name))


def validate_app_name(args=None):
    parser = ArgumentParser(
        description="""
Check if the specified app_name is valid and available. An app name can not be
registered if it's already taken. Also there are certain restrictions on the
app name, like it can't contain certain characters or exceed a certain length.

Examples:
$ ./bin/validate_app_name hypernode
App name 'hypernode' is valid.

$ ./bin/validate_app_name hyper_node
App name 'hyper_node' is invalid: ["This value can only contain non-capital letters 'a' through 'z' or digits 0 through 9."]
""",
        formatter_class=RawTextHelpFormatter,
    )
    parser.add_argument(
        "app_name",
        help="The app name to validate",
    )
    args = parser.parse_args(args=args)
    client = get_client()
    try:
        client.validate_app_name(args.app_name)
        print("App name '{}' is valid.".format(args.app_name))
        exit(EX_OK)
    except Exception as e:
        print("App name '{}' is invalid: {}".format(args.app_name, e))
        exit(EX_UNAVAILABLE)


def get_app_flavor(args=None):
    parser = ArgumentParser(
        description="""
Get the current flavor of the Hypernode app.

Example:
$ ./bin/get_app_flavor
{
  "name": "3CPU/16GB/80GB (Falcon M 202202)",
  "redis_size": "2048"
}
""",
        formatter_class=RawTextHelpFormatter,
    )
    parser.parse_args(args=args)
    client = get_client()
    app_name = get_app_name()
    print_response(client.get_app_flavor(app_name))


def get_flows(args=None):
    parser = ArgumentParser(
        description="""
Llist the flows for the Hypernode app. This is a history of all the
Hypernode automation jobs that have been ran for this Hypernode.

Example:
$ ./bin/get_flows
{
  "count": 36,
  "next": null,
  "previous": null,
  "results": [
    {
      "uuid": "ad3b520e-a424-4bcb-a6fb-7d1fc055c3fa",
      "state": "success",
      "name": "create_backup",
      "created_at": "2024-05-25T10:01:25Z",
      "updated_at": "2024-05-25T10:01:57Z",
      "progress": {
        "running": [],
        "total": 2,
        "completed": 2
      },
      "logbook": "myhypernodeappname",
      "tracker": {
        "uuid": null,
        "description": null
      }
    },
    ...
}
""",
        formatter_class=RawTextHelpFormatter,
    )
    parser.parse_args(args=args)
    client = get_client()
    app_name = get_app_name()
    print_response(client.get_flows(app_name))


def get_slas(args=None):
    parser = ArgumentParser(
        description="""
List all available SLAs.

Example:
$ ./bin/get_slas
[
  {
    "id": 123,
    "code": "sla-standard",
    "name": "SLA Standard",
    "price": 1234,
    "billing_period": 1,
    "billing_period_unit": "month"
  },
  ...
]
""",
        formatter_class=RawTextHelpFormatter,
    )
    parser.parse_args(args=args)
    client = get_client()
    print_response(client.get_slas())


def get_sla(args=None):
    parser = ArgumentParser(
        description="""
Get a specific SLA.

$ ./bin/get_sla sla-standard
{
  "id": 123,
  "code": "sla-standard",
  "name": "SLA Standard",
  "price": 1234,
  "billing_period": 1,
  "billing_period_unit": "month"
}
""",
        formatter_class=RawTextHelpFormatter,
    )
    parser.add_argument("sla_code", help="The code of the SLA to get")
    args = parser.parse_args(args=args)
    client = get_client()
    print_response(client.get_sla(args.sla_code))


def get_available_backups_for_app(args=None):
    parser = ArgumentParser(
        description="""
List the available backups for the Hypernode

Example:
$ ./bin/get_available_backups_for_app
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": [
    {
      "backup_created_at": "2024-05-02T12:00:33+02:00",
      "type": "periodic",
      "backup_id": "1169e792-8b05-449c-a7b1-7d52cf43153a",
      "expired_at": "2024-05-30T12:00:33+02:00"
    },
    ...
]
""",
        formatter_class=RawTextHelpFormatter,
    )
    parser.parse_args(args=args)
    client = get_client()
    app_name = get_app_name()
    print_response(client.get_available_backups_for_app(app_name))


def get_eav_description(args=None):
    parser = ArgumentParser(
        description="""
List all available EAV settings and their descriptions.

Example:
$ ./bin/get_eav_description
{
  "supervisor_enabled": [
    true,
    false
  ],
  "redis_eviction_policy": [
    "noeviction",
    "allkeys-lru",
    "allkeys-lfu",
    "volatile-lru",
    "volatile-lfu",
    "allkeys-random",
    "volatile-random",
    "volatile-ttl"
  ],
  ...
}
""",
        formatter_class=RawTextHelpFormatter,
    )
    parser.parse_args(args=args)
    client = get_client()
    print_response(client.get_app_eav_description())


def get_app_configurations(args=None):
    parser = ArgumentParser(
        description="""
List all the available configurations that can be selected when ordering a new Hypernode.

Example:
$ ./bin/get_app_configurations
{
  "count": 7,
  "next": null,
  "previous": null,
  "results": [
    {
      "name": "Akeneo 6.0",
      "configuration_id": "akeneo_6_0",
      "php_version": "8.0",
      "mysql_version": "8.0",
      ...
    },
    ...
}
""",
        formatter_class=RawTextHelpFormatter,
    )
    parser.parse_args(args=args)
    client = get_client()
    print_response(client.get_app_configurations())


def get_cluster_relations(args=None):
    parser = ArgumentParser(
        description="""
List all the cluster relations for the Hypernode.

Example:
$ ./bin/get_cluster_relations
{
  "parents": [
    {
      "id": 182,
      "parent": "mytestappdb",
      "child": "mytestappweb",
      "relation_type": "mysql",
      "cluster_description": null
    },
    {
      "id": 180,
      "parent": "mytestapp",
      "child": "mytestappweb",
      "relation_type": "loadbalancer",
      "cluster_description": null
    },
    ...
}
""",
        formatter_class=RawTextHelpFormatter,
    )
    parser.parse_args(args=args)
    client = get_client()
    app_name = get_app_name()
    print_response(client.get_cluster_relations(app_name))


def get_product_info(args=None):
    parser = ArgumentParser(
        description="""
Gets the product info for the specified product

$ ./bin/get_product_info FALCON_S_202203
{
  "code": "FALCON_S_202203",
  "name": "Falcon S",
  "backups_enabled": true,
  "storage_size_in_gb": 57,
  "price": 1234,
  ...
}
""",
        formatter_class=RawTextHelpFormatter,
    )
    client = get_client()
    parser.add_argument(
        "product_code",
        help="The code of the product to get",
        choices=[p["code"] for p in client.get_active_products().json()],
    )
    args = parser.parse_args(args=args)
    print_response(client.get_product_info_with_price(args.product_code))


def get_block_attack_descriptions(args=None):
    parser = ArgumentParser(
        description="""
List all attack blocking strategies and their descriptions.

Example:
$ ./bin/get_block_attack_descriptions
{
  "BlockSqliBruteForce": "Attempts to deploy NGINX rules to block suspected (blind) SQL injection attacks",
  ...
}
""",
        formatter_class=RawTextHelpFormatter,
    )
    parser.parse_args(args=args)
    client = get_client()
    print_response(client.get_block_attack_descriptions())


def block_attack(args=None):
    parser = ArgumentParser(
        description="""
Block a specific attack based on a pre-defined attack blocking strategy.

$ ./bin/block_attack BlockSqliBruteForce
A job to block the 'BlockSqliBruteForce' attack has been posted.
""",
        formatter_class=RawTextHelpFormatter,
    )
    client = get_client()
    choices = client.get_block_attack_descriptions().json().keys()
    parser.add_argument("attack_name", help="The attack to block", choices=choices)
    args = parser.parse_args(args=args)
    app_name = get_app_name()
    output = client.block_attack(app_name, args.attack_name).content
    if output:
        print(output)
    else:
        print(
            "A job to block the '{}' attack has been posted.".format(args.attack_name)
        )


def get_whitelist_options(args=None):
    parser = ArgumentParser(
        description="""
List all available WAF whitelist options for the Hypernode.

Example:
$ ./bin/get_whitelist_options
{
  "name": "Whitelist",
  "description": "",
  "renders": [
    "application/json"
  ],
  ...
}
""",
        formatter_class=RawTextHelpFormatter,
    )
    parser.parse_args(args=args)
    client = get_client()
    app_name = get_app_name()
    print_response(client.get_whitelist_options(app_name))


def get_whitelist_rules(args=None):
    parser = ArgumentParser(
        description="""
List all currently configured WAF whitelist rules for the Hypernode.

Example:
$ ./bin/get_whitelist_rules
[
  {
    "id": 1234,
    "created": "2024-05-25T13:39:48Z",
    "domainname": "yourhypernodeappname.hypernode.io",
    "ip": "1.2.3.4",
    "type": "database",
    "description": "my description"
  },
  ...
]
""",
        formatter_class=RawTextHelpFormatter,
    )
    parser.parse_args(args=args)
    client = get_client()
    app_name = get_app_name()
    print_response(client.get_whitelist_rules(app_name))


def get_current_product_for_app(args=None):
    parser = ArgumentParser(
        description="""
Gets the current product for the specified app.

Example:
$ ./bin/get_current_product_for_app
{
  "code": "FALCON_M_202203",
  "name": "Falcon M",
  "backups_enabled": true,
  "is_development": false,
  "varnish_supported": true,
  "supports_sla": true,
  "provider_flavors": [
    {
      "vcpus": 3,
      "ram_in_mb": 16384,
      ...
    },
    ...
}
""",
        formatter_class=RawTextHelpFormatter,
    )
    parser.parse_args(args=args)
    client = get_client()
    app_name = get_app_name()
    print_response(client.get_current_product_for_app(app_name))


def check_payment_information_for_app(args=None):
    parser = ArgumentParser(
        description="""
Shows the payment information for the specified app.

Example:
$ ./bin/check_payment_information_for_app
{
  "has_valid_vat_number": true,
  "has_valid_payment_method": true
}
""",
        formatter_class=RawTextHelpFormatter,
    )
    parser.parse_args(args=args)
    client = get_client()
    app_name = get_app_name()
    print_response(client.check_payment_information_for_app(app_name))


def get_active_products(args=None):
    parser = ArgumentParser(
        description="""
Lists all available products.

Example:
$ ./bin/get_active_products
[
  {
    "code": "JACKAL_S_202301",
    "name": "Jackal S",
    "backups_enabled": true,
    "is_development": false,
    ...
  },
  ...
]
""",
        formatter_class=RawTextHelpFormatter,
    )
    parser.parse_args(args=args)
    client = get_client()
    print_response(client.get_active_products())


def check_xgrade(args=None):
    parser = ArgumentParser(
        description="""
Verify that the specified app can be upgraded to the specified product.
This checks if there is enough disk space available. The output will also
show whether or not there will be an IP change and if a volume swap xgrade
would be performed instead of an rsync xgrade.

Example:
$ ./bin/check_xgrade FALCON_L_202203
{
  "has_valid_vat_number": true,
  "has_valid_payment_method": true,
  "will_change_ip": false,
  "will_do_volswap": false,
  "will_disk_fit": true
}
""",
        formatter_class=RawTextHelpFormatter,
    )
    client = get_client()
    parser.add_argument(
        "product_code",
        help="The code of the product to check",
        choices=[p["code"] for p in client.get_active_products().json()],
    )
    args = parser.parse_args(args=args)
    app_name = get_app_name()
    print_response(client.check_xgrade(app_name, args.product_code))


def xgrade(args=None):
    parser = ArgumentParser(
        description="""
Change the plan of your Hypernode.

Example:
$ ./bin/xgrade FALCON_L_202203
The job to xgrade Hypernode 'yourappname' to product 'FALCON_L_202203' has been posted
""",
        formatter_class=RawTextHelpFormatter,
    )
    client = get_client()
    parser.add_argument(
        "product_code",
        help="The code of the product to check",
        choices=[p["code"] for p in client.get_active_products().json()],
    )
    args = parser.parse_args(args=args)
    app_name = get_app_name()
    data = {"product": args.product_code}
    output = client.xgrade(app_name, data=data).content
    if output:
        print(output)
    else:
        print(
            "The job to xgrade Hypernode '{}' to product '{}' "
            "has been posted".format(app_name, args.product_code)
        )


def get_active_branchers(args=None):
    parser = ArgumentParser(
        description="""
List all active branchers

Example:
$ ./bin/get_active_branchers
{
  "monthly_total_time": 0,
  "total_minutes_elapsed": 0,
  "actual_monthly_total_cost": 0,
  "monthly_total_cost": 0,
  "branchers": []
}
""",
        formatter_class=RawTextHelpFormatter,
    )
    parser.parse_args(args=args)
    client = get_client()
    app_name = get_app_name()
    print_response(client.get_active_branchers(app_name))


def create_brancher(args=None):
    parser = ArgumentParser(
        description="""
Create a Brancher Hypernode from the specified app.
Outputs the app_info of the brancher to be created..

Example:
$ ./bin/create_brancher
{
  "name": "yourappname-ephoj82yb",
  "parent": "yourappname",
  "type": "brancher",
  "product": "FALCON_M_202203",
  "domainname": "yourappname-ephoj82yb.hypernode.io",
  ...
}
""",
        formatter_class=RawTextHelpFormatter,
    )
    parser.parse_args(args=args)
    client = get_client()
    app_name = get_app_name()
    data = {}
    print_response(client.create_brancher(app_name, data=data))


def destroy_brancher(args=None):
    parser = ArgumentParser(
        description="""
Destroy a Brancher Hypernode.

Examples:
$ ./bin/destroy_brancher yourbrancherappname-eph12345
A job has been posted to cancel the 'yourbrancherappname-eph12345' brancher app.
""",
        formatter_class=RawTextHelpFormatter,
    )
    parser.add_argument(
        "brancher_app_name",
        help="The name of the brancher to destroy. See ./bin/get_active_branchers",
    )
    args = parser.parse_args(args=args)
    client = get_client()
    try:
        client.destroy_brancher(args.brancher_app_name)
        print(
            "A job has been posted to cancel the '{}' brancher app.".format(
                args.brancher_app_name
            )
        )
        exit(EX_OK)
    except Exception as e:
        print(
            "Brancher app '{}' failed to be cancelled: {}".format(
                args.brancher_app_name, e
            )
        )
        exit(EX_UNAVAILABLE)


def get_fpm_status(args=None):
    parser = ArgumentParser(
        description="""
Show the status of the PHP-FPM workers.

Example:
$ ./bin/get_fpm_status
{
  "message": null,
  "data": "50570 IDLE   0.0s -  phpfpm    127.0.0.1       GET  magweb/status.php   (python-requests/2.28.1)\n50571 IDLE   0.0s -  phpfpm    127.0.0.1       GET  magweb/status.php   (python-requests/2.28.1)\n",
  "status": 200
}
""",
        formatter_class=RawTextHelpFormatter,
    )
    parser.parse_args(args=args)
    client = get_client()
    app_name = get_app_name()
    print_response(client.get_fpm_status(app_name))
