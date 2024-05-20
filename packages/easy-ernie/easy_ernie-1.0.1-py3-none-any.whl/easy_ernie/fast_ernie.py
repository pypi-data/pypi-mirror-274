from typing import Generator
from . import ernie, model

class FastErnie:
    def __init__(self, BAIDUID: str, BDUSS_BFESS: str):
        self.ernie = ernie.Ernie(BAIDUID, BDUSS_BFESS)
        self.sessionId = ''
        self.sessionName = ''
        self.parentChatId = '0'

    def askStream(self, question: str, botModel: model.BotModel=model.BotModel.EB3_5) -> Generator[model.AskStreamResponse, None, None]:
        if not self.sessionId:
            self.sessionName = question
        for data in self.ernie.askStream(question, sessionId=self.sessionId, sessionName=self.sessionName, parentChatId=self.parentChatId, botModel=botModel):
            yield data
        self.sessionId = data.sessionId
        self.parentChatId = data.botChatId

    def ask(self, question: str, botModel: model.BotModel=model.BotModel.EB3_5) -> model.AskResponse:
        data = list(self.askStream(question, botModel=botModel))
        doneData = data[-1]
        return model.AskResponse(answer=doneData.answer, sessionId=doneData.sessionId, botChatId=doneData.botChatId)

    def close(self) -> bool:
        if self.ernie.deleteSession(self.sessionId):
            self.sessionId = ''
            self.sessionName = ''
            self.parentChatId = '0'
            return True
        return False