import tensorflow as tf
import numpy as np


class Agent:
    def __init__(self, width, height, epsilon=1, gamma=0.9):
        self.width = width
        self.height = height
        self.gamma = gamma
        self.epsilon = epsilon
        self.model = self.create_model()

    def create_model(self):
        model = tf.keras.models.Sequential()
        model.add(tf.keras.layers.Input(shape=(self.height, self.width, 1)))
        model.add(tf.keras.layers.Conv2D(32, (5, 5), activation="relu"))
        model.add(tf.keras.layers.MaxPooling2D((2, 2)))
        model.add(tf.keras.layers.Conv2D(32, (3, 3), activation="relu"))
        model.add(tf.keras.layers.Flatten())
        model.add(tf.keras.layers.Dense(64, activation="relu"))
        model.add(tf.keras.layers.Dense(4, activation="softmax"))

        model.compile(loss=tf.keras.losses.MSE, optimizer="adam")
        return model

    def get_action(self, state):
        if np.random.random() < self.epsilon:
            return np.random.randint(0, 4)
        else:
            q_values = self.model.predict(np.array([state]))[0]
            return np.argmax(q_values)

    def train(self, batches):
        for batch in batches:
            targets = []
            states = []
            for state, action, reward, next_state in batch:
                pred = self.model.predict(np.array([state]))
                target = reward + self.gamma * np.amax(
                    self.model.predict(np.array([next_state]))
                )
                pred[0][action] = target
                targets.append(pred)
                states.append(state)

            states = np.array(states)
            targets = np.array(targets)
            self.model.fit(states, targets, epochs=1)


class ReplayBuffer:
    def __init__(self):
        self.buffer = []

    def add(self, state, action, reward, next_state):
        self.buffer.append([state, action, reward, next_state])

    def batching(self, batch_size):
        shuffle = self.buffer[:]
        np.random.shuffle(shuffle)
        batches = []
        for i in range(0, len(shuffle), batch_size):
            batches.append(shuffle[i : i + batch_size])

        return batches
