import os

def get_path_tree(address):
    contents = []

    # Get initial address contents or return an error if address doesn't exist    
    try:
        address_data = os.listdir(address)
    except Exception as e:
        print(f'[!] The address: {address} does not exist')
        return contents

    # Make a tuple of files and a tuple of folders
    folders = []
    files = []
    for item in address_data:
        item_path = os.path.join(address, item)
        if os.path.isdir(item_path):
            folders.append(item_path)
        else:
            files.append(item)

    # Wrap this into a list of ["address", (folders), (files)]
    contents.append((address, tuple(folders), tuple(files)))

    # Now loop through until there are no directories left
    for folder in folders:
        contents.extend(get_path_tree(folder))

    return contents

def print_tree(contents):
    address_map = {address: (folders, files) for address, folders, files in contents}

    def _print_tree(address, indent):
        print(f'{indent}{os.path.basename(address)}/')
        sub_indent = indent + "    "
        folders, files = address_map.get(address, ([],[]))
        for file in files:
            print(f'{sub_indent}{file}')
        for folder in folders:
            _print_tree(folder, sub_indent)
    
    if contents:
        root_address = contents[0][0]
        _print_tree(root_address, '')
        

def main():
    contents = get_path_tree("./static")
    print_tree(contents)
    

if __name__ == "__main__":
    main()