import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    return x * (1 - x)

inputs = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
outputs = np.array([[0], [1], [1], [0]])

np.random.seed(42)
input_layer_neurons = 2
hidden_layer_neurons = 4
output_neurons = 1

weights_input_hidden = np.random.uniform(size=(input_layer_neurons, hidden_layer_neurons))
weights_hidden_output = np.random.uniform(size=(hidden_layer_neurons, output_neurons))

lr = 0.5
epochs = 10000

for epoch in range(epochs):
    hidden_input = np.dot(inputs, weights_input_hidden)
    hidden_output = sigmoid(hidden_input)

    final_input = np.dot(hidden_output, weights_hidden_output)
    final_output = sigmoid(final_input)

    error = outputs - final_output
    d_output = error * sigmoid_derivative(final_output)

    error_hidden_layer = d_output.dot(weights_hidden_output.T)
    d_hidden_layer = error_hidden_layer * sigmoid_derivative(hidden_output)

    weights_hidden_output += hidden_output.T.dot(d_output) * lr
    weights_input_hidden += inputs.T.dot(d_hidden_layer) * lr

print("Final Output after Training:")
print(final_output)
