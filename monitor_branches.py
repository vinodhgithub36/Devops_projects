import requests
import time

# Configuration
bitbucket_url = "https://bitbucket.com/rest/api/1.0/projects/project-name/repos/repo-name/branches"
jenkins_url = "https://jenkins.com:8443/job/CS-branch-Sonar-scan/buildWithParameters"
bitbucket_auth = ("user-name", "bitbucket-api_token")
jenkins_auth = ("user-name", "Jenkins_api_token")

branch_check_interval = 10  # Time interval to check for new branches in seconds

# Proxy configuration (replace with your proxy details if needed)
proxies = {
    "http": "http://proxy:3128/",
    "https": "http://proxy:3128/",
}

# Disable SSL verification
requests.packages.urllib3.disable_warnings()

def get_branches():
    response = requests.get(bitbucket_url, auth=bitbucket_auth, verify=False, proxies=proxies)
    response.raise_for_status()
    branches = [branch['displayId'] for branch in response.json()['values']]
    return set(branches)

def trigger_jenkins_build(branch_name):
    build_params = {"BRANCH_NAME": branch_name}
    response = requests.post(jenkins_url, auth=jenkins_auth, params=build_params, verify=False, proxies=proxies)
    response.raise_for_status()
    print(f"Triggered Jenkins build for branch: {branch_name}")

def main():
    # Initial test request to the root URL with proxy and SSL verification disabled
    response = requests.get('https://bitbucket.com', proxies=proxies, verify=False)
    response.raise_for_status()

    known_branches = get_branches()
    print("Monitoring for new branches...")

    while True:
        time.sleep(branch_check_interval)
        current_branches = get_branches()

        new_branches = current_branches - known_branches
        if new_branches:
            for branch in new_branches:
                print(f"New branch detected: {branch}")
                trigger_jenkins_build(branch)
            known_branches = current_branches

if __name__ == "__main__":
    main()
