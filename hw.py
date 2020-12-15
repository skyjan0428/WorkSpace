import tensorflow as tf
import numpy as np

def add_layer(inputs, input_size, output_size, activation_function=None):
    
    Weights = tf.Variable(tf.random_normal([input_size, output_size]))
    threshold = tf.Variable(tf.zeros([1, output_size]) + 0.1)
    Wx_plus_b = tf.matmul(inputs, Weights) + threshold

    if activation_function is None:
        outputs = Wx_plus_b
    else:
        outputs = activation_function(Wx_plus_b)
    return outputs

inputSize = 10
hiddenSize = 10
dataVolume = 10


x_data = 2 * np.random.random_sample((dataVolume, inputSize)) -1
y_data = np.random.rand() 

hiddenLayer = add_layer(tf.placeholder(tf.float32, [dataVolume, inputSize]), inputSize, hiddenSize, activation_function = tf.tanh)
outputLayer = add_layer(hiddenLayer, hiddenSize, 1, activation_function = None)

initinitializer = tf.global_variables_initializer()

errors = tf.reduce_mean(tf.reduce_sum(tf.square(tf.placeholder(tf.float32)  - outputLayer), reduction_indices=[1]))

train = tf.train.GradientDescentOptimizer(0.05).minimize(errors)

sess = tf.Session()

sess.run(init)

for i in range(500):
    # training
    print("x:",x_data)
    print("y:",y_data)
    
    sess.run(train, feed_dict={xs: x_data, yc: y_data})

sess.close()