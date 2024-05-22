import cli
import paramiko
import threading

def get_desc(interface):
    output = cli.execute('show running-config interface ' + interface)
    for line in output.split('\n'):
        if line.strip().startswith('description'):
            desc = line.split('description ')[1].strip()
            return desc
    return None

def change_vlan(interface, desc, ssh_shell):
    if desc == "Office":
        ssh_shell.send(f"conf t\ninterface {interface}\nswitchport access vlan 200\n")
        print("VLAN changed to 200 for interface", interface)
    else:
        print("No VLAN change needed for interface", interface)

def execute_ssh_command(host, username, password):
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=host, username=username, password=password)
        print(f"Connected to {host}")

        ssh_shell = ssh_client.invoke_shell()

        output = ssh_shell.recv(65535).decode("utf-8")
        print(f"Logged into {host}:\n{output}")

        output = cli.execute('show interfaces status')
        for line in output.split('\n'):
            if '55' in line:
                interface = line.split()[0]
                desc = get_desc(interface)
                if desc is not None:
                    change_vlan(interface, desc, ssh_shell)
                else:
                    print("No description found for interface", interface)

        ssh_client.close()
    except paramiko.AuthenticationException:
        print(f"Failed to authenticate on {host}: Invalid username or password")
    except paramiko.SSHException as ssh_exc:
        print(f"SSH error on {host}: {ssh_exc}")
    except Exception as e:
        print(f"Error on {host}: {e}")

def execute_ssh_commands_in_parallel(hosts, username, password):
    threads = []
    for host in hosts:
        thread = threading.Thread(target=execute_ssh_command, args=(host, username, password))
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()

def run_network_commands(username, password, base_ip, start_ip, end_ip):
    hosts = [base_ip.format(i) for i in range(start_ip, end_ip + 1)]
    execute_ssh_commands_in_parallel(hosts, username, password)



    run_network_commands(username, password, base_ip, start_ip, end_ip)
 
