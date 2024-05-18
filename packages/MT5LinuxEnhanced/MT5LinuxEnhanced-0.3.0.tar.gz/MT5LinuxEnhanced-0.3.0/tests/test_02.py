from datetime import datetime

import pytz

from mt5linux import MetaTrader5

mt5 = MetaTrader5(port=8001)
mt5.initialize()
timezone = pytz.timezone("Etc/UTC")
start_date = datetime(2024, 5, 10, tzinfo=timezone)
end_date = datetime(2024, 5, 10, tzinfo=timezone)
print(mt5.terminal_info())
copy_ticks = mt5.copy_ticks_range("EURUSD", start_date, end_date, mt5.COPY_TICKS_ALL)
print(copy_ticks)
copy_rates = mt5.copy_rates_range("EURUSD", mt5.TIMEFRAME_M15, start_date, end_date)
print(copy_rates)
mt5.shutdown()
assert True