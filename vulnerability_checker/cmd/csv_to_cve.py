import csv
import subprocess
import argparse

def run_grype(image_name):
    """
    Run the grype command with the given image name.
    """
    command = [
        "grype",
        image_name,
        "--add-cpes-if-none",
        "--by-cve"
    ]
    subprocess.run(command)

def main():
    parser = argparse.ArgumentParser(description="Run grype for images from a CSV file.")
    parser.add_argument('-f', '--file', required=True, help="CSV file containing image names.")

    args = parser.parse_args()

    with open(args.file, "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        
        for row in csv_reader:
            image_name = row[0]
            run_grype(image_name)

if __name__ == "__main__":
    main()
