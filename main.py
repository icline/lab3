import HuffmanTree

# Main function to process input file
def main():
    # Set frequency table
    freq_table = {
        'A': 19, 'B': 16, 'C': 17, 'D': 11, 'E': 42, 'F': 12, 'G': 14, 
        'H': 17, 'I': 16, 'J': 5, 'K': 10, 'L': 20, 'M': 19, 'N': 24, 
        'O': 18, 'P': 13, 'Q': 1, 'R': 25, 'S': 35, 'T': 25, 'U': 15, 
        'V': 5, 'W': 21, 'X': 2, 'Y': 8, 'Z': 3
    }
    
    # Create HuffmanTree instance from the frequency table above
    huff_tree = HuffmanTree.Huffman_Tree(freq_table)

    # Define valid punctuation allowed in alphabetic lines
    valid_punctuation = set(" ,.!?;:-\'\"")
    
    # Open input and output files for reading and writing, respectively
    with open('input.txt', 'r') as input_file, \
        open('output.txt', 'w') as output_file:
        
        # Read and process each line from input file
        for line in input_file:
            
            # Skip blank lines
            if not line:
                continue
            # Remove white space from line
            line = line.strip()
            
            '''
            Determine wheter all characters are alphabetic or binary.
            It is considered alphabetic if all characters are letters in
            the alphabet or punctuation. 
            It is considered binary if all characters are either 0 or 1.
            Otherwise, output an error to the file and move to the next line. 
            '''
            is_alpha = all((char.isalpha() or char in valid_punctuation) \
                           for char in line)
            is_binary = all(char in '01' for char in line)
            
            if not (is_alpha or is_binary):
                output_file.write(f"Error: Line '{line}' has invalid " + 
                              f"characters\n\n")
                continue
            
            # Encode if line is alphabetic
            if is_alpha:
                encoded = huff_tree.encode(line)
                if encoded is None:
                    output_file.write(f"Error: Alphabetic line '{line}' " + 
                                      f"has invalid characters. Unable to " + 
                                      f"encode.\n\n")
                else:
                    output_file.write(f"Encoded:\n '{line}' \nto:\n " + 
                                      f"{encoded}\n\n")

            # Decode otherwise (i.e. if line consists of valid binary codes)
            else:
                decoded = huff_tree.decode(line)
                if decoded is None:
                    output_file.write(f"Error: Line '{line}' is an invalid " + 
                                  f"binary string for decoding\n\n")
                else:
                    output_file.write(f"Decoded:\n '{line}' \nto: \n " + 
                                  f"{decoded}\n\n")

if __name__ == "__main__":
    main()
