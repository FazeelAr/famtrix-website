from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

# Initialize admin
admin = Admin(app, name='Admin Panel', template_mode='bootstrap4')

# Add your models
admin.add_view(ModelView(ContactRequest, db.session))
