#!/usr/bin/env python3

import argparse
import requests
import json
import concurrent.futures


# ----------------------------------
# Colors
# ----------------------------------
NOCOLOR='\033[0m'
RED='\033[0;31m'
GREEN='\033[0;32m'
ORANGE='\033[0;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
LIGHTGRAY='\033[0;37m'
DARKGRAY='\033[1;30m'
LIGHTRED='\033[1;31m'
LIGHTGREEN='\033[1;32m'
YELLOW='\033[1;33m'
LIGHTBLUE='\033[1;34m'
LIGHTPURPLE='\033[1;35m'
LIGHTCYAN='\033[1;36m'
WHITE='\033[1;37m'



def check_graphql_endpoint(base_url, endpoint, verbose):
    payload = {
        "query": "query{__typename}"
    }
    headers = {"Content-Type": "application/json"}

    # Construct the full URL
    url = base_url.rstrip('/') + endpoint

    try:
        response = requests.post(url, headers=headers, json=payload)

        # Verbose output
        if verbose:
            print(f"{YELLOW}\nChecking: {url}{NOCOLOR}")
            status_color = GREEN if response.status_code == 200 else RED
            print(f"{status_color}Status Code: {response.status_code}{NOCOLOR}")
        
        response_data = response.json()

        if response.status_code == 200 and 'data' in response_data and '__typename' in response_data['data']:
            print(f"{GREEN}{url} seems to be a GraphQL endpoint.{NOCOLOR}")
            return True
        else:
            if verbose:
                print(f"{RED}{url} does not seem to be a GraphQL endpoint.{NOCOLOR}")
            return False
    except Exception as e:
        if verbose:
            print(f"{RED}Error at {url}: {e}{NOCOLOR}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Check if a URL has a GraphQL endpoint.")
    parser.add_argument("base_url", help="Base URL to check")
    parser.add_argument("-v", "--verbose", help="Increase output verbosity", action="store_true")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Number of threads to use (default: 10)")

    args = parser.parse_args()

    endpoints = [
        "/graphql/console",
        "/api",
        "/api/graphql",
        "/graphql/api",
        "/graphql/graphql",
        "/v1/explorer",
        "/v1/graphiql",
        "/graph",
        "/graphql",
        "/graphql/",
        "/graphql/console/",
        "/graphql.php",
        "/graphiql",
        "/graphiql.php"
    ]

    # Using ThreadPoolExecutor to speed up requests
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = [executor.submit(check_graphql_endpoint, args.base_url, endpoint, args.verbose) for endpoint in endpoints]
        concurrent.futures.wait(futures)

if __name__ == "__main__":
    main()
