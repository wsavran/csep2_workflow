import docker

def run_u3etas():
    client = docker.from_env()
    client.containers.run('wsavran/csep:u3etas-test', 
            volumes=['u3etas-test:/run_dir/output_dir'])
            

if __name__ == "__main__":
    run_u3etas()
    
