from typing import Union

from project import db
from project.network_interface import linux_commands, models
from project.network_interface.models import NetworkInterfaceType
from project.network_interface.selectors import NetworkInterfaceSelector
from project.network_interface.validators import IpAddressValidator


class NetworkInterface:

    def __init__(self, name: str, ip_address: str, prefix: str) -> None:
        self.name = name
        self.ip_address = ip_address
        self.prefix = prefix
        self.__linux_command = None

    @property
    def linux_commands(self):
        if self.__linux_command is None:
            self.__linux_command = (
                linux_commands.LinuxCommandNetworkInterface(self)
            )
        return self.__linux_command

    def enable(self) -> None:
        if self._is_enabled():
            raise ValueError(f'{self} already enabled')
        self.linux_commands.enable_network_interface()
        self._write_to_db('is_enable', True)

    def disable(self) -> None:
        if not self._is_enabled():
            raise ValueError(f'{self} already disabled')
        self.linux_commands.disable_network_interface()
        self._write_to_db('is_enable', False)

    def change_ip_address(self, ip_address):
        if not self._is_enabled():
            raise ValueError(f'{self} is disabled')
        self.linux_commands.change_ip_address(current_ip=self.ip_address,
                                              new_ip_address=ip_address,
                                              prefix=self.prefix)
        self._set_attrs('ip_address', ip_address)
        self._write_to_db('ip_address', ip_address)

    def change_prefix(self, prefix):
        if not self._is_enabled():
            raise ValueError(f'{self} is disabled')
        self.linux_commands.change_prefix(ip_address=self.ip_address,
                                          current_prefix=self.prefix,
                                          new_prefix=prefix)
        self._set_attrs('prefix', prefix)
        self._write_to_db('prefix', prefix)

    def _is_enabled(self) -> bool:
        return bool(NetworkInterfaceSelector().
                    get_enabled_network_interface(self.name))

    def _set_attrs(self, field, value):
        setattr(self, field, value)

    def _write_to_db(self, field: str, value: Union[bool, str]) -> None:
        selector = NetworkInterfaceSelector()
        obj = selector.get_network_interface(name=self.name)
        setattr(obj, field, value)
        db.session.add(obj)
        db.session.commit()
        selector.flush_cache()

    def __str__(self):
        return f'Network interface {self.name} {self.ip_address} {self.prefix}'


class InitNetworkInterfaces:
    def init_existing_network_interfaces(self):
        for name in linux_commands.get_network_interface_names():
            if data := linux_commands.get_interface_data(name):
                clear_data = self._get_clear_data(data)
                obj = (models.NetworkInterface(**clear_data))
                db.session.add(obj)
        db.session.flush()
        db.session.commit()

    @staticmethod
    def _get_clear_data(data):
        ENABLE_STATE = {
            'UP': True,
            'DOWN': False,
            'UNKNOWN': False
        }
        name, is_enable, ip_address_with_prefix = data.split()
        ip_address, prefix = ip_address_with_prefix.split('/')
        validator = IpAddressValidator()
        ip_type = (
            NetworkInterfaceType.ipv4 if validator.validate_is_ipv4(ip_address)
            else NetworkInterfaceType.ipv6
        )
        return {
            'name': name,
            'ip_address': ip_address,
            'ip_type': ip_type,
            'prefix': prefix,
            'is_enable': ENABLE_STATE[is_enable]
        }
