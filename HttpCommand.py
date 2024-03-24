class HttpCommand:
    def __init__(self, option) -> None:
        self.option = option
        self.url = None

    def check(self, command):
        command = command.split()
        if len(command) != 2:
            return False
        
        if command[0] != self.option:
            return False
        
        self.url = command[1]
        return True
    
    def response(self):
        return self.url
