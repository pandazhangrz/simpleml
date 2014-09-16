'''
Example of how to use Decision Trees and Random Forests.
'''
import sys, os, time

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# %cd C:/Users/g1rxf01/Downloads/New folder/simpleml/examples
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from simpleml.perceptron import MultilayerPerceptron


np.random.seed(2345)
num_obs = 500

x = np.random.normal(size=(num_obs, 2))
e = np.random.normal(1, size=num_obs)

# # Linear boundary with kink
# y = np.logical_and(np.dot(x, [ 2,-3])+e < 4,
#                    np.dot(x, [-3,-1])+e < 3).astype(int)

# Sinusoidal boundary
y = (x[:,1]+e*.8 < .8+np.sin((x[:,0])*3)).astype(int)


x0_min, x1_min = np.min(x, axis=0)
x0_max, x1_max = np.max(x, axis=0)

x0, x1 = np.meshgrid(np.linspace(x0_min, x0_max, 500),
                     np.linspace(x1_min, x1_max, 500))
x_flatmesh = np.column_stack([x0.ravel(), x1.ravel()])

mlp = MultilayerPerceptron(
    num_inputs=3, num_outputs=1, num_hidden_layers=1, num_hidden_nodes=6,
    learn_rate=.5, momentum=.1, seed=23456
)

start = time.perf_counter()
with PdfPages('example.pdf') as pdf:
    for i in range(0, 20):
        mlp.fit(x, y, epochnum=10, add_constant=True, verbose=True)
        Z = mlp.classify(x_flatmesh, add_constant=True)
        Z = Z.reshape(x0.shape)

        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)

        ax.contour(x0, x1, Z, cmap=plt.cm.Paired)
        ax.scatter(x[:,0], x[:,1], c=y, cmap=plt.cm.Paired)

        pdf.savefig(fig)
        plt.close(fig)

        if i % 5 == 4:
            print(i+1)
print('Time elapsed: {:6.3f}'.format(time.perf_counter() - start))
