def transform_file(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            # Split the line into parts by whitespace
            parts = line.split()
            if len(parts) >= 2:  # Ensure the line has enough parts
                # Extract the first two elements and join them with a comma
                transformed_line = f"{parts[0]},{parts[1]}\n"
                outfile.write(transformed_line)

# Example usage:
# Replace 'input.txt' and 'output.txt' with your file paths.
transform_file('input\CA-HepPh.txt', 'input/CA-HepPh.csv')