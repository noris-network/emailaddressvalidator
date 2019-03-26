import dns.resolver
import ipaddress
import re

class EmailAddressValidator(object):
    """
    With this you can check if an email address is valid.

    You can customize behaviour with constructor arguments:

        message (string): The error message that is raised when validation fails.
        check_mx (bool): Try to look up a MX record on the domain part in DNS.
        whitelist (list): A list of domain names that will validate without being checked.

    The instance of EmailAddressValidator is a callable, so just call it by passing it a string that
    you want to validate

        Raises:
            AssertionError if the given email address fails to validate.

    Shamelessly stolen from django 1.11 and adjusted to taste.

    """
    message = 'Enter a valid email address.'
    user_regex = re.compile(
        r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*\Z"  # dot-atom
        r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013\014\016-\177])*"\Z)',
        # quoted-string
        re.IGNORECASE)
    domain_regex = re.compile(
        # max length for domain name labels is 63 characters per RFC 1034
        r'((?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+)(?:[A-Z0-9-]{2,63}(?<!-))\Z',
        re.IGNORECASE)
    literal_regex = re.compile(
        # literal form, ipv4 or ipv6 address (SMTP 4.1.3)
        r'\[([A-f0-9:\.]+)\]\Z',
        re.IGNORECASE)
    domain_whitelist = []

    def __init__(self, message=None, check_mx=False, whitelist=None, allow_ip_literals=False):
        if message is not None:
            self.message = message
        if whitelist is not None:
            self.domain_whitelist = whitelist
        self.check_mx = check_mx
        self.allow_ip_literals = allow_ip_literals

    def __call__(self, value):

        assert value and '@' in value, self.message

        user_part, domain_part = value.rsplit('@', 1)

        assert self.user_regex.match(user_part), self.message

        if domain_part not in self.domain_whitelist:
            try:
                is_literal = self.validate_domain_part(domain_part)
            except AssertionError:
                # Try for possible IDN domain-part
                try:
                    domain_part = domain_part.encode('idna').decode('ascii')
                except UnicodeError:
                    raise AssertionError(self.message) from None
                else:
                    is_literal = self.validate_domain_part(domain_part)
            if self.check_mx and not is_literal:
                self.validate_mx(domain_part)

    def validate_domain_part(self, domain_part):
        if self.allow_ip_literals:
            literal_match = self.literal_regex.match(domain_part)
        else:
            literal_match = False

        if self.domain_regex.match(domain_part):
            pass
        elif literal_match:
            ip_address = literal_match.group(1)
            try:
                ipaddress.ip_address(ip_address)
            except ValueError:
                raise AssertionError(self.message) from None
        else:
            raise AssertionError(self.message)

        return True if literal_match else False

    def validate_mx(self, domain_part):
        try:
            dns.resolver.query(domain_part + '.', 'MX')
        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer) as e:
            raise AssertionError(str(e)) from None

