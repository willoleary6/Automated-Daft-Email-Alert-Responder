class BasicObject():

    def __init__(self, operand_one, operand_two):
        self._operand_one = operand_one
        self._operand_two = operand_two
        self._result = 0

    def get_result(self):
        return self._result

    def multiply_operands(self):
        self._result = self._operand_one * self._operand_two

    def divide_operands(self):
        self._result = self._operand_one / self._operand_two

    def add_operands(self):
        self._result = self._operand_one + self._operand_two


#if __name__ == '__main__':
    #class_to_be_tested = ClassToBeTested(1,2)