import random
import sys
import json
import asyncio
import websockets
import os
from mapa import Map
from pacmanTreeSearch import *


async def agent_loop(server_address = "localhost:8000", agent_name="student"):
    async with websockets.connect("ws://{}/player".format(server_address)) as websocket:

        # Receive information about static game properties 
        await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))
        msg = await websocket.recv()
        game_properties = json.loads(msg) 
         
        mapa = Map(game_properties['map'])


        #init agent properties
        acts = []
        currentlives = 99

        while True: 
            r = await websocket.recv()
            state = json.loads(r) #receive game state

            if not state['lives']:
                print("GAME OVER")
                return



            #You recalculate if:
            #   -You die (lives decrement)
            #   -Ghost gets on your path    (WIP!!!)
            #   -Run out of acts
            if not acts or state['lives'] < currentlives:

                print("----------START SEARCH-----------")
                cur_x, cur_y = state['pacman']

                closest = list(state['energy'] + state['boost'])

                target_x, target_y = min(closest,key=lambda p: abs(cur_x - p[0]) + abs(cur_y - p[1]))
                d = PacDomain(mapa,state)
                f = formulatePacman(d,state['pacman'], (target_x, target_y))
                t = solvePacman(f,'astar')

                acts = t[1]
                coords = t[0]

                print("----------CONCLUDED SEARCH-----------")
                print("Output:")
                print(acts)
                print(t[0])


            key = acts.pop(0)


            await websocket.send(json.dumps({"cmd": "key", "key": key}))

            currentlives = state['lives']


loop = asyncio.get_event_loop()
SERVER = os.environ.get('SERVER', 'localhost')
PORT = os.environ.get('PORT', '8000')
NAME = os.environ.get('NAME', 'student')
loop.run_until_complete(agent_loop("{}:{}".format(SERVER,PORT), NAME))

