class HelpCommand:
    def __init__(self, option, help) -> None:
        self.option = option
        self.help = help

    def check(self, command):
        command = command.split()
        if len(command) != 1:
            return False
        
        if command[0] != self.option:
            return False

        return True
    
    def response(self):
        return self.help