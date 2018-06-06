'''
THis is a simple script to get cert expiration date on cdn backend
Read in a cdn_mapping file
With format like following:
DomainName\tBackendDomianName
'''
import subprocess

with open('cdn_mapping', 'r') as f:
    for line in f:
        record_map = line.strip().split('\t')    
        print(record_map)
        #cmd_line = "openssl s_client -connect {1}:443 -servername {0} < /dev/null 2> /dev/null |openssl x509 -text | grep 'After'|grep 2018".format(record_map[0], record_map[1])
        cmd_line = "openssl s_client -connect {1}:443 -servername {0} < /dev/null 2> /dev/null |openssl x509 -text | grep 'After'".format(record_map[0], record_map[1])
        print(cmd_line)
        try:
             output = subprocess.check_output(cmd_line, shell=True)
             print(output)
#            p1 = subprocess.Popen(cmd_line, stdout=subprocess.PIPE ,shell=True)
#            p2 = subprocess.Popen("openssl x509 -noout -dates", stdin=p1.stdout, stdout=subprocess.PIPE)
#            while True:
#                output = p2.communicate()
#                print(output)
        except Exception as e:
            print(e)
