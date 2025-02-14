import os
import yaml
import ast


def get_client_classes(directory):
    client_classes = {}
    for filename in os.listdir(directory):
        if filename.endswith("Client.py"):
            filepath = os.path.join(directory, filename)
            with open(filepath, "r") as file:
                tree = ast.parse(file.read(), filename=filename)
                for node in ast.walk(tree):
                    if isinstance(node, ast.ClassDef):
                        class_name = node.name
                        methods = {}
                        for n in node.body:
                            if isinstance(n, ast.FunctionDef):
                                # Get function arguments
                                args = []
                                for arg in n.args.args:
                                    if arg.arg != "self":  # Skip 'self' parameter
                                        args.append(arg.arg)
                                methods[n.name] = args
                        client_classes[class_name] = methods
    return client_classes


def generate_yaml(client_classes, output_file):
    with open(output_file, "w") as file:
        yaml.dump(client_classes, file, sort_keys=False)


if __name__ == "__main__":
    directory = "reqs"
    output_file = "clients.yaml"
    client_classes = get_client_classes(directory)
    generate_yaml(client_classes, output_file)
    print(f"YAML file '{output_file}' generated successfully.")
