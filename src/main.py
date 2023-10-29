from fastapi import Request
from starlette.responses import JSONResponse

from core.config.settings import settings
from core.errors import CustomError
from core.log import log
from core.registar import register_app

app = register_app()


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    log.exception("Alarm! Global exception!")
    return JSONResponse(
        status_code=500,
        content={"error": "O-o-o-ps! Internal server error"}
    )

@app.exception_handler(CustomError)
async def custom_exception_handler_a(request: Request, exc: CustomError):
    log.info(exc)
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.__dict__
    )

@app.on_event("startup")
def on_startup() -> None:
    try:
        log.info(
            r"""
             /$$$$$$$$                  /$$                                           
            |__  $$__/                 | $$                                           
               | $$  /$$$$$$   /$$$$$$$| $$   /$$                                     
               | $$ |____  $$ /$$_____/| $$  /$$/                                     
               | $$  /$$$$$$$|  $$$$$$ | $$$$$$/                                      
               | $$ /$$__  $$ \____  $$| $$_  $$                                      
               | $$|  $$$$$$$ /$$$$$$$/| $$ \  $$                                     
               |__/ \_______/|_______/ |__/  \__/                                     
                                                                                      
             /$$$$$$/$$$$   /$$$$$$  /$$$$$$$   /$$$$$$   /$$$$$$   /$$$$$$   /$$$$$$ 
            | $$_  $$_  $$ |____  $$| $$__  $$ |____  $$ /$$__  $$ /$$__  $$ /$$__  $$
            | $$ \ $$ \ $$  /$$$$$$$| $$  \ $$  /$$$$$$$| $$  \ $$| $$$$$$$$| $$  \__/
            | $$ | $$ | $$ /$$__  $$| $$  | $$ /$$__  $$| $$  | $$| $$_____/| $$      
            | $$ | $$ | $$|  $$$$$$$| $$  | $$|  $$$$$$$|  $$$$$$$|  $$$$$$$| $$      
            |__/ |__/ |__/ \_______/|__/  |__/ \_______/ \____  $$ \_______/|__/      
                                                         /$$  \ $$                    
                                                        |  $$$$$$/                    
                                                         \______/                     
            """
        )
    except Exception as e:
        log.error(f'❌ FastAPI start filed: {e}')
        raise Exception
