import HuffmanTree
import coding
from time import perf_counter

# Main function
def main():

    def _print_table(data):
        for row in data:
            output_file.write("{:<15} {:<5}".format(*row))
    # Define letters with corresponding frequencies by index in lists
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
               'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    frequencies = [19, 16, 17, 11, 42, 12, 14, 17, 16, 5, 10, 20, 19,
                   24, 18, 13, 1, 25, 35, 25, 15, 5, 21, 2, 8, 3]
    max_width = 80

    # Create Huffman Tree instance, build the tree, create the coding
    # dictionary, and create a Huffman Coder instance that will encode and
    # decode using the coder the character-frequency dictionary mapping 
    # provided
    tree = HuffmanTree.HuffmanTree(letters, frequencies)
    root = tree.build_huffman_tree()
    code_dict = tree.get_codes_dict(root)
    coder = coding.HuffmanCoder(code_dict)

    # Define valid punctuation allowed in alphabetic lines
    valid_punctuation = set(" ,.!?;:-\'\"")

    # Track Duration, Compression and Decompression metrics for the 
    # entire program.
    # Maintain stats separately for compression and decompression.
    total_duration = 0.0
    total_enc_bits = 0
    total_compressed_bits = 0
    total_dec_bits = 0
    total_decompressed_bits = 0

    # Open input and output files for reading and writing, respectively
    with open('input.txt', 'r') as input_file, \
        open('output.txt', 'w') as output_file:

        # Print Huffman Tree (pre-order traversal)
        output_file.write(f'The tree in preorder is: \n')
        nodes = tree.print_preorder_traversal(root)
        current_line = ""
        for i in range(len(nodes)):
            if i != len(nodes) - 1:
                output_file.write(f'{nodes[i]}, ')
                current_line += f'{nodes[i]}, '
            else:
                output_file.write(f'{nodes[i]}')

            if len(current_line) >= max_width:
                output_file.write('\n')
                current_line = ""
        output_file.write('\n---------------------------------------------\n')

        # Print the Codes Generated from the Huffman Tree
        current_line = ""
        output_file.write(f'The code is: \n')
        for char,code in code_dict.items():
            output_file.write(f'{char:>8}: {code:>2}, ')
            current_line += f'{char:>8}: {code:>2}, '

            if len(current_line) >= max_width:
                output_file.write('\n')
                current_line = ""
        output_file.write('\n---------------------------------------------\n')


        # Read and process each line from input file
        for line in input_file:
            # Skip blank lines        
            if not line:
                continue           
            # Strip white spaces in line
            line = line.strip()

            '''
            Determine whether the line is alphabetic (requiring encoding) 
            or binary (requiring decoding).
            It is considered alphabetic if all characters in the line are 
            letters in the alphabet or are punctuation. 
            It is considered binary if all characters are either 0 or 1.
            Otherwise, output an error to the file and move to the next line. 
            '''
            is_alphabetic = all(char.isalpha() or char in valid_punctuation
                                for char in line)
            is_binary = all(char in '01' for char in line)

            if not (is_alphabetic or is_binary):
                output_file.write(f"Error: Line '{line}' has invalid "
                                  f"characters\n\n")
                continue

            # Encode if line is alphabetic
            if is_alphabetic:
                # Encode line and calculate encoding time
                start_time = perf_counter()
                encoded = coder.encode(line)
                end_time = perf_counter()


                if encoded['valid'] is False:
                    output_file.write(f'Input: "{line}"\n')
                    output_file.write(encoded['message'])
                    continue

                # Calculate encoding time duration in milliseconds
                # Also add the encoding duration for the line to the 
                # total program duration
                duration = (end_time - start_time) * 1000  
                total_duration += duration

                '''
                Calculate Encoding Compression Rate: 
                Number of original bits (8 bits per character) divided by 
                Number of post-encoded compressed bits
                '''
                original_enc_bits = len(line) * 8  
                compressed_bits = len(encoded)
                compression_rate = (compressed_bits/original_enc_bits) * 100 

                total_enc_bits += original_enc_bits
                total_compressed_bits += compressed_bits

                # Print Encoding duration and Compression Rate metrics to 
                # output file
                output_file.write(f"Encoded:\n '{line}'\n to:\n {encoded['message']}\n")
                output_file.write(f"Duration: {duration:.4f} milliseconds\n")
                output_file.write(f"Compression Rate: " 
                                  f"{compression_rate:.2f}%\n\n")

            # Decode if line consists of valid binary codes            
            else:
                # Decode line and time it
                start_time = perf_counter()
                decoded = coder.decode(line)
                end_time = perf_counter()

                if decoded['valid'] is False:
                    output_file.write(f'Input: "{line}"\n')
                    output_file.write(decoded['message'])
                    continue

                # Calculate decoding duration for line
                # Also add that line duration to the total program duration
                duration = (end_time - start_time) * 1000  
                total_duration += duration

                '''
                Calculate Decoding Decompression (Expansion) Rate: 
                Number of decompressed bits (num characters * 8) divided by 
                Number of original bits in binary codes line
                '''
                original_dec_bits = len(line)
                final_dec_bits = len(decoded) * 8
                decompression_rate = (final_dec_bits / 
                                      original_dec_bits) * 100 

                total_dec_bits += original_dec_bits
                total_decompressed_bits += final_dec_bits

                # Print Decoding duration and Decompression Rate metrics to 
                # output file
                output_file.write(f"Decoded:\n '{line}'\n to:\n {decoded['message']}\n")
                output_file.write(f"Duration: {duration:.4f} milliseconds\n")
                output_file.write(f"Decompression (Expansion) Rate: "+ 
                                  f"{decompression_rate:.2f}%\n\n")

        # Calculate Overall Compression Rate for lines requiring encoding
        overall_compression_rate = (total_compressed_bits / 
                                    total_enc_bits) * 100 
        # Print compression statistics for encoding
        output_file.write(f"Total Original Bytes to Encode: " 
                          f"{int(total_enc_bits/8)}\n")
        output_file.write(f"Total Original Bits to Encode: {total_enc_bits}\n")
        output_file.write(f"Total Compressed Bits: {total_compressed_bits}\n")
        output_file.write(f"Overall Compression Rate: " + 
                          f"{overall_compression_rate:.2f}%\n\n")

        # Calculate Overall Decompression Rate for lines requiring decoding       
        overall_decompression_rate = (total_decompressed_bits / 
                                      total_dec_bits) * 100 
        # Print overall decompression statistics for decoding        
        output_file.write(f"Total Original Bits to Decode: " 
                          f"{total_dec_bits}\n")
        output_file.write(f"Total Final Decompressed Bytes: " + 
                          f"{int(total_decompressed_bits/8)}\n")
        output_file.write(f"Total Final Decompressed Bits: " + 
                          f"{total_decompressed_bits}\n")
        output_file.write(f"Overall Decompression (Expansion) Rate: " + 
                          f"{overall_decompression_rate:.2f}%\n\n")

        # Print total duration of program 
        output_file.write(f"Total Program Duration: " + 
                          f"{total_duration:.4f} milliseconds\n\n")        

if __name__ == "__main__":
    main()