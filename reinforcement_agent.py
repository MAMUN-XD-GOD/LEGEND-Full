import numpy as np
from sklearn.ensemble import RandomForestRegressor
from backend.experience_replay import ReplayBuffer

class TimingAgent:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=16)
        self.replay = ReplayBuffer(capacity=10000)
        self._trained = False
    def featurize(self, state):
        # state: dict of recent features; flatten into vector
        return np.array([state.get(k,0) for k in sorted(state.keys())], dtype=float)
    def act(self, state):
        x = self.featurize(state).reshape(1,-1)
        if not self._trained:
            # random action: -1 (earlier), 0 (no shift), 1 (later)
            return np.random.choice([-1,0,1])
        pred = self.model.predict(x)[0]
        return int(np.sign(pred))
    def push_experience(self, state, action, reward, next_state, done):
        self.replay.push(state, action, reward, next_state, done)
    def train(self, batch_size=256):
        if len(self.replay) < 64:
            return False
        samples = self.replay.sample(batch_size)
        X=[]; y=[]
        for s,a,r,ns,d in samples:
            X.append(self.featurize(s))
            y.append(r)
        self.model.fit(np.array(X), np.array(y))
        self._trained = True
        return True
