from matplotlib import pyplot as plt


def cost(weight, x_, y):
    s = 0
    for step in range(len(x_)):
        s += (weight * x_[step] - y[step]) ** 2

    return s / len(x_)


def gradients(weight, x_, y):
    n_x = []
    for step in range(len(x_)):
        n_x.append(weight * x_[step] - y[step])

    s = 0
    for step in range(len(x_)):
        s += n_x[step] * x_[step]

    return s / len(x_)


X = [1., 2., 3.]
Y = [1., 2., 3.]

W_val, cost_val = [], []
for i in range(-30, 51):
    W = i * 0.1
    c = cost(W, X, Y)
    # print('{:.1f}, {:.1f}'.format(W, c))

    W_val.append(W)
    cost_val.append(c)

plt.plot(W_val, cost_val, 'ro')
plt.ylabel('Cost')
plt.xlabel('W')
plt.show()

W = 100
# W = -100
for i in range(1000):
    c = cost(W, X, Y)
    g = gradients(W, X, Y)
    W = W - g * 0.01

    # cost 는 거리의 제곱을 취하기 때문에 W 가 음수이건 양수이건 상관없다.
    if c < 1.0e-15:
        break

    if i % 20 == 19:
        print('{:4} : {:17.12f} {:12.8f} {:12.8f}'.format(i+1, c, g, W))
