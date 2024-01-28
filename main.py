import time  # we will use it to get unix timestamp
import os  # we will use it to expand user path
import shutil  # we will use it to copy files

# config file paths
current_unix_timestamp = str(time.time())
default_config_file = '~/.config/kitty/kitty.conf'
current_backup_file = f'~/.config/kitty/kitty.conf.{current_unix_timestamp}.bak'
default_config_file_full_path = os.path.expanduser(default_config_file)
current_backup_file_full_path = os.path.expanduser(current_backup_file)

# backup config file
shutil.copyfile(default_config_file_full_path, current_backup_file_full_path)

# load map file
with open('map.txt') as f:
    lines = f.readlines()
line1 = lines[0].strip()
line2 = lines[1].strip()
map_dict = dict(zip(line1, line2))

# read config file all lines
with open(default_config_file_full_path) as f:
    lines = f.readlines()

# for each line search mapping line and add additional line with mapping
new_lines = []
for line in lines:

    # if line doesn't contain map
    if ' map ' not in line:
        new_lines.append(line)
        continue

    # if line contains map but starts with #::
    if line.startswith('#::'):
        new_lines.append(line)
        continue

    # line contains map the first thing is to find mapping parts
    line_parts = line.split(' ')
    map_part_index = line_parts.index('map')
    keys_part_index = map_part_index + 1
    keys_list = line_parts[keys_part_index].split('+')

    # for each key in keys list find mapping
    new_keys_list = []
    for key in keys_list:
        if key not in map_dict:
            new_keys_list.append(key)
            continue
        new_keys_list.append(map_dict[key])

    # create new line with new keys list
    new_keys_part = '+'.join(new_keys_list)
    new_line = ''
    for i, part in enumerate(line_parts):
        if i == keys_part_index:
            new_line += new_keys_part
        else:
            new_line += part
        new_line += ' '

    # remove comment from line and new line if it exists
    if line.startswith('#'):
        line = line[1:].strip() + '\n'
        new_line = new_line[1:].strip() + '\n'

    new_lines.append(line)
    new_lines.append(new_line)

# write new config file
with open(default_config_file_full_path, 'w') as f:
    f.writelines(new_lines)

