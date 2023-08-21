# AWS Session Token Generator README

This script is designed to streamline the process of fetching an AWS session token by leveraging both AWS CLI and 1Password CLI. It makes use of ARNs mapped to AWS profiles and 1Password OTP UUIDs.

## Prerequisites

1. **AWS CLI**: This is the command-line interface tool to manage your AWS services. You can install it following the [official guide](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html).

2. **1Password CLI**: Version 8 of the command-line tool for 1Password. You can get it from [1Password's official download page](https://1password.com/downloads/command-line/).

## Configuration

1. **AWS Profile**: Set up your AWS CLI with the profile names you intend to use. For example:
   ```bash
   aws configure --profile prd
   ```

2. **1Password OTP UUID**: If you're using 1Password's One-Time Password (OTP) feature, each item will have a unique UUID associated with the OTP. This UUID is essential for our script to fetch the OTP.

3. **Updating the Script**:
   - Populate the `ARN_MAPPING` dictionary with your AWS profile aliases as keys. The script will automatically update the ARN values by calling the `identityAWS.py` script.
   - In the `OTP_MAPPING` dictionary, map your AWS profile names to the respective 1Password OTP UUIDs.

## Usage

Run the script with the desired AWS profile name:

```bash
python main.py <aws_profile_name>
```

Replace `<aws_profile_name>` with your AWS profile name like `prd`, `stg`, or `sbx`.

Upon successful execution, the script will generate an `aws_exports.sh` file with the necessary `export` commands for `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and `AWS_SESSION_TOKEN`. 

## Post-execution

To utilize the generated AWS session credentials in your terminal, source the `aws_exports.sh` file:

```bash
source aws_exports.sh
```

This command will set the AWS session credentials as environment variables in your terminal session, allowing you to use AWS CLI commands with the session token.

## Note

- Ensure that your AWS profiles and 1Password OTP UUIDs are correctly configured in the script for accurate results.
- The script will update the ARN value to replace the `:user/` segment with `:mfa/` to adhere to your specific requirements.
