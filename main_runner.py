import asyncio, logging, time
from backend.data_feed import DataFeed
from backend.strategy_engine import StrategyEngine
from backend.signal_manager import SignalManager
from backend.db_init import init

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger('main')

async def on_minute(datafeed, engine, signals_mgr):
    df = datafeed.get_all()
    for pair, candles in df.items():
        res = await engine.evaluate(pair, candles, datafeed)
        if res and res.get('fire'):
            s = res['signal']
            signals_mgr.save(s)
            LOG.info('Signal saved: %s', s)
            # attempt to resolve previous signal
            signals_mgr.resolve_recent(pair)

async def main():
    init()  # ensure DB
    datafeed = DataFeed(pairs=['EURUSD'])
    await datafeed.start()
    engine = StrategyEngine()
    signals_mgr = SignalManager()
    # minute loop
    try:
        while True:
            await asyncio.sleep(60 - (time.time() % 60))
            await on_minute(datafeed, engine, signals_mgr)
    except KeyboardInterrupt:
        await datafeed.stop()

if __name__=='__main__':
    asyncio.run(main())
