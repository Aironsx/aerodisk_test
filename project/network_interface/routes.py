from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_required

from project.network_interface.forms import ChangeIpForm, ChangePrefixForm
from project.network_interface.selectors import NetworkInterfaceSelector
from project.network_interface.services import (InitNetworkInterfaces,
                                                NetworkInterface)

network_interface = Blueprint('network_interface',
                              __name__,
                              template_folder='templates',
                              static_folder='static')


@network_interface.route('/list', methods=['GET'])
@login_required
def list_network_interfaces():
    data = NetworkInterfaceSelector().get_network_interfaces()
    return render_template('network_interface/list_network_interface.html',
                           data=data)


@network_interface.route('/<string:interface_name>', methods=['GET'])
@login_required
def get_network_interface(interface_name):
    interface = (
        NetworkInterfaceSelector().get_network_interface(interface_name)
    )
    return render_template('network_interface/get_network_interface.html',
                           interface=interface)


@network_interface.route('create_interfaces', methods=['GET'])
@login_required
def create_network_interfaces():
    InitNetworkInterfaces().init_existing_network_interfaces()
    return redirect(url_for('.list_network_interfaces'))


@network_interface.route('/enable/<string:interface_name>', methods=['GET'])
@login_required
def enable_network_interface(interface_name):
    interface_db_obj = (
        NetworkInterfaceSelector().get_network_interface(interface_name)
    )
    interface = NetworkInterface(name=interface_db_obj.name,
                                 ip_address=interface_db_obj.ip_address,
                                 prefix=interface_db_obj.prefix)
    interface.enable()
    return redirect(url_for('.get_network_interface',
                            interface_name=interface_name))


@network_interface.route('/disable/<string:interface_name>', methods=['GET'])
@login_required
def disable_network_interface(interface_name):
    interface_db_obj = (
        NetworkInterfaceSelector().get_network_interface(interface_name)
    )
    interface = NetworkInterface(name=interface_db_obj.name,
                                 ip_address=interface_db_obj.ip_address,
                                 prefix=interface_db_obj.prefix)
    interface.disable()
    return redirect(url_for('.get_network_interface',
                            interface_name=interface_name))


@network_interface.route('/change_ip/<string:interface_name>',
                         methods=['GET', 'POST'])
@login_required
def change_ip_address(interface_name):
    form = ChangeIpForm(request.form)
    interface_db_obj = (
        NetworkInterfaceSelector().get_network_interface(interface_name)
    )
    if request.method == 'POST' and form.validate():
        interface = NetworkInterface(name=interface_db_obj.name,
                                     ip_address=interface_db_obj.ip_address,
                                     prefix=interface_db_obj.prefix)
        interface.change_ip_address(form.ip_address.data)
        return redirect(url_for('.get_network_interface',
                                interface_name=interface_name))
    return render_template('network_interface/change_ip_address.html',
                           interface=interface_db_obj, form=form)


@network_interface.route('/change_mask/<string:interface_name>',
                         methods=['GET', 'POST'])
@login_required
def change_prefix(interface_name):
    form = ChangePrefixForm(request.form)
    interface_db_obj = (
        NetworkInterfaceSelector().get_network_interface(interface_name)
    )
    if request.method == 'POST' and form.validate():
        interface = NetworkInterface(name=interface_db_obj.name,
                                     ip_address=interface_db_obj.ip_address,
                                     prefix=interface_db_obj.prefix)
        interface.change_prefix(form.prefix.data)
        return redirect(url_for('.get_network_interface',
                                interface_name=interface_name))
    return render_template('network_interface/change_prefix.html',
                           interface=interface_db_obj, form=form)
