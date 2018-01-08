from math import exp;
from random import random, seed, shuffle;
import csv;

class NeuralNet (object):

	__network = None;
	__inputs = None;
	__hidden = None;
	__oupputs = None;

	# Calculate neuron activation for an input
	def __activate (self, neuron, inputs):
		activation = neuron["bias"];
		for i in range(len(neuron["weights"])):
			activation += neuron["weights"][i] * inputs[i];
		return activation;

	# Backpropagate error and store in neurons
	def __backward_progragate_error (self, expected):
		for i in reversed(range(len(self.__network))):
			layer = self.__network[i];
			errors = list();
			if (i != len(self.__network)-1):
				for j in range(len(layer)):
					error = 0.0;
					for neuron in self.__network[i + 1]:
						error += (neuron["weights"][j] * neuron["delta"]);
					errors.append(error);
			else:
				for j in range(len(layer)):
					neuron = layer[j];
					errors.append(expected[j] - neuron["output"]);
			for j in range(len(layer)):
				neuron = layer[j];
				neuron["delta"] = errors[j] * self.__transfer_derivative(neuron["output"]);

	# Forward propagate input to a network output
	def __forward_propagate (self, row):
		current_row = row;
		for layer in self.__network:
			next_row = [];
			for neuron in layer:
				activation = self.__activate (neuron, current_row);
				neuron["output"] = self.__transfer(activation);
				next_row.append(neuron["output"]);
			current_row = next_row;
		return current_row;

	# Constructor
	def __init__ (self, n_inputs=0, n_hidden=0, n_outputs=0):
		seed(1);
		self.__inputs = n_inputs;
		self.__hidden = n_hidden;
		self.__outputs = n_outputs;
		self.__network = list();
		hidden_layer = [{"weights":[random() for i in range(n_inputs)],"bias":random()} for j in range(n_hidden)];
		self.__network.append(hidden_layer);
		output_layer = [{"weights":[random() for i in range(n_hidden)],"bias":random()} for j in range(n_outputs)];
		self.__network.append(output_layer);

	# Transfer neuron activation
	def __transfer (self, activation):
		return (1.0/(1.0 + exp(-activation)));

	# Calculate the derivative of a neuron ouput
	def __transfer_derivative (self, output):
		return (output * (1.0 - output));

	# Update network weights with error
	def __update_weights (self, row, l_rate):
		for i in range (len(self.__network)):
			inputs = row[:-1];
			if i != 0:
				inputs = [neuron["output"] for neuron in self.__network[i - 1]];
			for neuron in self.__network[i]:
				for j in range (len(inputs)):
					neuron["weights"][j] += l_rate * neuron["delta"] * inputs[j];
				neuron["bias"] += l_rate * neuron["delta"];

	# Get normalised, randomised train and test data (tuple)
	def get_datasets (self, filename, offset=0):

		# Declare empty lists for datasets
		dataset = [];
		dataset_normalised = [];

		# Read file and populate datasets
		with open (filename) as csvfile:
			reader = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC);
			for row in reader:
				if not row:
					continue;
				dataset.append(row);

		max_params = list();

		for i in range(len(dataset[0])-1):
			max_params.append(max([dataset[x][i] for x in range(len(dataset))]));

		# Normalise each column
		for row in dataset:
			dataset_normalised.append ([row[i]/max_params[i] for i in range(len(row)-1)]);
			dataset_normalised[-1].append(int(row[-1])-offset);

		shuffle(dataset_normalised);
		train_range = int(8*len(dataset_normalised)/10);

		# Train:Test split 80:20
		return (dataset_normalised[:train_range], dataset_normalised[train_range:]);

	# Return number of neurons in the hidden layer
	def get_hidden_count (self):
		return self.__hidden;

	# Return number of neurons in the input layer
	def get_inputs_count (self):
		return self.__inputs;

	# Return network object
	def get_network (self):
		return self.__network;

	# Return number of neurons in the output layer
	def get_outputs_count (self):
		return self.__outputs;

	# Make a prediction with the network
	def predict (self, row):
		outputs = self.__forward_propagate (row);
		return outputs.index(max(outputs));

	# Set the weights and biases
	def set_network (self, net):
		self.__inputs = len(net[0][0]["weights"]);
		self.__hidden = len(net[1][0]["weights"]);
		self.__outputs = len(net[1]);
		self.__network = list();
		for layer in net:
			self.__network.append(layer);

	# Train the network for a fixed number of epochs
	def train_network (self, train, l_rate, n_epoch, echo=False):
		for epoch in range (n_epoch):
			sum_error = 0;
			for row in train:
				outputs = self.__forward_propagate (row);
				expected = [0 for i in range(self.__outputs)];
				expected[row[-1]] = 1;
				sum_error += sum([(expected[i] - outputs[i])**2 for i in range(len(expected))]);
				self.__backward_progragate_error (expected);
				self.__update_weights (row, l_rate);
			if echo:
				print (">epoch={:d}, lrate={:.3f}, error={:.3f}".format(epoch, l_rate, sum_error));
