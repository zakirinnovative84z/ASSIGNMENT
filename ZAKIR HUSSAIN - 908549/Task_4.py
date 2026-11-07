tasks = ["build", "test", "deploy", "design"]

dependencies = [
    ("build", "test"),
    ("test", "deploy"),
    ("design", "build")
]

def execution_order(tasks, dependencies):
    pass

print(execution_order(tasks, dependencies))