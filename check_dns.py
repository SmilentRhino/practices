'''
This is a simple script to verify dnsname ip match when you have just updated 
your dns record
'''
import os
import os.path
import click
import dns.resolver

@click.command()
@click.argument('filepath')
def check_dns(filepath):
    '''This script check dns in file'''
    if filepath.startswith('/'):
        abs_path = filepath 
    else:
        abs_path = os.path.join(os.getcwd(), filepath)
    resolver = dns.resolver.Resolver(configure=False)
    resolver.nameservers = ['8.8.8.8']
    with open(abs_path, 'r') as f:
        for i in f.readlines():
#            print(i)
            dns_name, ip_address = i.strip().split(' ')
#            print(dns_name, ip_address)
            answer = resolver.query(dns_name, 'A')
            if any(ip_address == x.address for x in answer):
                print(u"{} {} \u2713".format(dns_name, ip_address))
            else:
                print("{} {} x".format(dns_name, ip_address))
if __name__ == '__main__':
    check_dns()
