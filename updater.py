import requests
from base64 import b64encode


# Sends a POST request containing the url and a chunk of data
# If the request fails ("ERROR PROCESSING CONTENTS\n"), try again until it succeeds ("OK\n")
def post_chunk_and_checksum(string_to_process):
    has_processed = False
    while has_processed is False:
        r = requests.post(url, data='CHUNK: ' + string_to_process)
        if r.text == "OK\n":
            has_processed = True


# Address for connecting to app.js
url = "http://localhost:3000"

# File/Firmware to send and process
file_name = "example.hex"

# Open hex file and read in line by line
# For each line, remove the ':' and convert from hex to bytes to base64
with open(file_name, "r") as hex_file:
    for hex_string in enumerate(hex_file):
        hex_string = hex_file.readline().replace(':', '')
        encoded_string = b64encode(bytes.fromhex(hex_string)).decode()

        # If base64 string's length exceeds 20 characters,
        # Split it in half and send each half separately
        # Else, just send the entire thing
        if len(encoded_string) > 20:
            length = int(len(encoded_string) / 2)
            first_half = encoded_string[:length]
            second_half = encoded_string[length:]

            post_chunk_and_checksum(first_half)
            post_chunk_and_checksum(second_half)
        else:
            post_chunk_and_checksum(encoded_string)

    # Once firmware is fully uploaded,
    # POST request CHECKSUM and compare the checksum from Python to the checksum from Javascript
    # If they match, then the firmware upload is a success
    # Otherwise, it's a failure
    # In this case, the final checksum of example.hex should be 0x81
    js_checksum = requests.post(url, data='CHECKSUM')
    if js_checksum.text == "Checksum: 0x81\n":
        print("Successfully uploaded firmware")
    else:
        print("Error: Checksums do not match")

