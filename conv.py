import torch
import numpy as np
import matplotlib.pyplot as plt

class Conv2D():
    def __init__(self, channels, kernel_size, stride=1, padding=None):
        ''' Parameters of Convolution
        channels: channels of input (binary image has 1, RGB something else)
        kernel_size: dimension of weights
        stride: jumping, use 1
        padding: adding zeros to borders of image, recompute for original image size '''
        self.kernel_size = 26
        self.kernel = torch.zeros(3, 26, 26)

    def set_weights(self, weights=None, bias=None):
        ''' For reassigning learned weights and bias for testing '''
        self.kernel = weights

    def forward(self, x):
        ''' FeedForward pass'''
        feature_map = torch.zeros(200, 200)

        x_pad = torch.cat(
            (torch.zeros(3, len(x[0]), self.kernel_size // 2), x, torch.zeros(3, len(x[0]), self.kernel_size // 2)), 2)
        x_pad = torch.cat((torch.zeros(3, self.kernel_size // 2, len(x_pad[0][0])), x_pad,
                           torch.zeros(3, self.kernel_size // 2, len(x_pad[0][0]))), 1)
        for r in range(len(x_pad[0])):
            if self.kernel_size + r >= len(x_pad[0]):
                break
            for c in range(len(x_pad[0][0])):
                if self.kernel_size + c >= len(x_pad[0][0]):
                    break
                x = torch.mul(x_pad[:, r:self.kernel_size + r, c:self.kernel_size + c], self.kernel)
                feature_map[r][c] = torch.sum(x)
        return feature_map
    def check_output_shape(self, *args):
        pass

if __name__ == '__main__':
    print("Evaluation script will perform followings steps ...")
    conv = Conv2D()

    stored_weights = torch.load('hw2_weights.pt') # upload as well!!!
    # torch.save(weights, path) for storing the weights

    conv.set_weights(stored_weights)

    output = conv.forward(x=x_test)    # x_test is different from provided image ...

    # Maximum of tensor "output" will be taken as a final position
    # You can reconstruct these step with data provided.
