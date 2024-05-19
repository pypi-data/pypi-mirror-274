"""Console script for rstms_mailgun."""

import json
import shlex
import subprocess
import sys
import time

import click
import click.core
import requests
from requests.auth import HTTPBasicAuth

from .exception_handler import ExceptionHandler
from .shell import _shell_completion
from .version import __timestamp__, __version__

header = f"{__name__.split('.')[0]} v{__version__} {__timestamp__}"

VERIFY_INTERVAL = 5
VERIFY_TIMEOUT = 60


def fail(msg):
    click.echo(msg, err=True)
    sys.exit(-1)


def _ehandler(ctx, option, debug):
    ctx.obj = dict(ehandler=ExceptionHandler(debug))
    ctx.obj["debug"] = debug


class Context:
    def __init__(self, api_key, domain):
        self.api_key = api_key
        self.base_url = "https://api.mailgun.net"
        self.auth = HTTPBasicAuth("api", api_key)
        self.json = True
        self.domain = domain
        self.quiet = False
        self.compact = False
        self.get_domains()

    def _request(self, func, path, **kwargs):
        url = f"{self.base_url}/{path}"
        kwargs["auth"] = self.auth
        response = func(url, **kwargs)
        response.raise_for_status()
        return response.json()

    def get(self, path, **kwargs):
        return self._request(requests.get, path, **kwargs)

    def put(self, path, **kwargs):
        return self._request(requests.put, path, **kwargs)

    def delete(self, path, **kwargs):
        return self._request(requests.delete, path, **kwargs)

    def post(self, path, **kwargs):
        return self._request(requests.post, path, **kwargs)

    def validate(self, exists=True, dns_domain=True):
        if exists is True:
            if self.domain not in self.domain_names:
                fail(f"Unknown domain: {repr(self.domain)}")
        elif exists is False:
            if self.domain in self.domain_names:
                fail(f"Domain exists: {repr(self.domain)}")

        if dns_domain:
            if "." not in self.domain:
                fail(f"Unexpected domain format: {repr(self.domain)}")

    def get_domains(self):
        result = self.get("v4/domains")
        self.domains = {item["name"]: item for item in result["items"]}
        self.domain_names = list(self.domains.keys())
        return self.domains

    def exit(self, exit_code=0, output=None):
        if output and not self.quiet:
            if self.json:
                if self.compact:
                    output = json.dumps(output, separators=(",", ":"))
                else:
                    output = json.dumps(output, indent=2)
            else:
                if isinstance(output, dict):
                    output = "\n".join([f"{k}: {v}" for k, v in output.items()])
                elif isinstance(output, list):
                    output = "\n".join(output)
            click.echo(output)
        sys.exit(exit_code)

    def list(self):
        ret = 0 if (self.domain is None or self.domain in self.domain_names) else -1
        self.exit(ret, self.domain_names)

    def get_status(self):
        result = self.get(f"v4/domains/{self.domain}")
        records = self.get_dns_records(result)
        return dict(
            domain=self.domain,
            state=result["domain"]["state"],
            spf=records["SPF"]["valid"],
            dkim=records["DKIM"]["valid"],
        )

    def get_dns_records(self, result=None):
        if not result:
            result = self.get(f"v4/domains/{self.domain}")
        ret = {}
        for record in result["sending_dns_records"]:
            _type = record["record_type"]
            value = record["value"]
            name = record["name"]
            if _type == "TXT" and "spf" in value:
                ret["SPF"] = record
            elif _type == "TXT" and "domainkey" in name:
                ret["DKIM"] = record
            elif _type == "CNAME":
                ret["CNAME"] = record
        return ret


@click.group("mailgun", context_settings={"auto_envvar_prefix": "MAILGUN"})
@click.version_option(message=header)
@click.option("-k", "--api-key", envvar="MAILGUN_API_KEY", show_envvar=True, help="mailgun API key")
@click.option("-d", "--debug", is_eager=True, is_flag=True, callback=_ehandler, help="debug mode")
@click.option("-v", "--verbose", is_flag=True, help="enable verbose output")
@click.option("-q", "--quiet", is_flag=True, help="suppress stdout")
@click.option("-c", "--compact", is_flag=True, help="compact JSON output")
@click.option("-j/-J", "--json/--no-json", "json_format", is_flag=True, default=True, help="output JSON")
@click.option("-f", "--force", is_flag=True, help="bypass confirmation")
@click.argument("domain")
@click.option(
    "--shell-completion",
    is_flag=False,
    flag_value="[auto]",
    callback=_shell_completion,
    help="configure shell completion",
)
@click.pass_context
def cli(ctx, domain, api_key, verbose, debug, quiet, json_format, compact, shell_completion, force):
    """rstms_mailgun top-level help"""
    ctx.obj = Context(api_key, domain)
    ctx.obj.json = json_format
    ctx.obj.quiet = quiet
    ctx.obj.compact = compact
    ctx.obj.verbose = verbose
    ctx.obj.force = force


@cli.command("list")
@click.pass_obj
def domains(ctx):
    """list configured domains"""
    ctx.list()


@cli.command()
@click.pass_obj
def exists(ctx):
    """exit code indicates domain configured in mailgun account"""
    ctx.validate(exists=None)
    ret = ctx.domain in ctx.domain_names
    ctx.exit(0 if ret else -1, str(ret))


@cli.command
@click.pass_obj
def detail(ctx):
    """detail for named domain"""
    ctx.validate(exists=True)
    result = ctx.get(f"v3/domains/{ctx.domain}")
    ctx.exit(0, result)


@cli.command
@click.pass_obj
def delete(ctx):
    """delete a domain"""
    ctx.validate(exists=True)
    if not ctx.force:
        click.confirm(f"Confirm DELETE mailgun domain {ctx.domain}?", abort=True)
    result = ctx.delete(f"v3/domains/{ctx.domain}")
    ctx.exit(0, result)


@cli.command
@click.option("-w", "--wildcard", is_flag=True, help="accept email from subdomains when sending")
@click.option("-d", "--dkim-key-size", type=click.Choice(["1024", "2048"]), default=None, help="set DKIM key size")
@click.option("-P", "--smtp-password", help="SMTP authentication password")
@click.option("-A", "--force-dkim-authority", is_flag=True, help="DKIM authority will be the created domain")
@click.option("-R", "--force-root-dkim-host", is_flag=True, help="DKIM authority will be the root domain")
@click.option("-h", "--dkim-host-name", help="DKIM host name")
@click.option("-s", "--dkim-selector", help="set DKIM selector for created domain")
@click.option("-p", "--pool-id", help="request IP Pool")
@click.option("-i", "--assign-ip", help="comma separated list of IP addresses assigned to new domain")
@click.option("-W", "--web-scheme", type=click.Choice(["http", "https"]), default=None, help="domain web scheme")
@click.option("-f", "--force", is_flag=True, help="bypass confirmation")
@click.pass_obj
def create(  # noqa: C901
    ctx,
    wildcard,
    dkim_key_size,
    smtp_password,
    force_dkim_authority,
    force_root_dkim_host,
    dkim_host_name,
    dkim_selector,
    pool_id,
    assign_ip,
    web_scheme,
    force,
):
    """create domain"""

    ctx.validate(exists=False)
    params = dict(name=ctx.domain)
    if wildcard:
        params["wildcard"] = True
    if dkim_key_size:
        params["dkim_key_size"] = dkim_key_size
    if smtp_password:
        params["smtp_password"] = smtp_password
    if force_dkim_authority:
        params["force_dkim_authority"] = True
    if force_root_dkim_host:
        params["force_root_dkim_host"] = True
    if dkim_host_name:
        params["dkim_host_name"] = dkim_host_name
    if dkim_selector:
        params["dkim_selector"] = dkim_selector
    if pool_id:
        params["pool_id"] = pool_id
    if assign_ip:
        params["ips"] = assign_ip
    if web_scheme:
        params["web_scheme"] = web_scheme
    if not ctx.force:
        click.echo("Creating domain {ctx.domain}:")
        click.echo(json.dumps(params, indent=2))
        click.confirm("Confirm?", abort=True)
    result = ctx.post("v4/domains", params=params)
    ctx.exit(0, result['message'])


@cli.command
@click.option("-P", "--smtp-password", help="SMTP authentication password")
@click.option("-w", "--wildcard", is_flag=True, help="accept email from subdomains when sending")
@click.option("-W", "--web-scheme", type=click.Choice(["http", "https"]), default=None, help="domain web scheme")
@click.option("-f", "--mail-from", help="MAILFROM hostname for outbound email")
@click.option(
    "-s", "--spam-action", type=click.Choice(["disabled", "tag", "block"]), default=None, help="domain web scheme"
)
@click.pass_obj
def update(ctx, smtp_password, wildcard, web_scheme, spam_action, mail_from):
    """update domain configuration"""

    ctx.validate(exists=True)

    if mail_from:
        result = ctx.put(f"v3/domains/{ctx.domain}/mailfrom_host", params=dict(mailfrom_host=mail_from))
        ctx.exit(0, result)

    params = dict(name=ctx.domain)
    if wildcard:
        params["wildcard"] = True
    if smtp_password:
        params["smtp_password"] = smtp_password
    if web_scheme:
        params["web_scheme"] = web_scheme
    if spam_action:
        params["spam_action"] = spam_action

    if len(params.keys()) > 1:
        result = ctx.put(f"v4/domains/{ctx.domain}", params=params)
        msg = result["message"]
    else:
        msg = "unchanged"
    ctx.exit(0, msg)


@cli.command
@click.option("-w", "--wait", is_flag=True, help="wait for verification")
@click.option("-i", "--interval", type=int, default=VERIFY_INTERVAL, help="seconds between verify requests")
@click.option("-t", "--timeout", type=int, default=VERIFY_TIMEOUT, help="wait timeout in seconds")
@click.argument("domain", required=False)
@click.pass_obj
def verify(ctx, domain, wait, interval, timeout):
    """request domain verification"""
    ctx.validate(exists=True)

    status = ctx.get_status()

    request_time = 0
    timeout_time = 0

    if timeout:
        timeout_time = time.time() + timeout
    else:
        timeout_time = 0

    while status["state"] != "active":

        if time.time() > request_time:
            if ctx.verbose:
                click.echo(f"\nRequesting verification...", nl=False)
            response = ctx.put(f"v4/domains/{ctx.domain}/verify")
            requested = True
            if ctx.verbose:
                click.echo(f"{response['message']}")
                first = True
            request_time = time.time() + interval

        if not wait:
            break

        if ctx.verbose:
            if requested:
                requested = False
                click.echo(f"Status: {status['state']}; waiting...", nl=False)
            else:
                click.echo('.', nl=False)

        if timeout and time.time() > timeout_time:
            fail("Timeout")

        time.sleep(1)
        status = ctx.get_status()

    if ctx.verbose:
        click.echo()

    ctx.exit(0, status)


@cli.command
@click.argument("domain", required=False)
@click.pass_obj
def status(ctx, domain):
    """output verification state"""
    ctx.validate(exists=True)
    status = ctx.get_status()
    ret = 0 if status["state"] == "active" else -1
    ctx.exit(ret, status)


def dns_cmd(*args, dry_run=False, parse_json=True):
    if dry_run:
        click.echo(shlex.join(args))
        ret = []
    else:
        proc = subprocess.run(args, text=True, capture_output=True, check=True)
        if parse_json:
            ret = json.loads(proc.stdout)
        else:
            ret = proc.stdout.strip()
    return ret


def find_dns_record(record, dns_records, domain_name):
    if record["name"] in ["@", domain_name]:
        name = domain_name
    else:
        name = ".".join([record["name"], domain_name])
    for dns in dns_records:
        if dns["name"] == name and dns["type"] == record["type"]:
            return dns
    return {}


@cli.command
@click.option(
    "-e",
    "--exec",
    "dns_exec",
    envvar="MAILGUN_DNS_EXEC",
    show_envvar=True,
    default="cloudflare",
    help="execute dns update command",
)
@click.option("-d", "--delete", "dns_delete", is_flag=True, help="delete from DNS")
@click.option("-u", "--update", "dns_update", is_flag=True, help="update to DNS")
@click.option("-q/-Q", "--query/--no-query", "dns_query", is_flag=True, default=True, help="query DNS")
@click.option("-c/-C", "--cname/--no-cname", is_flag=True, default=False, help="include CNAME record")
@click.option("-s/-S", "--spf/--no-spf", is_flag=True, default=True, help="include SPF record")
@click.option("-k/-K", "--dkim/--no-dkim", is_flag=True, default=True, help="include DKIM record")
@click.option("--dry-run", is_flag=True, help="output dns-exec command line to stdout")
@click.pass_obj
def dns(ctx, dns_exec, dry_run, dns_update, dns_delete, dns_query, cname, spf, dkim):  # noqa: C901
    """show|update|delete required DNS records"""

    ctx.validate(exists=True)
    mailgun_records = ctx.get_dns_records()

    records = []
    for record in mailgun_records.values():
        out = {}
        if record["record_type"] == "CNAME" and not cname:
            continue
        if record["record_type"] == "TXT":
            if "_domainkey" in record["name"] and not dkim:
                continue
            if "v=spf1" in record["value"] and not spf:
                continue

        name = record["name"]
        if name.endswith(ctx.domain):
            name = name[: -1 - len(ctx.domain)]
        if not name:
            name = "@"
        out["domain"] = ctx.domain
        out["name"] = name
        out["type"] = record["record_type"]
        out["value"] = record["value"]
        out['dns'] = 'unknown'
        records.append(out)

    if dns_update or dns_delete or dns_query:
        dns_records = dns_cmd(dns_exec, "--json", "list", ctx.domain, dry_run=dry_run)

        for record in records:
            dns_record = find_dns_record(record, dns_records, ctx.domain)
            record["id"] = dns_record.get("id", None)
            if dns_record.get("content", None) is None:
                record["dns"] = "absent"
            elif record["value"] == dns_record.get("content", None):
                record["dns"] = "present"
            else:
                record["dns"] = "mismatch"

    if dns_delete:
        for record in records:
            if record["dns"] in ["present", "mismatch"]:
                dns_cmd(dns_exec, "delete", ctx.domain, "ID", record["id"], dry_run=dry_run, parse_json=False)
                record["id"] = None
                record["dns"] = "deleted"

    if dns_update:
        for record in records:
            if record["dns"] == "mismatch":
                dns_cmd(dns_exec, "delete", ctx.domain, "ID", record["id"], dry_run=dry_run, parse_json=False)
                record["dns"] == "deleted"
            if record["dns"] != "present":
                result = dns_cmd(
                    dns_exec,
                    "create",
                    ctx.domain,
                    record["type"],
                    record["name"],
                    record["value"],
                    dry_run=dry_run,
                    parse_json=False,
                )
                record["dns"] = "updated"
                record["id"] = result.strip().split()[0]

    for record in records:
        record.pop("id", None)


    if ctx.json:
        ret = records
    else:
        ret = []
        for record in records:
            name = record["name"]
            if name == ctx.domain or name == "@":
                name = ctx.domain
            else:
                name = ".".join([name, ctx.domain])
            ret.append(" ".join(
                [
                    name,
                    record["type"],
                    record["value"],
                    record.get("dns", ""),
                ]

            ))

    ctx.exit(0, ret)


if __name__ == "__main__":
    sys.exit(cli())  # pragma: no cover
