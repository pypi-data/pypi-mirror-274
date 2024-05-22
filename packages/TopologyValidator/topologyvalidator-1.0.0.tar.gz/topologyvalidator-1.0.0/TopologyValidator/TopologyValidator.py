import yaml
import jsonref 
from jsonschema import validate as json_validate
from jsonschema.exceptions import ValidationError

def load_openapi_schema(file_path):
    with open(file_path, 'r') as file:
        openapi_spec = yaml.safe_load(file)
    return openapi_spec

def resolve_references(openapi_spec):
    return jsonref.JsonRef.replace_refs(openapi_spec)

def get_validator_schema(openapi_spec):
    return openapi_spec['paths']['/validator']['post']['requestBody']['content']['application/json']['schema']

def validate(data, schema):
    """Validate the converted topology data against the OpenAPI schema."""
    try:
        json_validate(instance=data, schema=schema)
        return {"result": "Validated Successfully", "status_code": 200}
    except ValidationError as e:
        return {"result": f"Validation Error: {e.message}", "status_code": 400}
