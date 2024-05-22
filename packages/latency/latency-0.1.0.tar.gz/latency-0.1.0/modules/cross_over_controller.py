import pandas as pd

ZERO_VALUE = 0


class CrossOverController:
    def __init__(self, df):
        """
        Initialize the CrossOverController with a DataFrame containing time series data.
        Parameters:
        - df (DataFrame): DataFrame containing data with a 'Time' column in nanosecond precision.
        """
        if 'Time' not in df.columns:
            raise ValueError("DataFrame must contain a 'Time' column.")

        if df.empty:
            raise ValueError("The provided DataFrame is empty.")  # Check for an empty DataFrame

        self.df = df.copy()

        try:
            self.df['Time'] = pd.to_datetime(self.df['Time'], unit='ns')  # Ensure 'Time' is in datetime format with nanosecond precision
        except Exception as e:
            raise ValueError("Error converting 'Time' column to datetime with nanosecond precision:", e)

    def detect_timestamp_crossovers(self):
        """
        Identifies any rows where timestamps are not in chronological order.
        Returns:
        - DataFrame: A DataFrame containing the details of each timestamp crossover incident, if any.
        """
        # Detect crossovers before sorting to capture actual data issues
        time_diffs = self.df['Time'].diff()
        crossovers = self.df[time_diffs.dt.total_seconds() < ZERO_VALUE]
        if crossovers.empty:
            print("\n------------------------TIMESTAMP CROSSOVERS----------------------------")
            print("\nNo timestamp crossovers detected.\n")
            return None
        else:
            print("\n----------------------TIMESTAMP CROSSOVERS------------------------------")
            print(f"\nDetected {len(crossovers)} timestamp crossovers.\n")
            return crossovers

    def report_timestamp_crossovers(self):
        """
        Generates a report of all timestamp crossovers detected in the dataset and stores the indices of crossover lines.
        Returns:
        - list: A list containing the indices of the DataFrame rows where timestamp crossovers were detected.
        """
        crossovers = self.detect_timestamp_crossovers()
        self.df.sort_values('Time', inplace=True)  # Sort after detecting crossovers
        if crossovers is not None:
            # Store indices of the rows with timestamp crossovers
            crossover_indices = crossovers.index.tolist()
            return crossover_indices
        return []
