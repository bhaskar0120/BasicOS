import argparse

def main():
    parser = argparse.ArgumentParser(description=
    'Converts text file to binary retaining values eg, 0a ff ff -> 0x0a 0xff 0xff'
    )
    parser.add_argument('filename', help='File to convert from text to binary')
    parser.add_argument('-o', '--output', help='Output file')

    args = parser.parse_args()

    filename = args.filename
    output = args.output if args.output else '.'.join([args.filename.split('.')[0],'bin'])
    return (filename, output)

def read_file(filename):
    try:
        with open(filename,'r') as read:
            lines = list(filter(lambda l: not (l == '' or l.isspace()), map(str.strip,read.readlines())))
    except FileNotFoundError as error:
        print(f"{filename} not found")
        exit(1)
    return lines

def parse_file(lines):
    binary_data = []
    try:
        for line, val in enumerate(lines):
            for col,chunk in enumerate(val.split(' ')):
                if chunk == '': continue
                if '*' in chunk:
                    num, size = chunk.split('*') 
                    try:
                        binary_data.append(int(num).to_bytes(int(size), byteorder='little'))
                    except ValueError as error:
                        print(f'{chunk} cannot be parsed as proper instruction, at {line}:{col}')
                        exit(1)
                elif chunk.startswith('dx'):
                    binary_data.append(int(chunk[2:],16).to_bytes(4,byteorder='little'))
                elif len(chunk) == 2:
                    try:
                        binary_data.append(int(chunk,16).to_bytes())
                    except ValueError as error:
                        print(f'{chunk} is not a single byte hexadecimal, at {line}:{col}')
                        exit(1)
                else:
                    raise ValueError(f"Unknown token {chunk} at {line}:{col}")
    except ValueError as e:
        print(e)
        exit(1)
    return binary_data

def write_file(output, binary_data):
    with open(output, 'wb') as write_file:
        for i in binary_data:
            write_file.write(i)
    print(binary_data)


if __name__ == "__main__":
    filename, output = main()
    lines = read_file(filename)
    binary_data = parse_file(lines)
    write_file(output,binary_data)
