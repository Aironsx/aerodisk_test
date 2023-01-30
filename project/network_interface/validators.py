from ipaddress import AddressValueError, IPv4Address, IPv6Address, ip_address


class IpAddressValidator:

    def validate(self, address: str) -> None:
        self._validate_is_ipaddress(address)

    @staticmethod
    def _validate_is_ipaddress(address: str) -> None:
        try:
            ip_address(address)
        except AddressValueError:
            raise 'my_custom_exception'

    @staticmethod
    def validate_is_ipv4(address):
        try:
            IPv4Address(address)
            return True
        except AddressValueError:
            return False

    @staticmethod
    def validate_is_ipv6(address):
        try:
            IPv6Address(address)
            return True
        except AddressValueError:
            return False


class MaskValidator:

    @staticmethod
    def validate(ip_address):
        return
