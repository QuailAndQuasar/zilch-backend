from typing import Dict, List, Tuple
import numpy as np

from .env import ZilchEnv
from .agent import ZilchRLAgent
from ..config.rl_config import RLConfig, default_config


def run_episode(env: ZilchEnv, agent: ZilchRLAgent, cfg: RLConfig) -> float:
    """
    Run a single training episode and return cumulative reward.
    """
    state = env.reset()
    total_reward = 0.0

    for _ in range(cfg.max_steps_per_episode):
        action = agent.choose_action(state)
        next_state, reward, done, info = env.step(action)
        agent.update(state, action, reward, next_state, done)
        total_reward += float(reward)
        state = next_state
        if done:
            break

    return total_reward


def train(episodes: int = None, cfg: RLConfig = None) -> ZilchRLAgent:
    """
    Train a Q-learning agent for the Zilch environment.
    Returns the trained agent.
    """
    cfg = cfg or default_config
    if episodes is not None:
        cfg.episodes = episodes

    env = ZilchEnv()
    agent = ZilchRLAgent(
        action_space=env.action_space,
        alpha=cfg.alpha,
        gamma=cfg.gamma,
        epsilon=cfg.epsilon_start,
        epsilon_min=cfg.epsilon_min,
        epsilon_decay=cfg.epsilon_decay,
    )

    rewards: List[float] = []
    for ep in range(cfg.episodes):
        ep_reward = run_episode(env, agent, cfg)
        rewards.append(ep_reward)
        if (ep + 1) % max(1, cfg.episodes // 10) == 0:
            avg = np.mean(rewards[-max(1, cfg.episodes // 10):])
            print(f"Episode {ep+1}/{cfg.episodes} | Last: {ep_reward:.2f} | Avg recent: {avg:.2f} | epsilon: {agent.epsilon:.3f}")

    # Save learned Q-table
    agent.save(cfg.model_path)
    return agent

