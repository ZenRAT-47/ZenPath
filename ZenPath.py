import requests
import threading
import random
import time
from queue import Queue

def load_user_agents(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def dirbuster(queue, target_url, user_agents, delay_range):
    session = requests.Session()
    session.headers.update({'User-Agent': random.choice(user_agents)})

    while not queue.empty():
        path = queue.get()
        url = f"{target_url}/{path}"

        try:
            response = session.get(url)
            if response.status_code == 200:
                print(f"Found: {url}")

            if random.randint(1, 10) > 8:
                session.headers.update({'User-Agent': random.choice(user_agents)})

            time.sleep(random.uniform(*delay_range))
        except requests.RequestException as e:
            print(f"Error accessing {url}: {e}")
        finally:
            queue.task_done()
            if random.randint(1, 100) > 95:
                session.close()
                session = requests.Session()
                session.headers.update({'User-Agent': random.choice(user_agents)})

def main(target_url, wordlist_path, user_agents_file, thread_count=10, delay_range=(1, 3)):
    banner = """

                                                                                                                                      
                                                                                                                                      
ZZZZZZZZZZZZZZZZZZZ                                      PPPPPPPPPPPPPPPPP                           tttt         hhhhhhh             
Z:::::::::::::::::Z                                      P::::::::::::::::P                       ttt:::t         h:::::h             
Z:::::::::::::::::Z                                      P::::::PPPPPP:::::P                      t:::::t         h:::::h             
Z:::ZZZZZZZZ:::::Z                                       PP:::::P     P:::::P                     t:::::t         h:::::h             
ZZZZZ     Z:::::Z      eeeeeeeeeeee    nnnn  nnnnnnnn      P::::P     P:::::Paaaaaaaaaaaaa  ttttttt:::::ttttttt    h::::h hhhhh       
        Z:::::Z      ee::::::::::::ee  n:::nn::::::::nn    P::::P     P:::::Pa::::::::::::a t:::::::::::::::::t    h::::hh:::::hhh    
       Z:::::Z      e::::::eeeee:::::een::::::::::::::nn   P::::PPPPPP:::::P aaaaaaaaa:::::at:::::::::::::::::t    h::::::::::::::hh  
      Z:::::Z      e::::::e     e:::::enn:::::::::::::::n  P:::::::::::::PP           a::::atttttt:::::::tttttt    h:::::::hhh::::::h 
     Z:::::Z       e:::::::eeeee::::::e  n:::::nnnn:::::n  P::::PPPPPPPPP      aaaaaaa:::::a      t:::::t          h::::::h   h::::::h
    Z:::::Z        e:::::::::::::::::e   n::::n    n::::n  P::::P            aa::::::::::::a      t:::::t          h:::::h     h:::::h
   Z:::::Z         e::::::eeeeeeeeeee    n::::n    n::::n  P::::P           a::::aaaa::::::a      t:::::t          h:::::h     h:::::h
ZZZ:::::Z     ZZZZZe:::::::e             n::::n    n::::n  P::::P          a::::a    a:::::a      t:::::t    tttttth:::::h     h:::::h
Z::::::ZZZZZZZZ:::Ze::::::::e            n::::n    n::::nPP::::::PP        a::::a    a:::::a      t::::::tttt:::::th:::::h     h:::::h
Z:::::::::::::::::Z e::::::::eeeeeeee    n::::n    n::::nP::::::::P        a:::::aaaa::::::a      tt::::::::::::::th:::::h     h:::::h
Z:::::::::::::::::Z  ee:::::::::::::e    n::::n    n::::nP::::::::P         a::::::::::aa:::a       tt:::::::::::tth:::::h     h:::::h
ZZZZZZZZZZZZZZZZZZZ    eeeeeeeeeeeeee    nnnnnn    nnnnnnPPPPPPPPPP          aaaaaaaaaa  aaaa         ttttttttttt  hhhhhhh     hhhhhhh
                                                                                                                                      
                                                                                                                                      
                                                                                                                                      
  Written by ZenRat-47. https://github.com/ZenRAT-47. Special Occasions.
                                                                                                                                    
                                                                                                                                      
                                                                                                                                      
                                                                                                                                      

    """
    print(banner)

    print("ZenPath - Enhanced DirBuster with randomized User-Agent and request timing.")
    user_agents = load_user_agents(user_agents_file)
    queue = Queue()

    with open(wordlist_path, 'r') as file:
        for line in file:
            queue.put(line.strip())

    threads = []
    for _ in range(thread_count):
        worker = threading.Thread(target=dirbuster, args=(queue, target_url, user_agents, delay_range))
        worker.start()
        threads.append(worker)

    for thread in threads:
        thread.join()

    print("Scan complete.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Enhanced DirBuster with randomized User-Agent and request timing")
    parser.add_argument("target_url", help="The target URL to scan")
    parser.add_argument("wordlist_path", help="Path to the wordlist file")
    parser.add_argument("user_agents_file", help="Path to the file containing User-Agent strings")
    parser.add_argument("--threads", type=int, default=10, help="Number of threads to use")
    parser.add_argument("--min-delay", type=float, default=1, help="Minimum delay between requests")
    parser.add_argument("--max-delay", type=float, default=3, help="Maximum delay between requests")
    args = parser.parse_args()
    main(args.target_url, args.wordlist_path, args.user_agents_file, args.threads, (args.min_delay, args.max_delay))
