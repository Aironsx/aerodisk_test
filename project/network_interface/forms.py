from wtforms import Form, StringField


class ChangeIpForm(Form):
    ip_address = StringField('New ip address')


class ChangePrefixForm(Form):
    prefix = StringField('New mask address')
