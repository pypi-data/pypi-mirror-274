import logging

from examon_core.protocols.multi_choice_protocol import MultiChoiceProtocol


class MultiChoiceFactory(MultiChoiceProtocol):
    def __init__(self, correct_answer, choice_list=None) -> None:
        self.correct_answer = correct_answer
        self.choice_list = choice_list

    def build(self):
        if self.correct_answer not in self.choice_list:
            self.choice_list.append(self.correct_answer)
        logging.debug(f"MultiChoiceFactory.build: {self.choice_list}")
        return self.choice_list
