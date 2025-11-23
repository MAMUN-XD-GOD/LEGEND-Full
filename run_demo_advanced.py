import json, random, time
from backend.liquidity_heatmap import compute_heatmap, plot_heatmap
from backend.orderflow_emulator import emulate_orderflow
from backend.experience_replay import ReplayBuffer
from backend.reinforcement_agent import TimingAgent

# generate synthetic candles
candles = []
price = 1.0800
for i in range(500):
    o = price
    move = random.uniform(-0.0006,0.0006)
    c = round(o + move,5)
    h = round(max(o,c) + random.uniform(0,0.0003),5)
    l = round(min(o,c) - random.uniform(0,0.0003),5)
    vol = random.randint(1,200)
    candles.append({'ts':int(time.time())+i*60,'open':o,'high':h,'low':l,'close':c,'volume':vol})
    price = c

levels = compute_heatmap(candles, precision=0.0001, window=300)
print('Top liquidity levels:', sorted(levels.items(), key=lambda x:-x[1])[:5])
print('Orderflow:', emulate_orderflow(candles[-50:]))

agent = TimingAgent()
# push some random experiences
for i in range(200):
    state = {'s'+str(j):random.random() for j in range(6)}
    action = random.choice([-1,0,1])
    reward = random.uniform(-1,1)
    next_state = {'s'+str(j):random.random() for j in range(6)}
    agent.push_experience(state, action, reward, next_state, False)
print('Replay size:', len(agent.replay))
trained = agent.train()
print('Agent trained?', trained)
