from .abstract import SelectionPolicy


class SelectionPolicyAll(SelectionPolicy):
    @staticmethod
    def message_selected(possible_message):
        return True
