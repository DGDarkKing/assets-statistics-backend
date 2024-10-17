import uvicorn
from fastapi import FastAPI

from routes.statistics import router as statistic_router
from routes.transactoins import router as transaction_router
from settings import app_settings

app = FastAPI(
    title='Monolithe static service',
    debug=app_settings.debug
)

app.include_router(transaction_router)
app.include_router(statistic_router)

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='127.0.0.1',
        port=8000,
        reload=True
    )
