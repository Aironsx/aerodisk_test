import abc
import subprocess
from typing import TYPE_CHECKING, Optional

from project.config import Config

if TYPE_CHECKING:
    from .services import NetworkInterface


class AbstractLinuxCommandNetworkInterface(abc.ABC):

    def __init__(self, network_interface: 'NetworkInterface') -> None:
        self.network_interface = network_interface

    @abc.abstractmethod
    def enable_network_interface(self):
        ...

    @abc.abstractmethod
    def disable_network_interface(self):
        ...

    @abc.abstractmethod
    def change_ip_address(self, current_ip, new_ip, prefix):
        ...

    @abc.abstractmethod
    def change_prefix(self, ip_address, current_prefix, new_prefix):
        ...


class LinuxCommandNetworkInterface(AbstractLinuxCommandNetworkInterface):

    def enable_network_interface(self) -> None:
        linux_command = f'sudo -S ip link set {self.network_interface.name} up'
        self._execute_command(linux_command, sudo=True)
        self._validate_is_enable()

    def disable_network_interface(self) -> None:
        linux_command = (f'sudo -S ip link set {self.network_interface.name} '
                         f'down')
        self._execute_command(linux_command, sudo=True)
        self._validate_is_disable()

    def change_ip_address(self,
                          current_ip: str,
                          new_ip_address: str,
                          prefix: str) -> None:
        linux_command_add = (
            f'sudo -S ip addr add {new_ip_address}/{prefix} dev '
            f'{self.network_interface.name}')
        linux_command_del = (f'sudo -S ip addr del {current_ip}/{prefix} dev '
                             f'{self.network_interface.name}')
        self._execute_command(linux_command_add, sudo=True)
        self._execute_command(linux_command_del)
        self._validate_is_ip_changed(new_ip_address)

    def change_prefix(self,
                      ip_address: str,
                      current_prefix: str,
                      new_prefix: str) -> None:
        linux_command_add = (
            f'sudo -S ip addr add {ip_address}/{new_prefix} dev '
            f'{self.network_interface.name}')
        linux_command_del = (
            f'sudo -S ip addr del {ip_address}/{current_prefix} dev '
            f'{self.network_interface.name}')
        self._execute_command(linux_command_add, sudo=True)
        self._execute_command(linux_command_del)
        self._validate_is_prefix_changed(new_prefix)

    @staticmethod
    def _execute_command(linux_command: str,
                         sudo: bool = False) -> Optional[str]:
        if sudo:
            process = subprocess.Popen(linux_command.split(),
                                       stdin=subprocess.PIPE,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       text=True)
            process.stdin.write(Config().SUDO_PASSWORD)
            process.stdin.close()
            return process.stdout
        process = subprocess.run(linux_command.split(), capture_output=True,
                                 text=True)
        return process.stdout

    def _validate_is_enable(self) -> None:
        linux_command = f'ip a show {self.network_interface.name} up'
        if self._execute_command(linux_command):
            raise ValueError(f'{self.network_interface.name} not enabled')

    def _validate_is_disable(self) -> None:
        linux_command = (f'ip -4 -brief address show'
                         f' {self.network_interface.name} up')
        if self._execute_command(linux_command):
            raise ValueError(f'{self.network_interface.name} not disabled')

    def _validate_is_ip_changed(self, ip_address: str) -> None:
        IP_ADDRESS_WITH_MASK = 2
        IP_ADDRESS = 0

        linux_command = (f'ip -4 -brief address show'
                         f' {self.network_interface.name}')
        result = self._execute_command(linux_command)
        current_ip_address = (
            result.split()[IP_ADDRESS_WITH_MASK].split('/')[IP_ADDRESS]
        )
        if current_ip_address != ip_address:
            raise ValueError(f'{self.network_interface.ip_address} not '
                             f'changed')

    def _validate_is_prefix_changed(self, prefix: str) -> None:
        IP_ADDRESS_WITH_MASK = 2
        PREFIX = 1

        linux_command = (f'ip -4 -brief address show'
                         f' {self.network_interface.name}')
        result = self._execute_command(linux_command)
        if result:
            current_prefix = (
                result.split()[IP_ADDRESS_WITH_MASK].split('/')[PREFIX]
            )
            if current_prefix != prefix:
                raise ValueError(f'{self.network_interface.prefix} not '
                                 'changed')

    @staticmethod
    def get_network_interface_names():
        linux_command = 'ls /sys/class/net'
        result = subprocess.run(linux_command.split(),
                                capture_output=True,
                                text=True)
        for name in result.stdout.split():
            yield name.rstrip()

    @staticmethod
    def get_interface_data(name: str) -> str:
        linux_command = f'ip -4 -brief address show {name}'
        result = subprocess.run(linux_command.split(),
                                capture_output=True,
                                text=True)
        return result.stdout.rstrip()

    @staticmethod
    def get_availability_status(name: str) -> bool:
        linux_command = f'ip a show {name} up'
        result = subprocess.run(linux_command.split(),
                                capture_output=True,
                                text=True)
        return bool(result.stdout)
