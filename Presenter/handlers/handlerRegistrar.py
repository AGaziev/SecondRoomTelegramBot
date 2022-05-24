from Presenter.handlers.admin import registerHandlers as adminRegister
from Presenter.handlers.client import registerHandlers as clientRegister


def handlerRegistrate(dp):
    adminRegister(dp)
    clientRegister(dp)
