from tqdm import tqdm
import tensorflow as tf
from collections import deque
import tensorflow.contrib.slim as slim
import numpy as np
from scipy import stats
from Holodeck.HolodeckEnvironment import *

#env = HolodeckUAVMazeWorld(grayscale=False)
env = HolodeckContinuousSphereMazeWorld(grayscale=True)

TAU = 0.01
GAMMA = .99
ACTOR_LR = 0.001
CRITIC_LR = 0.001
ACTOR_L2_WEIGHT_DECAY = 0.00
CRITIC_L2_WEIGHT_DECAY = 0.01
BATCH_SIZE = 64
REPLAY_BUFFER_SIZE = 10000
MAX_EPISODE_LENGTH = 1000
ITERATIONS_BEFORE_TRAINING = BATCH_SIZE + 1

ACTION_DIM = env.action_space.shape[0]

assert len(env.action_space.shape) == 1

def fanin_init(layer):
    fanin = layer.get_shape().as_list()[1]
    v = 1.0 / np.sqrt(fanin)
    return tf.random_uniform_initializer(minval=-v, maxval=v)

class Noise:
    def __init__(self, ):
        self.state = np.zeros(ACTION_DIM)

    def josh(self, mu, sigma):
        return stats.truncnorm.rvs((-1 - mu) / sigma, (1 - mu) / sigma, loc=mu, scale=sigma, size=len(self.state))

    def ou(self, mean, theta=.2, sigma=.15):
        self.state += -theta * (self.state - mean) - sigma * np.random.randn(len(self.state))
        return self.state.copy()


def actor_network(state, outer_scope, reuse=False):
    with tf.variable_scope(outer_scope + '/actor', reuse=reuse):
        uniform_random = tf.random_uniform_initializer(minval=-3e-3, maxval=3e-3)
        net = slim.conv2d(inputs=state, num_outputs=32, kernel_size=5, weights_initializer=fanin_init(state), biases_initializer=fanin_init(state))
        # net = slim.conv2d(inputs=net, num_outputs=64, kernel_size=4, stride=4, weights_initializer=fanin_init(net), biases_initializer=fanin_init(net))
        # net = slim.conv2d(inputs=net, num_outputs=128, kernel_size=3, padding="VALID", weights_initializer=fanin_init(net), biases_initializer=fanin_init(net))
        net = slim.conv2d(inputs=net, num_outputs=200, kernel_size=1, stride=5, padding="VALID", weights_initializer=fanin_init(net), biases_initializer=fanin_init(net))
        net = tf.contrib.layers.flatten(net)

        net = slim.fully_connected(net, 100, weights_initializer=fanin_init(net), biases_initializer=fanin_init(net))
        output = slim.fully_connected(net, ACTION_DIM, weights_initializer=uniform_random, biases_initializer=uniform_random, activation_fn=tf.tanh)

    return output


def critic_network(state, action, outer_scope, reuse=False):
    with tf.variable_scope(outer_scope + '/critic', reuse=reuse):
        uniform_random = tf.random_uniform_initializer(minval=-3e-3, maxval=3e-3)
        net = slim.conv2d(inputs=state, num_outputs=32, kernel_size=5, weights_initializer=fanin_init(state), biases_initializer=fanin_init(state))
        # net = slim.conv2d(inputs=net, num_outputs=64, kernel_size=4, stride=4, weights_initializer=fanin_init(net), biases_initializer=fanin_init(net))
        # net = slim.conv2d(inputs=net, num_outputs=128, kernel_size=3, padding="VALID", weights_initializer=fanin_init(net), biases_initializer=fanin_init(net))
        net = slim.conv2d(inputs=net, num_outputs=200, kernel_size=1, stride=5, padding="VALID", weights_initializer=fanin_init(net), biases_initializer=fanin_init(net))
        
        net = tf.concat(1, [tf.contrib.layers.flatten(net), action])
        net = slim.fully_connected(net, 100, weights_initializer=fanin_init(net), biases_initializer=fanin_init(net))
        net = slim.fully_connected(net, 1, weights_initializer=uniform_random, biases_initializer=uniform_random, activation_fn=None)

        return tf.squeeze(net, [1])

state_placeholder = tf.placeholder(tf.uint8, [None] + list(env.observation_space.shape), 'state')
next_state_placeholder = tf.placeholder(tf.uint8, [None] + list(env.observation_space.shape), 'next_state')

state_processed = 2.0 * (tf.cast(state_placeholder, tf.float32) - env.observation_space.low.min()) / (env.observation_space.high.max() - env.observation_space.low.min()) - 1
next_state_processed = 2.0 * (tf.cast(next_state_placeholder, tf.float32) - env.observation_space.low.min()) / (env.observation_space.high.max() - env.observation_space.low.min()) - 1

action_placeholder = tf.placeholder(tf.float32, [None, ACTION_DIM], 'action')
reward_placeholder = tf.placeholder(tf.float32, [None], 'reward')
done_placeholder = tf.placeholder(tf.bool, [None], 'done')

train_actor_output = actor_network(state_processed, outer_scope='train_network')
train_actor_next_output = actor_network(next_state_processed, outer_scope='train_network', reuse=True)
target_actor_output = actor_network(state_processed, outer_scope='target_network')
target_actor_next_output = actor_network(next_state_processed, outer_scope='target_network', reuse=True)

target_critic_next_output = critic_network(next_state_processed, target_actor_next_output, outer_scope='target_network')
train_critic_current_action = critic_network(state_processed, train_actor_output, outer_scope='train_network')
train_critic_placeholder_action = critic_network(state_processed, action_placeholder, outer_scope='train_network', reuse=True)

train_actor_vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope='train_network/actor')
target_actor_vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope='target_network/actor')
train_critic_vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope='train_network/critic')
target_critic_vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope='target_network/critic')

print 'Total Actor Parameters:', sum([sum([reduce(lambda x, y: x * y, l.get_shape().as_list()) for l in e]) for e in [train_actor_vars]])
print 'Total Critic Parameters:', sum([sum([reduce(lambda x, y: x * y, l.get_shape().as_list()) for l in e]) for e in [train_critic_vars]])

with tf.name_scope('actor_loss'):
    weight_decay_actor = tf.add_n([ACTOR_L2_WEIGHT_DECAY * tf.reduce_sum(var ** 2) for var in train_actor_vars])

    optim_actor = tf.train.AdamOptimizer(ACTOR_LR)
    loss_actor = -tf.reduce_mean(train_critic_current_action) + weight_decay_actor

    # Actor Optimization
    grads_and_vars_actor = optim_actor.compute_gradients(loss_actor, var_list=train_actor_vars, colocate_gradients_with_ops=True)
    optimize_actor = optim_actor.apply_gradients(grads_and_vars_actor)

    with tf.control_dependencies([optimize_actor]):
        train_target_vars = zip(train_actor_vars, target_actor_vars)
        train_actor = tf.group(*[target.assign(TAU * train + (1 - TAU) * target) for train, target in train_target_vars])

with tf.name_scope('critic_loss'):
    # q_target_value = tf.select(done_placeholder, reward_placeholder, reward_placeholder + GAMMA * tf.stop_gradient(target_critic_next_output))
    q_target_value = tf.cast(done_placeholder, tf.float32)*reward_placeholder + (1-tf.cast(done_placeholder, tf.float32))*(reward_placeholder + GAMMA * tf.stop_gradient(target_critic_next_output))
    q_error = (q_target_value - train_critic_placeholder_action) ** 2
    q_error_batch = tf.reduce_mean(q_error)
    weight_decay_critic = tf.add_n([CRITIC_L2_WEIGHT_DECAY * tf.reduce_sum(var ** 2) for var in train_critic_vars])
    loss_critic = q_error_batch + weight_decay_critic

    # Critic Optimization
    optim_critic = tf.train.AdamOptimizer(CRITIC_LR)
    grads_and_vars_critic = optim_critic.compute_gradients(loss_critic, var_list=train_critic_vars, colocate_gradients_with_ops=True)
    optimize_critic = optim_critic.apply_gradients(grads_and_vars_critic)
    with tf.control_dependencies([optimize_critic]):
        train_target_vars = zip(train_critic_vars, target_critic_vars)
        train_critic = tf.group(*[target.assign(TAU * train + (1 - TAU) * target) for train, target in train_target_vars])

sess = tf.Session(config=tf.ConfigProto(gpu_options= tf.GPUOptions(allow_growth=True),
                                        allow_soft_placement=True,
                                        log_device_placement=False))
sess.run(tf.global_variables_initializer())

# Initialize target = train
sess.run([target.assign(train) for train, target in zip(train_actor_vars, target_actor_vars)])
sess.run([target.assign(train) for train, target in zip(train_critic_vars, target_critic_vars)])

sess.graph.finalize()

replay_buffer = deque(maxlen=REPLAY_BUFFER_SIZE)
replay_priorities = np.zeros(replay_buffer.maxlen, dtype=np.float64)
replay_priorities_sum = 0
rewards = []

for episode in tqdm(range(1000)):
    env_state = env.reset()[0]
    eta_noise = Noise()
    training = len(replay_buffer) >= min(ITERATIONS_BEFORE_TRAINING, replay_buffer.maxlen)
    testing = (episode + 1) % 2 == 0 and training
    history = []

    for step in tqdm(range(MAX_EPISODE_LENGTH)):
        action = sess.run(train_actor_output, feed_dict={state_placeholder: [env_state]})[0]

        action = action if testing else np.clip(action, -1, 1) + eta_noise.ou(mean=action,theta=.15, sigma=.2)
        env.render()

        assert action.shape == env.action_space.sample().shape, (action.shape, env.action_space.sample().shape)

        env_next_state, env_reward, env_done, env_info = env.step(np.clip(action, -1, 1) * 2)
        env_next_state = env_next_state[0]

        replay_buffer.append([env_state, action, env_reward, env_next_state, env_done])

        replay_priorities_sum -= replay_priorities[len(replay_buffer) - 1]
        replay_priorities[len(replay_buffer) - 1] = 300
        replay_priorities_sum += replay_priorities[len(replay_buffer) - 1]

        env_state = env_next_state

        if training:
            p_errors = replay_priorities[:len(replay_buffer)] / replay_priorities_sum
            minibatch_indexes = np.random.choice(range(len(replay_buffer)), size=BATCH_SIZE, replace=False, p=p_errors)

            state_batch = np.array([replay_buffer[i][0] for i in minibatch_indexes]).astype(np.uint8)
            action_batch = np.array([replay_buffer[i][1] for i in minibatch_indexes])
            reward_batch = np.array([replay_buffer[i][2] for i in minibatch_indexes])
            next_state_batch = np.array([replay_buffer[i][3] for i in minibatch_indexes]).astype(np.uint8)
            done_batch = np.array([replay_buffer[i][4] for i in minibatch_indexes])

            _, _, errors = sess.run([train_critic, train_actor, q_error], feed_dict={
                                        state_placeholder: state_batch,
                                        action_placeholder: action_batch,
                                        reward_placeholder: reward_batch,
                                        next_state_placeholder: next_state_batch,
                                        done_placeholder: done_batch
                                    })

            for i, error in zip(minibatch_indexes, errors):
                replay_priorities_sum -= replay_priorities[i]
                replay_priorities[i] = error
                replay_priorities_sum += replay_priorities[i]

        if env_done:
            break
