from environs import Env, EnvError

env = Env()
env.read_env()  # read .env file, if it exists

__all__ = ("env", "EnvError")
