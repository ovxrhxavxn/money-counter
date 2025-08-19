from aiogram.fsm.state import State, StatesGroup


class UseModelStates(StatesGroup):
    use_yolo8s = State()
    use_yolo8m = State()
    use_yolo8n = State()