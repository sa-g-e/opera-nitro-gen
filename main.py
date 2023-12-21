from random import choice
import random, requests, threading

class count:
    c = 0

session = requests.Session()

def load_proxies(file_path='proxies.txt'):
    with open(file_path, 'r') as f:
        proxies = [line.strip() for line in f.readlines() if line.strip()]
    return proxies

def genuid():
    characters = 'abcdef1234567890'
    return ''.join(random.choice(characters) for _ in range(32))

proxies = load_proxies()

def gen():
    while True:
        url = "https://api.discord.gx.games/v1/direct-fulfillment"
        
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.0",
        }

        data = {
            "partnerUserId": genuid()
        }
        print(data)

        try:
            proxy = choice(proxies)
            r = session.post(url, json=data, headers=headers, proxies={'http': proxy})

            if r.status_code == 200:
                token = r.json().get('token')
                if token:
                    count.c += 1
                    link = f"https://discord.com/billing/partner-promotions/1180231712274387115/{token}"
                    with open("links.txt", "a") as f:
                        f.write(f"{link}\n")
                        print(f"x{count.c}")
            elif r.status_code == 429:
                print(f"Rate-limit")    
            else:
                print(f"req failed {r.status_code}")
        except Exception as e:
            print(f"req failed {e}")

def main():
    threadsamount = int(input(f"threads: "))

    threads = []
    for i in range(threadsamount):
        thread = threading.Thread(target=gen)
        threads.append(thread)

    for thread in threads:
        thread.start()


if __name__ == "__main__":
    main()
