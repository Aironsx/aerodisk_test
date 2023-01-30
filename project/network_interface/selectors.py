from .models import NetworkInterface


class NetworkInterfaceSelector:

    def get_enabled_network_interface(self, name):
        if self.__enabled_network_interface is None:
            self.__enabled_network_interface = (
                NetworkInterface.query.filter_by(name=name,
                                                 is_enable=True).first()
            )
        return self.__enabled_network_interface

    def get_network_interface(self, name):
        if self.__network_interface is None:
            self.__network_interface = (
                NetworkInterface.query.filter_by(name=name).first()
            )
        return self.__network_interface

    def get_network_interfaces(self):
        if self.__network_interfaces is None:
            self.__network_interfaces = (
                NetworkInterface.query.all()
            )
        return self.__network_interfaces

    def flush_cache(self):
        self.__init__()

    def __init__(self):
        self.__enabled_network_interface = None
        self.__network_interface = None
        self.__network_interfaces = None
