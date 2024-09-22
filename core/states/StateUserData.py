from aiogram.fsm.state import State, StatesGroup

class StateUserData(StatesGroup):
    USER_DATA = State()
    USER_SIGNATURE = State()
    USER_BIO = State()