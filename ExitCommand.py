from sys import exit
class ExitCommand:
    def __init__(self, option) -> None:
        self.option = option

    def check(self, command):
        command = command.split()
        if len(command) != 1:
            return False
        
        if command[0] != self.option:
            return False

        return True
    
    def response(self):
        exit(0)