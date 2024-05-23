class CalculateMean:
    def __init__(self, values):
        self.values = values

    def calculate_mean(self):
        """
        This method calculates the mean of a list of numbers.

        Returns:
        float: The mean of the values
        """
        # Check if the list is empty
        if not self.values:
            return "The list is empty, please provide a list of numbers."

        # Calculate the sum of the values
        total_sum = sum(self.values)

        # Calculate the count of the values
        count = len(self.values)

        # Calculate the mean
        mean = total_sum / count

        return mean
