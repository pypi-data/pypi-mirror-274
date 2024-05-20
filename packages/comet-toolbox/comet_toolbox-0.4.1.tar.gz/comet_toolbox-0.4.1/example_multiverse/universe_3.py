import numpy as np
import bct
import comet

print(f"Decision 1: 1")

    
# Load example data and calculate dFC + local efficiency
ts = comet.data.load_example()
dfc = comet.methods.SlidingWindow(ts, **{'windowsize': 45, 'shape': 'rectangular', 'std': 10.0, 'diagonal': 0, 'standardize': False, 'fisher_z': False, 'tril': False}).connectivity()
dfc = dfc[0] if isinstance(dfc, tuple) else dfc #required as LeiDA returns multiple outputs
    
W = dfc[:,:,100]
W_t = comet.graph.threshold(W, **{'type': 'density', 'threshold': 0.0, 'density': 0.5})