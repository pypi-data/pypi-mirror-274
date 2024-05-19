import paramiko
from io import StringIO
from src.ParamikoMock.ssh_mock import SSHClientMock, SSHCommandMock, SSHMockEnvron, SSHCommandFunctionMock
from unittest.mock import patch

def example_function_1():
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # Some example of connection
    client.connect('some_host',
                    port=22,
                    username='root',
                    password='root',
                    banner_timeout=10)
    stdin, stdout, stderr = client.exec_command('ls -l')
    return stdout.read()

def example_function_2():
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # Some example of connection
    client.connect('some_host_2',
                    port=4826,
                    username='root',
                    password='root',
                    banner_timeout=10)
    stdin, stdout, stderr = client.exec_command('sudo docker ps')
    return stdout.read()

def example_function_3():
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # Some example of connection
    client.connect('some_host_3',
                    port=22,
                    username='root',
                    password='root',
                    banner_timeout=10)
    stdin, stdout, stderr = client.exec_command('custom_command --param1 value1')
    return stdout.read()

def test_example_function_1():
    SSHMockEnvron().add_responses_for_host('some_host', 22, {
        'ls -l': SSHCommandMock('', 'ls output', '')
    }, 'root', 'root')
    with patch('paramiko.SSHClient', new=SSHClientMock): 
        output = example_function_1()
        assert output == 'ls output'

def test_example_function_2():
    ssh_mock = SSHClientMock()
    SSHMockEnvron().add_responses_for_host('some_host_2', 4826, {
        'sudo docker ps': SSHCommandMock('', 'docker-ps-output', '')
    }, 'root', 'root')
    # patch the paramiko.SSHClient with the mock
    with patch('paramiko.SSHClient', new=SSHClientMock): 
        output = example_function_2()
        assert output == 'docker-ps-output'

def test_example_function_3():
    # We can also use a custom command processor
    def custom_command_processor(ssh_client_mock: SSHClientMock, command: str):
        # Parse the command and do something with it
        if 'param1' in command and 'value1' in command:
            return StringIO(''), StringIO('value1'), StringIO('')
    
    # You can use a regexp expresion to match the command with the custom processor
    ssh_mock = SSHClientMock()
    SSHMockEnvron().add_responses_for_host('some_host_3', 22, {
        r're(custom_command .*)': SSHCommandFunctionMock(custom_command_processor) # This is a regexp command
    }, 'root', 'root')
    # patch the paramiko.SSHClient with the mock
    with patch('paramiko.SSHClient', new=SSHClientMock): 
        output = example_function_3()
        assert output == 'value1'
