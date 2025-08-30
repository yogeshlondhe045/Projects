import heapq
import os

# -------------------------------
# Huffman Tree Node
# -------------------------------
class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    # For priority queue
    def __lt__(self, other):
        return self.freq < other.freq


# -------------------------------
# Huffman Coding Class
# -------------------------------
class HuffmanCoding:
    def __init__(self, path):
        self.path = path
        self.heap = []
        self.codes = {}
        self.reverse_mapping = {}

    def make_frequency_dict(self, text):
        freq = {}
        for char in text:
            freq[char] = freq.get(char, 0) + 1
        return freq

    def make_heap(self, frequency):
        for key in frequency:
            node = HuffmanNode(key, frequency[key])
            heapq.heappush(self.heap, node)

    def merge_nodes(self):
        while len(self.heap) > 1:
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)
            merged = HuffmanNode(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2
            heapq.heappush(self.heap, merged)

    def make_codes_helper(self, root, current_code):
        if root is None:
            return
        if root.char is not None:
            self.codes[root.char] = current_code
            self.reverse_mapping[current_code] = root.char
            return
        self.make_codes_helper(root.left, current_code + "0")
        self.make_codes_helper(root.right, current_code + "1")

    def make_codes(self):
        root = heapq.heappop(self.heap)
        current_code = ""
        self.make_codes_helper(root, current_code)

    def get_encoded_text(self, text):
        encoded_text = ""
        for char in text:
            encoded_text += self.codes[char]
        return encoded_text

    def pad_encoded_text(self, encoded_text):
        extra_padding = 8 - len(encoded_text) % 8
        for i in range(extra_padding):
            encoded_text += "0"

        padded_info = "{0:08b}".format(extra_padding)
        encoded_text = padded_info + encoded_text
        return encoded_text

    def get_byte_array(self, padded_encoded_text):
        if len(padded_encoded_text) % 8 != 0:
            print("Encoded text not padded properly!")
            exit(0)

        b = bytearray()
        for i in range(0, len(padded_encoded_text), 8):
            byte = padded_encoded_text[i:i+8]
            b.append(int(byte, 2))
        return b

    def compress(self):
        filename, file_extension = os.path.splitext(self.path)
        output_path = filename + ".bin"

        with open(self.path, 'r') as file:
            text = file.read()

        frequency = self.make_frequency_dict(text)
        self.make_heap(frequency)
        self.merge_nodes()
        self.make_codes()

        encoded_text = self.get_encoded_text(text)
        padded_encoded_text = self.pad_encoded_text(encoded_text)

        b = self.get_byte_array(padded_encoded_text)

        with open(output_path, 'wb') as output:
            output.write(bytes(b))

        print("Compressed file saved as:", output_path)
        return output_path

    def remove_padding(self, padded_encoded_text):
        padded_info = padded_encoded_text[:8]
        extra_padding = int(padded_info, 2)

        padded_encoded_text = padded_encoded_text[8:]
        encoded_text = padded_encoded_text[:-1*extra_padding]
        return encoded_text

    def decode_text(self, encoded_text):
        current_code = ""
        decoded_text = ""

        for bit in encoded_text:
            current_code += bit
            if current_code in self.reverse_mapping:
                character = self.reverse_mapping[current_code]
                decoded_text += character
                current_code = ""
        return decoded_text

    def decompress(self, input_path):
        filename, file_extension = os.path.splitext(self.path)
        output_path = filename + "_decompressed.txt"

        with open(input_path, 'rb') as file:
            bit_string = ""
            byte = file.read(1)
            while byte:
                byte = ord(byte)
                bits = bin(byte)[2:].rjust(8, '0')
                bit_string += bits
                byte = file.read(1)

        encoded_text = self.remove_padding(bit_string)
        decompressed_text = self.decode_text(encoded_text)

        with open(output_path, 'w') as output:
            output.write(decompressed_text)

        print("Decompressed file saved as:", output_path)
        return output_path


# -------------------------------
# Run Example
# -------------------------------
if __name__ == "__main__":
    # Step 1: Create a sample text file automatically
    with open("sample.txt", "w") as f:
        f.write("hello huffman, this is a test for file compression using Huffman coding in Python!")

    # Step 2: Run Huffman Compression & Decompression
    path = "sample.txt"
    h = HuffmanCoding(path)

    compressed_file = h.compress()
    h.decompress(compressed_file)