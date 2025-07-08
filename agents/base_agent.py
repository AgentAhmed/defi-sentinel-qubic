class BaseAgent:
    def __init__(self, name: str, context):
        self.name = name
        self.context = context

    def log(self, message: str):
        print(f"[{self.name}] {message}")

    def read_context(self, key: str, default=None):
        return self.context.read(key, default)

    def write_context(self, key: str, value):
        self.context.write(key, value)

    def run(self, *args, **kwargs):
        raise NotImplementedError("Each agent must implement its own run() method.")
