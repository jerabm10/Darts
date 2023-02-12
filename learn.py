import torch
import numpy as np
import matplotlib.pyplot as plt


KERNEL_SIZE = 26
LEARNING_RATE = 0.005
ITERATIONS = 16
img = torch.from_numpy(np.load('utek.npy')).permute(2,0,1)
label = torch.from_numpy(np.load('label.npy'))
kernel = torch.rand(3, KERNEL_SIZE, KERNEL_SIZE, requires_grad=True)

img_pad = torch.cat((torch.zeros(3, len(img[0]), KERNEL_SIZE//2), img, torch.zeros(3, len(img[0]), KERNEL_SIZE//2)), 2)
img_pad = torch.cat((torch.zeros(3, KERNEL_SIZE//2, len(img_pad[0][0])), img_pad, torch.zeros(3,KERNEL_SIZE//2, len(img_pad[0][0]))), 1)

#kernel = torch.load('hw2_weights.pt')
optimizer = torch.optim.SGD([kernel], lr=LEARNING_RATE, momentum=0)
for i in range(ITERATIONS):
    feature_map = torch.zeros(200, 200)
    for r in range(len(img_pad[0])):
        if KERNEL_SIZE + r >= len(img_pad[0]):
            break
        for c in range(len(img_pad[0][0])):
            if KERNEL_SIZE + c >= len(img_pad[0][0]):
                break
            x = torch.mul(img_pad[:, r:KERNEL_SIZE + r, c:KERNEL_SIZE + c], kernel)
            feature_map[r][c] = torch.sum(x)

    feature_map = feature_map/torch.max(feature_map)
    loss = torch.sum((feature_map - 100*label)**4)
    print(loss)
    loss.backward()
    plt.imshow(feature_map.detach().numpy())
    plt.show()
    plt.pause(0.1)
    optimizer.step()
    optimizer.zero_grad()
    torch.save(kernel, 'hw2_weights.pt')
