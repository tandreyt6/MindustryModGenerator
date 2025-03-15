import os
import struct
import hashlib
import argparse

MAGIC = b'BINPACK'
VERSION = 1
HEADER_FORMAT = '<7sBII'
ENTRY_HEADER_FORMAT = '<IIH32s'


def create_package(files, output_path):
    entries = []
    content = bytearray()

    for file_path in files:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File {file_path} not found")

        with open(file_path, 'rb') as f:
            data = f.read()

        file_name = os.path.basename(file_path)
        name_bytes = file_name.encode('utf-8')
        checksum = hashlib.sha256(data).digest()

        entries.append((
            len(content),
            len(data),
            name_bytes,
            checksum
        ))

        content.extend(data)

    header = bytearray()
    header.extend(struct.pack(
        HEADER_FORMAT,
        MAGIC,
        VERSION,
        len(files),
        len(content)
    ))

    for entry in entries:
        offset, size, name_bytes, checksum = entry
        header.extend(struct.pack(
            ENTRY_HEADER_FORMAT,
            offset,
            size,
            len(name_bytes),
            checksum
        ))
        header.extend(name_bytes)

    if os.path.dirname(output_path):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'wb') as f:
        f.write(header)
        f.write(content)


class BinaryPackage:
    def __init__(self, path):
        self.path = path
        self.files = {}
        self.content_start = 0
        self._load()

    def _load(self):
        with open(self.path, 'rb') as f:
            header = f.read(struct.calcsize(HEADER_FORMAT))
            magic, version, file_count, content_size = struct.unpack(
                HEADER_FORMAT, header
            )

            if magic != MAGIC:
                raise ValueError("Invalid file format")

            for _ in range(file_count):
                entry_header = f.read(struct.calcsize(ENTRY_HEADER_FORMAT))
                offset, size, name_len, checksum = struct.unpack(
                    ENTRY_HEADER_FORMAT, entry_header
                )

                name_bytes = f.read(name_len)
                file_name = name_bytes.decode('utf-8')

                self.files[file_name] = {
                    'offset': offset,
                    'size': size,
                    'checksum': checksum
                }

            self.content_start = f.tell()

    def get_file(self, name):
        if name not in self.files:
            raise KeyError(f"File {name} not found")

        meta = self.files[name]
        with open(self.path, 'rb') as f:
            f.seek(self.content_start + meta['offset'])
            data = f.read(meta['size'])

        if hashlib.sha256(data).digest() != meta['checksum']:
            raise ValueError(f"Checksum mismatch for {name}")

        return data


# if __name__ == '__main__':
#     package = BinaryPackage('test.bin')
#     print("Available files:", list(package.files.keys()))
#
#     try:
#         data = package.get_file('test.png')
#         print("File size:", len(data))
#     except KeyError as e:
#         print(e)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='File packer')
    parser.add_argument('--files', nargs='+', help='Files to pack')
    parser.add_argument('-o', '--output', required=True, help='Output file')
    args = parser.parse_args()

    try:
        create_package(args.files, args.output)
        print(f"Package created: {args.output}")
    except Exception as e:
        print(f"Error: {str(e)}")