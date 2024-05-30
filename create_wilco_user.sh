#!/bin/bash

# Get the default region from AWS CLI configuration
region=$(aws configure get region)

# Step 1: Create the IAM user
aws iam create-user --user-name wilco

# Step 2: Create access key for the user and capture the output
output=$(aws iam create-access-key --user-name wilco)

# Extract AccessKeyId and SecretAccessKey from the output
AccessKeyId=$(echo $output | jq -r '.AccessKey.AccessKeyId')
SecretAccessKey=$(echo $output | jq -r '.AccessKey.SecretAccessKey')

# Step 3: Attach the AmazonS3ReadOnlyAccess policy to the user
aws iam attach-user-policy --user-name wilco --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess

# Print the Access Key ID, Secret Access Key, and Region in the specified format
echo "Your credentials are: $AccessKeyId:$SecretAccessKey:$region"
