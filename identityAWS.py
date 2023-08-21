import subprocess
import json
import sys

def run_aws_command(command):
    try:
        response = subprocess.check_output(command, stderr=subprocess.STDOUT, universal_newlines=True)
        return json.loads(response)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"An error occurred: {e.output}")
    except json.JSONDecodeError:
        raise ValueError(f"Failed to parse JSON response for command: {' '.join(command)}")

def get_caller_identity(profile_name):
    command = ["aws", "sts", "get-caller-identity", "--profile", profile_name]
    return run_aws_command(command)

def extract_identity_info(identity_dict):
    return [
        identity_dict.get('UserId', 'N/A'),
        identity_dict.get('Account', 'N/A'),
        identity_dict.get('Arn', 'N/A')
    ]

def get_caller_identities_for_profiles(profile_names):
    identities = {}
    for profile_name in profile_names:
        try:
            identity_info = get_caller_identity(profile_name)
            identities[profile_name] = extract_identity_info(identity_info)
        except (RuntimeError, ValueError) as e:
            print(f"Error for profile '{profile_name}': {e}")
    return identities

def display_identities(identities_dict):
    for profile_name, identity in identities_dict.items():
        print(f"Identity for profile '{profile_name}':")
        print(f"UserId: {identity[0]}")
        print(f"Account: {identity[1]}")
        print(f"Arn: {identity[2]}")
        print('-'*40)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python <script_name>.py <aws_profile_name1> <aws_profile_name2> ...")
        sys.exit(1)

    profile_names = sys.argv[1:]
    identities_dict = get_caller_identities_for_profiles(profile_names)
    display_identities(identities_dict)
