from flask import Flask,request,Response
from botbuilder.core import BotFrameworkAdapter,BotFrameworkAdapterSettings,TurnContext,ConversationState,MemoryStorage
from botbuilder.schema import Activity
import asyncio
from pic_button import SampleAnimationCard


app = Flask(__name__)
loop = asyncio.get_event_loop()

#botsettings = BotFrameworkAdapterSettings("","")
botsettings = BotFrameworkAdapterSettings("679559fc-0375-4fe3-9d1f-941b9a922812","4645cd20-fdc0-4689-b507-aab26a91725d")
botadapter = BotFrameworkAdapter(botsettings)

CONMEMORY = ConversationState(MemoryStorage())
botdialog = SampleAnimationCard()


@app.route("/api/messages",methods=["POST"])
def messages():
    if "application/json" in request.headers["content-type"]:
        body = request.json
    else:
        return Response(status = 415)

    activity = Activity().deserialize(body)

    auth_header = (request.headers["Authorization"] if "Authorization" in request.headers else "")

    async def call_fun(turncontext):
        await botdialog.on_turn(turncontext)

    task = loop.create_task(
        botadapter.process_activity(activity,auth_header,call_fun)
        )
    loop.run_until_complete(task)


if __name__ == '__main__':
    app.run('localhost',3978)
