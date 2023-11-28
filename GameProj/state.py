class State :
    def __init__(self):
        """
        Инициализирует объект State.
        """
        self.states = {}
        self.state = None

    def set_state(self, state):
        """
        Устанавливает текущее состояние.

        :param state: Состояние для установки.
        """
        if state in self.states:
            self.state = state

    def run_state(self):
        """
         Запускает текущее состояние, если оно установлено.
        """
        if self.state is not None:
            self.states[self.state]()