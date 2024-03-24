from HttpCommand import HttpCommand
from SearchCommand import SearchCommand
from HelpCommand import HelpCommand
from ExitCommand import ExitCommand

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
    g = Go2Web([HttpCommand('-u'),
                SearchCommand("-s"),
                HelpCommand('-h', f"""
                            go2web -u <URL>  # make an HTTP request to the specified URL and print the response
                            go2web -s <search-term> # make an HTTP request to search the term using your favorite search engine and print top 10 results
                            go2web -h               # show this help 
                            go2web -e # exit the program
                            """),
                            ExitCommand("-e")])
    print(g.run())