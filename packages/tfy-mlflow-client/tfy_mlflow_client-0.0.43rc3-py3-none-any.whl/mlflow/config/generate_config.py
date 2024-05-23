import inspect

from mlflow.server import app


def generate_config(api_route):
    class_name = "".join(word.capitalize() for word in api_route.name.split("_"))
    response_dto = {api_route.__dict__.get("response_model")}
    if response_dto:
        response_dto = response_dto.pop()
        if response_dto:
            response_dto = response_dto.__name__
    else:
        response_dto = {}
    request_func_annotation = inspect.getfullargspec(route.endpoint).annotations
    if "request_dto" in request_func_annotation:
        request_dto = request_func_annotation["request_dto"].__name__
    else:
        request_dto = {}
        if isinstance(request_func_annotation, dict):
            for key, value in request_func_annotation.items():
                if inspect.isclass(value):
                    request_dto[key] = value.__name__
                else:
                    request_dto[key] = value
    class_definition = f"""
class {class_name}:
    path = '{api_route.path}'
    method = '{api_route.methods.pop()}'
    response_dto = {response_dto}
    request_dto = {request_dto}
    """
    return class_definition


total_write = []
total_write.append(
    """import typing

from mlflow.dto.artifacts_dto import *
from mlflow.dto.auth_dto import *
from mlflow.dto.experiments_dto import *
from mlflow.dto.mlfoundry_artifacts_dto import *
from mlflow.dto.python_deployment_config_dto import *
from mlflow.dto.runs_dto import *
"""
)
for route in app.routes:
    if "/preview" not in route.path:
        total_write.append(generate_config(route))

with open("config.py", "w") as f:
    f.write("\n\n".join(total_write))
