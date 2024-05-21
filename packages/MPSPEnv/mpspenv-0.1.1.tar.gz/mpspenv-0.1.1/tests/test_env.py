import numpy as np
import pytest
import subprocess
from helpers import *


@pytest.fixture(scope="session", autouse=True)
def build_env():
    subprocess.run("make build", shell=True)  # Setup
    yield
    subprocess.run("make clean", shell=True)  # Teardown


def test_cpputest_suite():
    result = subprocess.run("make cpputest", shell=True, capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr)
    assert result.returncode == 0, "CppUTest suite failed"


def test_reset_to_transportation():
    from MPSPEnv import Env

    env = Env(2, 2, 4, auto_move=False)
    T = np.array(
        [
            [0, 2, 0, 2],
            [0, 0, 2, 0],
            [0, 0, 0, 2],
            [0, 0, 0, 0],
        ],
        dtype=np.int32,
    )
    env.reset_to_transportation(T)

    assert np.all(env.bay == np.zeros((2, 2)))
    assert np.all(env.T == T)
    assert np.all(env.mask == np.array([0, 0, 1, 1, 0, 0, 0, 0]))

    env.close()


def test_rollouts():
    rollouts = get_rollouts()

    for rollout in rollouts:
        env = recreate_env(rollout["settings"], rollout["seed"])
        run_env_against_rollout(env, rollout["states"])
        env.close()


def test_quicktest():
    episodes = 1000

    for _ in range(episodes):
        settings = get_random_settings()
        seed = np.random.randint(0, 1000000)
        initial_containers = get_initial_containers(settings, seed)
        env = recreate_env(settings, seed)
        additional_info = get_additional_env_info(env)

        while not env.terminal:
            sanity_check_env(env, **additional_info)
            action = get_random_action(env.mask)
            env.step(action)

        sanity_check_env(env, **additional_info)
        assert initial_containers - env.total_reward == env.containers_placed
        env.close()
