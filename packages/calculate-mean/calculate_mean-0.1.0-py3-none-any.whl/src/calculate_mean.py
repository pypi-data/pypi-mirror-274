def calculate_mean(values):
    """
    This function calculates the mean of a list of numbers.

    Parameters:
    values (list): A list of numerical values

    Returns:
    float: The mean of the values
    """
    # Check if the list is empty
    if not values:
        return "The list is empty, please provide a list of numbers."

    # Calculate the sum of the values
    total_sum = sum(values)

    # Calculate the count of the values
    count = len(values)

    # Calculate the mean
    mean = total_sum / count

    return mean