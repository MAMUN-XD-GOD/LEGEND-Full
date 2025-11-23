
// This frontend expects a websocket at /ws/signals that pushes JSON signals and candles.
// Integrate lightweight-charts or Chart.js for candle rendering. Below is a simple live queue.
let queue = document.getElementById('queue');
let ws = new WebSocket((location.protocol==='https:'?'wss://':'ws://') + location.host + '/ws/signals');
ws.onopen = ()=>{console.log('ws open')};
ws.onmessage = (ev)=>{try{const msg=JSON.parse(ev.data); if(msg.type==='signal'){const li=document.createElement('li'); li.textContent=`${msg.signal.pair} ${msg.signal.direction} conf=${msg.signal.confidence}`; queue.prepend(li);} }catch(e){}}
