from app import FastAPIAppWrapper
from users.api import UserAPI
from cv_models.api import CVAPI


app_wrapper = FastAPIAppWrapper()

app = app_wrapper.app

routers = [
    
    CVAPI().router,
    UserAPI().router

    ]
    
app_wrapper.include_routers_to_app(routers)