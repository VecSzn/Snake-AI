import tensorflow as tf
import numpy as np


class Agent:
    def __init__(self, epsilon=1, gamma=0.9):
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_net = self.create_model()
        self.target_net = self.create_model()
        self.optimizer = tf.keras.optimizers.Adam(learning_rate=0.01)
        self.buffer = []

    def create_model(self):
        model = tf.keras.models.Sequential()
        model.add(tf.keras.layers.Input(shape=(8)))
        model.add(tf.keras.layers.Dense(64, activation="relu"))
        model.add(tf.keras.layers.Dense(64, activation="relu"))
        model.add(tf.keras.layers.Dense(4, activation="softmax"))

        return model

    def get_action(self, state):
        if np.random.random() < self.epsilon:
            return np.random.randint(0, 3)
        else:
            q_values = self.q_net(np.array([state]))[0]
            return np.argmax(q_values)

    def train(self, batch):
        state, action, reward, next_state = batch
        targets = []
        for i in range(len(action)):
            if reward[i] == -1:
                target = reward[i]
            else:
                target = reward[i] + self.gamma * np.max(
                    self.target_net(np.array([next_state[i]]))
                )
            targets.append(target)

        with tf.GradientTape() as tape:
            q_values = tf.gather(self.q_net(state), action, batch_dims=1)
            loss = tf.keras.losses.MSE(targets, q_values)

        grads = tape.gradient(loss, self.q_net.trainable_variables)
        self.optimizer.apply_gradients(zip(grads, self.q_net.trainable_variables))

        self.epsilon *= 0.999

    def set_weights(self):
        self.target_net.set_weights(self.q_net.get_weights())

    def add(self, state, action, reward, next_state):
        self.buffer.append([state, action, reward, next_state])

    def batching(self, batch_size):
        shuffle = self.buffer
        np.random.shuffle(shuffle)
        sample = list(map(tf.constant, zip(*shuffle[:batch_size])))
        return sample
