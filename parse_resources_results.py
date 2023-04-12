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
                        'MEM %': line.index('MEM %'),
                        'NET I/O': line.index('NET I/O')
                        }
                    continue

                name = line[line_info_idxs['NAME']:].split(' ')[0]
                cpu = float(line[line_info_idxs['CPU %']:].split('%')[0])
                mem_usage = float(line[line_info_idxs['MEM USAGE']:].split('MiB')[0])
                mem = float(line[line_info_idxs['MEM %']:].split('%')[0])
                net_in = line[line_info_idxs['NET I/O']:].split('B / ')[0][0:-1]
                net_in = float(net_in) if net_in else 0.0
                net_out = line[line_info_idxs['NET I/O']:].split('B / ')[1].split('B')[0][0:-1]
                net_out = float(net_out) if net_out else 0.0

                output_file2.write(name + ';')
                output_file2.write(str(cpu) + ';')
                output_file2.write(str(mem_usage) + ';')
                output_file2.write(str(mem) + ';')
                output_file2.write(str(net_in) + ';')
                output_file2.write(str(net_out))
                output_file2.write('\n')

                if not (name in containers_stats):
                    containers_stats[name] = {
                        'COUNT': 0,
                        'CPU %': 0.0,
                        'MEM USAGE': 0.0,
                        'MEM %': 0.0,
                        'NET IN': 0.0,
                        'NET OUT': 0.0
                        }
                
                containers_stats[name]['COUNT'] += 1
                containers_stats[name]['CPU %'] += cpu
                containers_stats[name]['MEM USAGE'] += mem_usage
                containers_stats[name]['MEM %'] += mem
                containers_stats[name]['NET IN'] += net_in
                containers_stats[name]['NET OUT'] += net_out

            for container in containers_stats.keys():
                count = containers_stats[container]['COUNT']

                output_file1.write(container + ';')
                output_file1.write(str(containers_stats[container]['CPU %'] / count) + ';')
                output_file1.write(str(containers_stats[container]['MEM USAGE'] / count) + ';')
                output_file1.write(str(containers_stats[container]['MEM %'] / count) + ';')
                output_file1.write(str(containers_stats[container]['NET IN'] / count) + ';')
                output_file1.write(str(containers_stats[container]['NET OUT'] / count))
                output_file1.write('\n')

            input_file.close()
            output_file1.close()
            output_file2.close()