import HuffmanTree
import coding
from time import perf_counter

# Main function
def main(letters, frequencies, output_file):

    # Create Huffman Tree instance, build the tree, create the coding
    # dictionary, and create a Huffman Coder instance that will encode and
    # decode using the coder the character-frequency dictionary mapping 
    # provided
    tree = HuffmanTree.HuffmanTree(letters, frequencies)
    build_start_time = perf_counter()
    root = tree.build_huffman_tree()
    build_stop_time = perf_counter()
    code_dict = tree.get_codes_dict(root)
    coder = coding.HuffmanCoder(code_dict)

    # Define valid punctuation allowed in alphabetic lines
    valid_punctuation = set(" ,.!?;:-\'\"")

    # Track Duration, Compression and Decompression metrics for the 
    # entire program.
    total_duration = 0.0
    total_enc_bits = 0
    total_compressed_bits = 0
    total_dec_bits = 0
    total_decompressed_bits = 0

    # Open input file for reading
    with open('input.txt', 'r') as input_file:
        # Print Huffman Tree (pre-order traversal)
        output_file.write(f'The tree in preorder is: \n')
        start_time = perf_counter()
        nodes = tree.print_preorder_traversal(root)
        stop_time = perf_counter()
        max_width = 80
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

        traverse_duration = (stop_time - start_time) * 1000
        build_duration = (build_stop_time - build_start_time) * 1000
        output_file.write('\n\n')
        output_file.write(f"Tree Traversal Duration: " + 
                          f"{traverse_duration:.4f} ms\n")
        output_file.write(f'Build Tree Duration: ' 
                          f'{build_duration:.4f} ms\n')
        output_file.write('---------------------------------------------\n')

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
        encoded_count = decoded_count = 0
        for line in input_file:
            # Skip blank lines        
            if not line or line == "\n":
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
                output_file.write(f'Input: {line}\n')
                output_file.write(f"Error: Invalid characters\n")
                output_file.write(f'\n-------------------' 
                                  f'--------------------------\n')
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
                    output_file.write(f'\n----------------------------' 
                                      f'-----------------\n')
                    continue

                # Calculate encoding time duration in milliseconds
                # Also add the encoding duration for the line to the 
                # total program duration
                duration = (end_time - start_time) * 1000  
                total_duration += duration

                '''
                Calculate Encoding Compression Rate: 
                Number of original bits (5 bits per character) divided by 
                Number of post-encoded compressed bits

                    - Since we are only generating codes for the letters in 
                    the alphabet, 5 bits is the minimum necessary to code the 
                    26 letters. In essence, using standard methods, the code 
                    lengths of each letter would be fixed at 5. However, 
                    Huffman encoding generates variable length codes that
                    will reduce the length of the encoded string.
                
                Compression Rate Formula Reference: 
                'A Comparison of Huffman Codes Across Ian': 
                (jhu.instructure.com/courses/93679/pages/
                module-8-huffman-tree-review-article)
                '''
                original_enc_bits = len(line) * 5
                compressed_bits = len(encoded['message'])
                compression_rate = \
                    (1 - (compressed_bits/original_enc_bits)) * 100 

                total_enc_bits += original_enc_bits
                total_compressed_bits += compressed_bits

                # Print Encoding duration and Compression Rate metrics to 
                # output file
                output_file.write(f"Encoded:\n '{line}'\n to:\n" 
                                  f" {encoded['message']}\n")
                output_file.write(f"Duration: {duration:.4f} milliseconds\n")
                output_file.write(f"Compression Rate: " 
                                  f"{compression_rate:.2f}%\n")
                output_file.write(f'\n------------------------------------' 
                                  f'---------\n')
                encoded_count += 1

            # Decode if line consists of valid binary codes            
            else:
                # Decode line and time it
                start_time = perf_counter()
                decoded = coder.decode(line)
                end_time = perf_counter()

                if decoded['valid'] is False:
                    output_file.write(f'Input: "{line}"\n')
                    output_file.write(decoded['message'])
                    output_file.write('\n--------------------------------' 
                                      f'-------------\n')
                    continue

                # Calculate decoding duration for line
                # Also add that line duration to the total program duration
                duration = (end_time - start_time) * 1000  
                total_duration += duration

                '''
                Calculate Decoding Decompression Rate: 
                Number of decompressed bits (num characters * 5) divided by 
                Number of original bits in binary codes line
                '''
                
                original_dec_bits = len(line)
                final_dec_bits = len(decoded['message']) * 5
                decompression_rate = (final_dec_bits / original_dec_bits) * 100

                total_dec_bits += original_dec_bits
                total_decompressed_bits += final_dec_bits

                # Print Decoding duration and Decompression Rate metrics to 
                # output file
                output_file.write(f"Decoded:\n '{line}'\n to:\n " 
                                  f"{decoded['message']}\n")
                output_file.write(f"Duration: {duration:.4f} milliseconds\n")
                output_file.write(f"Decompression Rate: "+ 
                                  f"{decompression_rate:.2f}%\n")
                output_file.write(f'\n----------------------------' 
                                  f'-----------------\n')
                decoded_count += 1

        # Calculate Overall Compression Rate for lines requiring encoding
        overall_compression_rate = (1 - (total_compressed_bits / 
                                    total_enc_bits)) * 100 
        # Print compression statistics for encoding
        output_file.write(f"Total Original Letters for Encoding: " 
                          f"{int(total_enc_bits/5)}\n")
        output_file.write(f"Total Original Bits for Encoding: " 
                          f"{total_enc_bits}\n")
        output_file.write(f"Total Compressed Bits: {total_compressed_bits}\n")
        output_file.write(f"Overall Compression Rate: " + 
                          f"{overall_compression_rate:.2f}%\n\n")

        # Calculate Overall Decompression Rate for lines requiring decoding       
        overall_decompression_rate = (1 - (total_decompressed_bits / 
                                      total_dec_bits)) * 100 
        # Print overall decompression statistics for decoding        
        output_file.write(f"Total Original Bits for Decoding: " 
                          f"{total_dec_bits}\n")
        output_file.write(f"Total Final Decompressed Letters: " + 
                          f"{int(total_decompressed_bits/5)}\n")
        output_file.write(f"Total Final Decompressed Bits: " + 
                          f"{total_decompressed_bits}\n")
        output_file.write(f"Overall Decompression Rate: " + 
                          f"{overall_decompression_rate:.2f}%\n\n")

        # Print total duration of program 
        output_file.write(f"Total Program Duration: " + 
                          f"{total_duration:.4f} milliseconds\n\n")
        
        # Print total number of lines processed:
        total_lines_processed = encoded_count + decoded_count
        output_file.write(f'Total Number of Lines Processed: ' 
                          f'{total_lines_processed}\n'
                          f'    - Lines Encoded: {encoded_count}\n'
                          f'    - Lines Decoded: {decoded_count}\n')
        input_file.close()

if __name__ == "__main__":
    # Define two sets of letters and frequencies
    letters_1 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 
                 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 
                 'Y', 'Z']
    frequencies_1 = [19, 16, 17, 11, 42, 12, 14, 17, 16, 5, 10, 20, 19,
                     24, 18, 13, 1, 25, 35, 25, 15, 5, 21, 2, 8, 3]
    
    letters_2 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 
                 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 
                 'Y', 'Z']
    frequencies_2 = [10, 20, 30, 15, 25, 10, 35, 20, 18, 11, 16, 17, 14,
                     22, 19, 28, 24, 16, 20, 11, 23, 12, 13, 15, 10, 9]

    # Open output file in append mode to keep results from both runs
    with open('output.txt', 'w') as output_file:
        # Loop through each pair of letters and frequencies and call the 
        # main function
        i = 1
        for letters, frequencies in [(letters_1, frequencies_1), 
                                     (letters_2, frequencies_2)]:
            # Write a separator between runs
            output_file.write(f"\n----------------------------------------" 
                              f"---------------------------------------\n")
            output_file.write(f'Frequency Table: {i}\n')
            output_file.write(f"Letters: {letters}\n")
            output_file.write(f"Frequencies: {frequencies}\n\n")
            main(letters, frequencies, output_file)
            i+=1
    output_file.close()
