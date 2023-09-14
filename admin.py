from fastapi_admin.app import FastAPIAdmin
from main import app
import models

admin = FastAPIAdmin(app)

# Register your models (in this case, the Book model)
admin.register('Users', models.User)
admin.register('Items', models.Item)
