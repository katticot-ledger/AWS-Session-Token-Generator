import subprocess
import json
import argparse
from identityAWS import get_caller_identity

# Dictionary mapping profiles to ARNs
ARN_MAPPING = {
    "prd": None,
    "stg": None,
    "sbx": None
}

OTP_MAPPING = {
    "prd": "kr2lkm5hsggz5qmcf2llpkhtwa",
    "stg": "jvwqxreqgbtcosbishgnhdx5yy",
    "sbx": "7z4njvchxglkewv2rovwrfpjwi"
}

def update_arn_mapping():
    for profile in ARN_MAPPING.keys():
        identity = get_caller_identity(profile)
        if 'Arn' in identity:
            modified_arn = identity['Arn'].replace(':user/', ':mfa/')
            ARN_MAPPING[profile] = modified_arn

def get_otp_from_1password(profile):
    item_id = OTP_MAPPING.get(profile)
    if not item_id:
        print(f"Error: Invalid profile - {profile}")
        return None

    try:
        cmd_output = subprocess.check_output(["op", "item", "get", item_id, "--otp"], text=True)
        return cmd_output.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None

def get_aws_session_token(profile):
    otp = get_otp_from_1password(profile)
    if not otp:
        return None

    arn = ARN_MAPPING.get(profile)
    if not arn:
        print(f"Error: Invalid profile - {profile}")
        return None

    cmd = [
        "aws", "sts", "get-session-token", 
        "--serial-number", arn, 
        "--token-code", otp, 
        "--profile", profile
    ]

    try:
        aws_output = subprocess.check_output(cmd, text=True)
        aws_json = json.loads(aws_output)

        access_key = aws_json['Credentials']['AccessKeyId']
        secret_key = aws_json['Credentials']['SecretAccessKey']
        session_token = aws_json['Credentials']['SessionToken']

        export_commands = [
            f"export AWS_ACCESS_KEY_ID={access_key}",
            f"export AWS_SECRET_ACCESS_KEY={secret_key}",
            f"export AWS_SESSION_TOKEN={session_token}"
        ]

        return export_commands

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None

def write_to_file(export_commands, filename="aws_exports.sh"):
    with open(filename, 'w') as file:
        for line in export_commands:
            file.write(line + "\n")

# Update ARN mapping
update_arn_mapping()

# Command-line argument parsing
parser = argparse.ArgumentParser(description="Get AWS session token based on profile.")
parser.add_argument("profile", help="Profile name (e.g., prd, stg, sbx)", choices=["prd", "stg", "sbx"])
args = parser.parse_args()

aws_credentials = get_aws_session_token(args.profile)
if aws_credentials:
    write_to_file(aws_credentials)
    print(f"Export commands written to aws_exports.sh")
