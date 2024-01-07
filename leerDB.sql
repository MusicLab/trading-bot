select * from klines

select timestamp, origen, estado , tipo, close from ordenes
where origen == "klines1MINUTE"

select timestamp, origen, estado , tipo, close from ordenes
where origen == "klines15MINUTE"

select timestamp, origen, estado , tipo, close from ordenes
where origen == "klines1HOUR"