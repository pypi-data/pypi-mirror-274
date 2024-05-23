import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

class GasChromatographyAnalysis:
    def read_data(file_path):
        """Read CSV data from the given file path."""
        data = pd.read_csv(file_path)
        return data

    def process_data(data):
        """Process the data to find peaks and other relevant analysis."""
        x = data['Time']
        y = data['Signal']
        peaks, _ = find_peaks(y, height=0.5)  # Detect peaks with height threshold
        return x, y, peaks

    def plot_results(x, y, peaks, output_path):
        """Plot the results and save the plot as an image."""
        plt.figure(figsize=(10, 6))
        plt.plot(x, y, label='Signal')
        plt.plot(x[peaks], y[peaks], "x", label='Peaks')
        plt.xlabel('Time')
        plt.ylabel('Signal')
        plt.title('Gas Chromatography Analysis')
        plt.legend()
        plt.savefig(output_path)
        plt.close()

    def main():
        """Main function to execute the analysis."""
        input_file = 'sample_data.csv'  # Replace with your input CSV file
        output_file = 'result.png'  # Output image file

        # Read and process data
        data = read_data(input_file)
        x, y, peaks = process_data(data)

        # Plot and save results
        plot_results(x, y, peaks, output_file)
        print(f"Results saved to {output_file}")

    if __name__ == '__main__':
        main()
