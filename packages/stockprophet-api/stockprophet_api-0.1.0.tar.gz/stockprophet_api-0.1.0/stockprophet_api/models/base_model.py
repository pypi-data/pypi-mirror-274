
from pydantic import BaseModel as PydanticBaseModel
from .custom_types import BSON_TYPES_ENCODERS

class BaseModel(PydanticBaseModel, validate_on_load=False, validate_on_assignment=False):
    """
    Base model for all models in the application.

    It sets default values for the model configuration.
    Default values are:
    - json_encoders: Custom JSON encoders for BSON types
    - from_attributes: Use attributes when initializing the model
    - extra: Forbid additional fields
    - validate_assignment: Validate field assignments
    - str_strip_whitespace: Strip whitespace from string fields
    - populate_by_name: Populate fields by name
    - str_to_upper: Convert string fields to uppercase
    - json_schema_serialization_defaults_required: Do not include default values in the JSON schema
    - allow_inf_nan: Do not allow +/- infinity and NaN values
    - arbitrary_types_allowed: Do not allow arbitrary types
    - validate_all: Do not validate all fields

    Attributes:
        model_config (dict): Configuration for the model
    """
    model_config = {
        "json_encoders": BSON_TYPES_ENCODERS, 
        "from_attributes": True, 
        "extra": "forbid", "validate_assignment": True, 
        "str_strip_whitespace": True, 
        "populate_by_name": True, 
        "str_to_upper": True,
        "json_schema_serialization_defaults_required":  False,
        "allow_inf_nan": False,
        "arbitrary_types_allowed": False,
        "validate_all": False
    }
