from pydantic import field_validator

def case_insensitive_enum_validator(field_name, enum_cls):
    @field_validator(field_name, mode="before")
    def validate_enum(cls, value):
        if isinstance(value, str):
            for member in enum_cls:
                if member.value.lower() == value.lower():
                    return member
            valid_values = [e.value for e in enum_cls]
            raise ValueError(f"Invalid value '{value}'. Must be one of: {valid_values}")
        return value
    return validate_enum