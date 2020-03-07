# -*- coding: utf-8 -*-

from myproject import app
from myproject.models import User

app.run(debug=True)
User.init_admin()
