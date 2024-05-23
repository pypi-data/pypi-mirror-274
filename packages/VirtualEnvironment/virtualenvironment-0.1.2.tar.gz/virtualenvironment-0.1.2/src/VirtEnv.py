class BuildVenv:

    def __init__(self):
        self

    def VirtEnv(self):
        import venv 

        venv.EnvBuilder().make_env()

        return