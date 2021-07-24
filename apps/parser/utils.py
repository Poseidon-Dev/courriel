import asyncio
from typing import AnyStr

def binary_pickle(cls):
    """
    Converts a class instance into a Binary pickle for postgres storage
    """
    from pickle import dumps
    from psycopg2 import Binary
    return Binary(dumps(cls)) 

def check_domain(email):
    """
    Checks that the domain is within the list of accepted domain
    """
    from config import ACCEPTED_DOMAIN
    email = email.split('@')
    if email[1] in ACCEPTED_DOMAIN:
        return email[0].lower()
    else:
        return None

# class Loop:
    
#     def __init__(self, looper, wait=0):
#         self.looper = looper
#         self.wait = asyncio.sleep(wait)
#         self.loop = asyncio.get_event_loop()
#         self.loop.call_later(5, self.stop)
#         self.task = self.loop.create_task(self.run())

#         try:
#             self.loop.run_until_complete(self.task)
#         except asyncio.CancelledError:
#             pass

#     def stop(self):
#         self.task.cancel()

#     async def run(self):
#         while True:
#             print('start')
#             self.looper
#             await self.wait
#             print('stop')
    
# class Loop:
#     def __init__(self, looper, wait=0):
#         self.looper = looper
#         self.loop = asyncio.get_event_loop()
#         self.wait = wait

#     async def loop(self):
#         print(self.looper)
#         await asyncio.sleep(self.wait)

class Loop:
    def __init__(self, looper, wait=0):
        self.looper = looper()
        self.wait = wait
        self.loop=asyncio.get_event_loop()

    async def run(self):
        while True:
            self.looper.run()
            await asyncio.sleep(self.wait)


