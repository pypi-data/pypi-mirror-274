from .ArchFlow import ArchFlow


class ArchFlowCli(ArchFlow):

    def teste(self, arg):
        print(arg)

    def functions_flow(self) -> dict:
        return {
            "teste": self.teste
        }