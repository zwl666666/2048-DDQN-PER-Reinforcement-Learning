import numpy as np
import torch
import argparse
import sys
from numba import jit


@jit(nopython=True)
def to_power_two_matrix(matrix):
    """Transform matrix to a power 2 matrix. Maximum value: 65566"""
    power_matrix = np.zeros(
        shape=(1, matrix.shape[0], matrix.shape[1], 16), dtype=np.float32
    )
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if matrix[i][j] == 0:
                power_matrix[0][i][j][0] = 1.0
            else:
                power = int(np.log(matrix[i][j]) / np.log(2))
                power_matrix[0][i][j][power] = 1.0

    return power_matrix


def selection_action(eps_threshold, valid_movements, policy_net, state):
    sample = np.random.rand(1)

    if sample > eps_threshold:
        with torch.no_grad():
            labels = policy_net(state, 1)
            ordered = np.flip(np.argsort(labels), axis=1)[0]
            intersection = np.nonzero(np.in1d(ordered, valid_movements)[0])

            return ordered[intersection[0]]
    else:
        return np.random.choice(np.nonzero(valid_movements)[0])


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=10)
    parser.add_argument("--pretrain", type=int, default=100000)
    parser.add_argument("--batch_size", type=int, default=128)

    args = parser.parse_args()

    return args


def plot_info():
    pass
