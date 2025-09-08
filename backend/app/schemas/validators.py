"""
Dictionary mapping each Belgian province to its valid postal code ranges.

Each province is associated with a list of `range` objects that represent 
the valid postal codes within that region.
"""
PROVINCE_POSTAL_CODE_RANGES: dict[str, list[range]] = {
    "Brussels": [range(1000, 1300)],
    "Luxembourg": [range(6600, 6999)],
    "Antwerp": [range(2000, 2999)],
    "FlemishBrabant": [range(1500, 1999), range(3000, 3499)],
    "EastFlanders": [range(9000, 9999)],
    "WestFlanders": [range(8000, 8999)],
    "Liège": [range(4000, 4999)],
    "WalloonBrabant": [range(1300, 1499)],
    "Limburg": [range(3500, 3999)],
    "Namur": [range(5000, 5680)],
    "Hainaut": [range(6000, 6599), range(7000, 7999)]
}

def is_postal_code_valid_in_any_province(postal_code: int) -> bool:
    """
    Check if the given postal code is valid in any Belgian province.

    Args:
        postal_code (int): The postal code to validate.

    Returns:
        bool: True if the postal code falls within any defined province range, False otherwise.
    """
    return any(
        postal_code in r
        for ranges in PROVINCE_POSTAL_CODE_RANGES.values()
        for r in ranges
    )

def is_postal_code_valid_for_province(postal_code: int, province: str) -> bool:
    """
    Check if the given postal code is valid within the specified province.

    Args:
        postal_code (int): The postal code to validate.
        province (str): The name of the province to validate against.

    Returns:
        bool: True if the postal code is valid within the specified province, False otherwise.
    """
    ranges = PROVINCE_POSTAL_CODE_RANGES.get(province, [])
    return any(postal_code in r for r in ranges)