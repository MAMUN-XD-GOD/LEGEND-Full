import aiohttp, time
class Notifier:
    def __init__(self,cfg=None):
        self.cfg=cfg or {}; self.mode=self.cfg.get('mode','print'); self._last=0
        self.telegram_token=self.cfg.get('telegram_token'); self.telegram_chat=self.cfg.get('telegram_chat')
    async def publish(self,signal):
        now=time.time()
        if now-self._last<1: return
        self._last=now
        text=f"Signal: {signal['pair']} {signal['direction']} conf={signal.get('confidence')}"
        if self.mode=='print': print(text); return
        if self.mode=='telegram' and self.telegram_token and self.telegram_chat:
            url=f'https://api.telegram.org/bot{self.telegram_token}/sendMessage'
            async with aiohttp.ClientSession() as s:
                await s.post(url,json={'chat_id':self.telegram_chat,'text':text})
            return
        print(text)
