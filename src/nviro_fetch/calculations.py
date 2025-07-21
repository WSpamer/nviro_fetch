def calculate_utah_chill_units(temperature_celsius):
    """
    Calculates Utah Chill Units for a given hourly temperature in Celsius.

    Args:
        temperature_celsius (float): Hourly temperature in Celsius.

    Returns:
        float: The corresponding Utah Chill Units for that hour.
    """
    if temperature_celsius < 1.4:  # Below this temperature, no chill is accumulated
        return 0.0  # No chill
    # Define the ranges for chill accumulation
    elif 1.4 <= temperature_celsius <= 2.4:
        return 0.5  # Low chill
    elif 2.4 < temperature_celsius <= 9.1:
        return 1.0  # Optimal chill range
    elif 9.1 < temperature_celsius <= 12.4:
        return 0.5  # Reduced chill
    elif 12.4 < temperature_celsius < 16.0:
        return 0.0  # No chill
    elif 16.0 <= temperature_celsius <= 18.0:
        return -0.5  # Negative chill
    elif temperature_celsius > 18.0:
        return -1.0  # Strong negative chill
    else:
        return None
