import subprocess


def stop_mysql_server():
    subprocess.run('C:/Program Files/MySQL/MySQL Server 8.0/bin/mysqladmin shutdown', shell=True)

if __name__ == '__main__':
    stop_mysql_server()
