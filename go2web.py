from HttpCommand import HttpCommand

class Go2Web:
    def __init__(self, commands_list) -> None:
        self.commands_list = commands_list
    
    def getCommand(self):
        return str(input("go2web "))
    
    def handleCommand(self, command):
        for command_checker in self.commands_list:
            if command_checker.check(command):
                return command_checker.response()

    def run(self):
        while True:
            command = self.getCommand()
            response = self.handleCommand(command)
            print(response)

if __name__ == "__main__":
    g = Go2Web([HttpCommand('-u')])
    print(g.run())