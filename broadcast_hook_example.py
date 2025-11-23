# Example: after generating a signal, broadcast to pro_broadcaster
from backend.pro_broadcaster import broadcast

def notify(signal):
    import asyncio
    asyncio.create_task(broadcast({'type':'signal','signal':signal}))
