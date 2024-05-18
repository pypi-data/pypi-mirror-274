from typing import List, Optional, Tuple

import numpy as np
import pandas as pd
from pydantic import BaseModel, ValidationError

from classification_model.config.core import config


def drop_na_inputs(*, input_data: pd.DataFrame) -> pd.DataFrame:
    """Check model inputs for na values and filter."""
    validated_data = input_data.copy()
    new_vars_with_na = [
        var
        for var in config.model_config.input_features
        if var
        not in config.model_config.categorical_vars
        + config.model_config.cabin
        + config.model_config.numerical_vars
        and validated_data[var].isnull().sum() > 0
    ]
    
    validated_data.dropna(subset=new_vars_with_na, inplace=True)

    return validated_data


def validate_inputs(*, input_data: pd.DataFrame) -> Tuple[pd.DataFrame, Optional[dict]]:
    """Check model inputs for unprocessable values."""

    relevant_data = input_data[config.model_config.input_features].copy()
    
    validated_data = drop_na_inputs(input_data=relevant_data)
    errors = None

    try:
        # replace numpy nans so that pydantic can validate
        MultiplePassengerDataInputs(
            inputs=validated_data.replace({np.nan: None}).to_dict(orient="records")
        )
    except ValidationError as error:
        errors = error.json()

    return validated_data, errors


class PassengerDataInputSchema(BaseModel):
    PassengerId: Optional[int]
    Age: Optional[float]
    Fare: Optional[float]
    Pclass: Optional[int]
    Sex: Optional[str]
    Name: Optional[str]
    SibSp: Optional[int]
    Parch: Optional[int]
    Embarked: Optional[str]
    Ticket: Optional[str]
    Cabin: Optional[str]


class MultiplePassengerDataInputs(BaseModel):
    inputs: List[PassengerDataInputSchema]