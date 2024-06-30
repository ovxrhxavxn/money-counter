import uvicorn

from app import FastAPIWrapper
from users.router import UserAPIRouterWrapper
from cv_models.router import CVAPIRouterWrapper

app_wrapper = FastAPIWrapper()

app = app_wrapper.app

if __name__ == '__main__':

    routers = [
        
        UserAPIRouterWrapper().router,
        CVAPIRouterWrapper().router
        
        ]
    
    for r in routers:
        app_wrapper.routers.append(r)
        

    uvicorn.run("main:app", 
                
                host="127.0.0.1", 
                
                port=8000, 
                
                log_level="info",

                reload=True 
    )