import numpy as np

import simpleml.dectree as dt


X_TRAIN = np.array([
    [-1.4273, -1.0824,  0.0058],
    [ 0.7866, -0.3452, -0.5211],
    [ 1.1191,  0.0517, -1.1401],
    [ 1.6514,  0.2658,  0.4943],
    [ 0.3742, -0.9247,  0.1196],
    [-0.5938, -0.9151, -0.2263],
    [ 1.0806, -0.5539, -1.9748],
    [-0.2261,  0.228 ,  0.5221],
    [ 1.0467,  0.9656,  0.4729],
    [-1.327 , -0.7972, -1.4782],
    [ 0.6219, -0.0472, -1.178 ],
    [ 0.4702,  0.16  , -0.111 ],
    [-0.7008, -0.586 , -1.2022],
    [-0.0925,  0.5194,  1.7272],
    [ 1.6551, -0.3479, -2.0299],
    [-1.0322, -0.6711, -1.476 ],
    [ 0.6841, -1.2086, -1.6619],
    [ 0.3332, -1.8284, -0.291 ],
    [-1.8365,  1.2062, -0.888 ],
    [-0.2278, -1.2292,  1.5369]
])

LABELS_TRAIN = np.array(
    [1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0]
)

X_TEST = np.array([
    [-0.4278, -0.9836, -0.0415],
    [-0.6813, -0.1991, -2.1691],
    [-1.5937, -0.9405, -1.6823],
    [ 1.8772,  1.0064,  0.0475],
    [ 0.736 ,  1.0728, -0.506 ],
    [-0.3631, -0.6367,  0.7501],
    [ 1.6533,  0.3377, -0.6203],
    [ 0.1004,  0.522 ,  0.131 ],
    [-1.1707,  2.5464,  0.4533],
    [ 0.6375, -1.2981,  0.2451],
    [ 0.1535,  0.8227,  0.9552],
    [ 0.6844, -0.468 , -0.989 ],
    [ 0.893 ,  2.8725,  0.5143],
    [ 0.2305,  0.5278,  0.2616],
    [ 0.7665, -0.4036,  0.8091],
    [ 0.0776,  0.5119,  0.1585],
    [-0.095 ,  1.2517,  0.3549],
    [-0.0125,  0.6841,  2.038 ],
    [-1.5437, -1.225 ,  0.1346],
    [ 0.4143,  0.2247, -0.0301]
])

LABELS_TEST = np.array(
    [1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1]
)

LABELS_TRAIN_BOOL = (LABELS_TRAIN == 1)
LABELS_TEST_BOOL = (LABELS_TEST == 1)


class TestEasyNode:
    labels_train = LABELS_TRAIN

    def setup(self):
        self.x =  X_TRAIN.copy()
        self.x[:,2] = np.abs(self.x[:,2]) * (-1+2*self.labels_train)

    def test_first_split(self):
        tree = dt._create_decision_node(self.x, self.labels_train)

        x_sorted = np.sort(self.x[:,2])
        zero_ind = np.searchsorted(x_sorted, 0)

        assert tree.split[0] == 2
        assert (tree.split[1] == x_sorted[zero_ind] or
                tree.split[1] == x_sorted[zero_ind-1])

    def test_create_tree(self):
        tree = dt._create_decision_node(self.x, self.labels_train)
        assert(tree.split[0] == 2)

        for i in range(2):
            assert tree.children[i].majority == i
            assert tree.children[1].split is None

    def test_tree_max_depth(self):
        tree = dt._create_decision_node(self.x, self.labels_train, max_depth=0)
        assert tree.split is None

    def test_num_nodes(self):
        tree = dt._create_decision_node(self.x, self.labels_train)
        assert tree.num_nodes() == 3

    def test_num_nodes1(self):
        tree = dt._create_decision_node(self.x, self.labels_train, max_depth=0)
        assert tree.num_nodes() == 1

    def test_descendents(self):
        tree = dt._create_decision_node(self.x, self.labels_train)
        assert len(tree.descendents()) == 3
        assert tree in tree.descendents()
        for i in range(2):
            assert tree.children[i] in tree.descendents()

    def test__data_at_node(self):
        tree = dt._create_decision_node(self.x, self.labels_train)
        assert np.all(
            self.x[self.x[:,2] < 0] == dt._data_at_node(tree, tree.children[0],
                                                       self.x)
        )
        assert np.all(
            self.x[self.x[:,2] > 0] == dt._data_at_node(tree, tree.children[1],
                                                       self.x)
        )

    def test_classify(self):
        tree = dt._create_decision_node(self.x, self.labels_train)
        for obs, label in zip(self.x, self.labels_train):
            assert tree.classify_obs(obs) == label

    def test_stumps(self):
        tree = dt._create_decision_node(self.x, self.labels_train)
        assert(len(tree.stumps()) == 1)
        assert(tree.stumps()[0] is tree)

    def test_stumps_nodepth(self):
        tree = dt._create_decision_node(self.x, self.labels_train, max_depth=0)
        assert(len(tree.stumps()) == 0)

class TestEasyNodeBin(TestEasyNode):
    def setup(self):
        self.x =  X_TRAIN.copy()
        self.x[:,2] = -0.5 + self.labels_train

class TestEasyNodeCat(TestEasyNode):
    def setup(self):
        self.x =  X_TRAIN.copy()
        self.x[:,2] = (-0.5 + self.labels_train +
                       np.logical_and(self.labels_train, self.x[:,2] > 0))


class TestNode:
    labels_train = LABELS_TRAIN

    def test_tree_print(self):
        tree = dt._create_decision_node(X_TRAIN, self.labels_train)
        print(tree)

    def test_stumps(self):
        tree = dt._create_decision_node(X_TRAIN, self.labels_train)
        for stump in tree.stumps():
            for i in range(2):
                assert(stump.children[i].split is None)

    def test_min_obs_split(self):
        min_obs = 5
        tree = dt._create_decision_node(X_TRAIN, self.labels_train,
                                        min_obs_split=min_obs)
        for desc in tree.descendents():
            if len(dt._data_at_node(tree, desc, X_TRAIN)) < min_obs:
                assert desc.split is None

    def test_classify(self):
        tree = dt._create_decision_node(X_TRAIN, self.labels_train)
        for obs, label in zip(X_TRAIN, self.labels_train):
            assert tree.classify_obs(obs) == label

    def test_num_nodes_min_split(self):
        tree_minobs0  = dt._create_decision_node(X_TRAIN, self.labels_train)
        tree_minobs10 = dt._create_decision_node(X_TRAIN, self.labels_train,
                                                 min_obs_split=10)
        assert tree_minobs0.num_nodes() > tree_minobs10.num_nodes()


def use_bool_labels(cls):
    class newclass(cls):
        labels_train = LABELS_TRAIN_BOOL
        labels_test = LABELS_TEST_BOOL
    newclass.__name__ = cls.__name__ + 'Bool'
    return newclass

TestEasyNodeBool = use_bool_labels(TestEasyNode)
TestEasyNodeBinBool = use_bool_labels(TestEasyNodeBin)
TestNodeBool = use_bool_labels(TestNode)
