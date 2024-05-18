from typing import Any, List

from docstring_parser import parse
from pydantic import BaseModel, Field


class RequestMetarNearest(BaseModel):
    latitude: str = Field(
        ...,
        description=(
            "The latitude of the location for which the nearest METAR"
            " station is requested."
        ),
    )
    longitude: str = Field(
        ...,
        description=(
            "The longitude of the location for which the nearest"
            " METAR station is requested."
        ),
    )


class PointQueryPrecipTotalAccum24Hr(BaseModel):
    layer: str = Field(
        ...,
        description=(
            "The layer of the precipitation total accumulation in the"
            " last 24 hours."
        ),
    )
    projection: str = Field(
        ...,
        description=(
            "The projection of the location for which the"
            " precipitation total accumulation is requested."
        ),
    )
    longitude: float = Field(
        ...,
        description=(
            "The longitude of the location for which the"
            " precipitation total accumulation is requested."
        ),
    )
    latitude: float = Field(
        ...,
        description=(
            "The latitude of the location for which the precipitation"
            " total accumulation is requested."
        ),
    )


class RequestNDFDBasic(BaseModel):
    latitude: float = Field(
        ...,
        description=(
            "The latitude of the location for which the NDFD basic"
            " forecast is requested."
        ),
    )
    longitude: float = Field(
        ...,
        description=(
            "The longitude of the location for which the NDFD basic"
            " forecast is requested."
        ),
    )
    forecast_time: str = Field(
        ...,
        description=(
            "The forecast time for which the NDFD basic forecast is"
            " requested."
        ),
    )


class PointQueryBaronHiresMaxReflectivityDbzAll(BaseModel):
    layer: str = Field(
        ...,
        description=(
            "The layer of the maximum reflectivity in dBZ for all"
            " heights."
        ),
    )
    projection: str = Field(
        ...,
        description=(
            "The projection of the location for which the maximum"
            " reflectivity is requested."
        ),
    )
    longitude: float = Field(
        ...,
        description=(
            "The longitude of the location for which the maximum"
            " reflectivity is requested."
        ),
    )
    latitude: float = Field(
        ...,
        description=(
            "The latitude of the location for which the maximum"
            " reflectivity is requested."
        ),
    )


class PointQueryBaronHiresWindSpeedMph10Meter(BaseModel):
    layer: str = Field(
        ...,
        description=(
            "The layer of the wind speed in mph at 10 meters above"
            " ground level."
        ),
    )
    projection: str = Field(
        ...,
        description=(
            "The projection of the location for which the wind speed"
            " is requested."
        ),
    )
    longitude: float = Field(
        ...,
        description=(
            "The longitude of the location for which the wind speed"
            " is requested."
        ),
    )
    latitude: float = Field(
        ...,
        description=(
            "The latitude of the location for which the wind speed is"
            " requested."
        ),
    )


def _remove_a_key(d: dict, remove_key: str) -> None:
    """Remove a key from a dictionary recursively"""
    if isinstance(d, dict):
        for key in list(d.keys()):
            if key == remove_key and "type" in d.keys():
                del d[key]
            else:
                _remove_a_key(d[key], remove_key)


def base_model_to_openai_function(
    pydantic_type: type[BaseModel],
    output_str: bool = False,
) -> dict[str, Any]:
    """
    Convert a Pydantic model to a dictionary representation of functions.

    Args:
        pydantic_type (type[BaseModel]): The Pydantic model type to convert.

    Returns:
        dict[str, Any]: A dictionary representation of the functions.

    """
    schema = pydantic_type.model_json_schema()

    docstring = parse(pydantic_type.__doc__ or "")
    parameters = {
        k: v
        for k, v in schema.items()
        if k not in ("title", "description")
    }

    for param in docstring.params:
        if (name := param.arg_name) in parameters["properties"] and (
            description := param.description
        ):
            if "description" not in parameters["properties"][name]:
                parameters["properties"][name][
                    "description"
                ] = description

    parameters["type"] = "object"

    if "description" not in schema:
        if docstring.short_description:
            schema["description"] = docstring.short_description
        else:
            schema["description"] = (
                "Correctly extracted"
                f" `{pydantic_type.__class__.__name__.lower()}` with"
                " all the required parameters with correct types"
            )

    _remove_a_key(parameters, "title")
    _remove_a_key(parameters, "additionalProperties")

    if output_str:
        out = {
            "function_call": {
                "name": pydantic_type.__class__.__name__.lower(),
            },
            "functions": [
                {
                    "name": pydantic_type.__class__.__name__.lower(),
                    "description": schema["description"],
                    "parameters": parameters,
                },
            ],
        }
        return str(out)

    else:
        return {
            "function_call": {
                "name": pydantic_type.__class__.__name__.lower(),
            },
            "functions": [
                {
                    "name": pydantic_type.__class__.__name__.lower(),
                    "description": schema["description"],
                    "parameters": parameters,
                },
            ],
        }


def multi_base_model_to_openai_function(
    pydantic_types: List[BaseModel] = None,
) -> dict[str, Any]:
    """
    Converts multiple Pydantic types to a dictionary of functions.

    Args:
        pydantic_types (List[BaseModel]]): A list of Pydantic types to convert.

    Returns:
        dict[str, Any]: A dictionary containing the converted functions.

    """
    functions: list[dict[str, Any]] = [
        base_model_to_openai_function(pydantic_type)["functions"][0]
        for pydantic_type in pydantic_types
    ]

    return {
        "function_call": "auto",
        "functions": functions,
    }


def function_to_str(function: dict[str, Any]) -> str:
    """
    Convert a function dictionary to a string representation.

    Args:
        function (dict[str, Any]): The function dictionary to convert.

    Returns:
        str: The string representation of the function.

    """
    function_str = f"Function: {function['name']}\n"
    function_str += f"Description: {function['description']}\n"
    function_str += "Parameters:\n"

    for param, details in function["parameters"][
        "properties"
    ].items():
        function_str += (
            f"  {param} ({details['type']}):"
            f" {details.get('description', '')}\n"
        )

    return function_str


def functions_to_str(functions: list[dict[str, Any]]) -> str:
    """
    Convert a list of function dictionaries to a string representation.

    Args:
        functions (list[dict[str, Any]]): The list of function dictionaries to convert.

    Returns:
        str: The string representation of the functions.

    """
    functions_str = ""
    for function in functions:
        functions_str += function_to_str(function) + "\n"

    return functions_str
