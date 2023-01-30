from project import create_app, db

app = create_app()

with app.app_context():
    from project.users.models import User
    from project.network_interface.models import NetworkInterface
    db.create_all()
app.run()
