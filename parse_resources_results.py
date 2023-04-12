import os
import sys

if __name__ == "__main__":
    if len(sys.argv) == 2:
        input_file_path = sys.argv[1]
        output_file_path1 = './output1.csv'
        output_file_path2 = './output2.csv'

        if os.path.exists(input_file_path):
            input_file = open(input_file_path, 'r')
            output_file1 = open(output_file_path1, 'w')
            output_file2 = open(output_file_path2, 'w')

            containers_stats = {}
            line_info_idxs = None
            for line in input_file.read().splitlines():
                if ' -- ' in line: # Ignore empty lines
                    continue
                elif 'CONTAINER ID' in line:
                    line = line[7:] # Ignore ␛[2J␛[H on beginning of line
                    line_info_idxs = {
                        'NAME': line.index('NAME'), 
                        'CPU %': line.index('CPU %'),
                        'MEM USAGE': line.index('MEM USAGE'),
                        'MEM %': line.index('MEM %')
                        }
                    continue

                name = line[line_info_idxs['NAME']:].split(' ')[0]
                cpu = float(line[line_info_idxs['CPU %']:].split('%')[0])
                mem_usage = float(line[line_info_idxs['MEM USAGE']:].split('MiB')[0])
                mem = float(line[line_info_idxs['MEM %']:].split('%')[0])

                output_file2.write(name + ';' + str(cpu) + ';' + str(mem_usage) + ';' + str(mem) + '\n')

                if not (name in containers_stats):
                    containers_stats[name] = {
                        'COUNT': 0,
                        'CPU %': 0.0,
                        'MEM USAGE': 0.0,
                        'MEM %': 0.0
                        }
                
                containers_stats[name]['COUNT'] += 1
                containers_stats[name]['CPU %'] += cpu
                containers_stats[name]['MEM USAGE'] += mem_usage
                containers_stats[name]['MEM %'] += mem

            for container in containers_stats.keys():
                count = containers_stats[container]['COUNT']

                output_file1.write(container + ';')
                output_file1.write(str(containers_stats[container]['CPU %'] / count) + ';')
                output_file1.write(str(containers_stats[container]['MEM USAGE'] / count) + ';')
                output_file1.write(str(containers_stats[container]['MEM %'] / count) + ';')
                output_file1.write('\n')

            input_file.close()
            output_file1.close()
            output_file2.close()