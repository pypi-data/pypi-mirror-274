import argparse
import os
import subprocess
import signal
# import boto3
# from botocore.exceptions import NoCredentialsError, ClientError

def usage():
    print("Usage: python script.py [-i image] [-u registry_username] [-p registry_password] [-r registry_url] [-l] [-s]")
    print(" -i      The image to apply a STIG to. This is required")
    print(" -u      The username for an image in a private registry. This is optional.")
    print(" -p      The password for an image in a private registry. This is optional.")
    print(" -r      The URL for a private registry. This is optional.")
    print(" -s      Allow insecure registries or registries with custom certs")
    print(" -l      Detected local image. Running in local mode.")
    print(" -h      Print usage info.")
    exit(1)

# def upload_to_s3(bucket_name, file):
#     """
#     Upload files from a specified directory to an AWS S3 bucket.

#     :param bucket_name: Name of the S3 bucket.
#     :param directory: Directory containing files to upload.
#     """
#     # Check if the directory exists
#     if not os.path.exists(file):
#         print(f"Error: Directory '{directory}' does not exist.")
#         return

#     # Initialize S3 client with custom credentials
#     s3 = boto3.client('s3')

#     try:
#         # Walk through the directory and upload files
#         file_path = file
#         s3.upload_file(file_path, bucket_name, file_path)
#         print(f"Uploaded '{file_path}' to '{bucket_name}' bucket.")
#     except NoCredentialsError:
#         print("Error: AWS credentials not found.")
#     except ClientError as e:
#         print(f"Error: {e}")

def main():
    parser = argparse.ArgumentParser(description="Apply STIG to a Docker image.")
    parser.add_argument("-u", dest="username", help="The username for an image in a private registry.")
    parser.add_argument("-p", dest="password", help="The password for an image in a private registry.")
    parser.add_argument("-r", dest="url", help="The URL for a private registry.")
    parser.add_argument("-i", dest="image", help="The image to apply a STIG to. This is required.", required=True)
    parser.add_argument("-l", dest="local", action="store_true", help="Detected local image. Running in local mode.")
    parser.add_argument("-s", dest="insecure", action="store_true", help="Allow insecure registries or registries with custom certs.")
    # parser.add_argument("-a", dest="aws_s3_bucket_upload", help="Upload results to S3 bucket. AWS cli must be configured to access the destination S3 bucket")
    
    args = parser.parse_args()

    if not args.image:
        usage()

    dir_name = args.image.replace("/", "-").replace(":", "-")
    os.makedirs(f"stig-results/{dir_name}", exist_ok=True)

    subprocess.run(["docker", "volume", "create", "stig-runner"])

    def cleanup_volume(signum, frame):
        subprocess.run(["docker", "volume", "rm", "stig-runner"])
        exit(1)

    signal.signal(signal.SIGINT, cleanup_volume)

    if args.local:
        print("Detected local image. Running in local mode.")
        subprocess.run(["docker", "save", args.image, "-o", "./local-image.tar.gz"])
        subprocess.run(["docker", "run", "-t", "--rm", "--privileged",
                        "-e", f"SCAN_IMAGE={args.image}",
                        "-e", f"INSECURE_REG={args.insecure}",
                        "--name", "stig-runner",
                        "-v", f"{os.getcwd()}/local-image.tar.gz:/etc/local-image.tar.gz:ro",
                        "-v", f"{os.getcwd()}/stig-results/{dir_name}:/tmp",
                        "anchore/static-stig:0.1.10"])
        os.remove("local-image.tar.gz")
    elif not args.username:
        subprocess.run(["docker", "run", "-t", "--rm", "--privileged",
                        "-e", f"SCAN_IMAGE={args.image}",
                        "-e", f"INSECURE_REG={args.insecure}",
                        "--name", "stig-runner",
                        "-v", f"{os.getcwd()}/stig-results/{dir_name}:/tmp",
                        "anchore/static-stig:0.1.10"])
    else:
        subprocess.run(["docker", "run", "-t", "--rm", "--privileged",
                        "-e", f"SCAN_IMAGE={args.image}",
                        "-e", f"INSECURE_REG={args.insecure}",
                        "-e", f"REGISTRY_USERNAME={args.username}",
                        "-e", f"REGISTRY_PASSWORD={args.password}",
                        "-e", f"REGISTRY_URL={args.url}",
                        "--name", "stig-runner",
                        "-v", f"{os.getcwd()}/stig-results/{dir_name}:/tmp",
                        "anchore/static-stig:0.1.10"])
                        
    subprocess.run(["docker", "run", "--rm", "-it",
                    "-v", f"{os.getcwd()}/stig-results/{dir_name}:/share",
                    "docker.io/mitre/saf:1.4.5", "convert", "xccdf_results2hdf",
                    "--input", "/share/xccdf-results.xml",
                    "--output", "/share/hdf-results.json"])                    

    # if args.aws_s3_bucket_upload:
    #     for file in os.listdir(f"{os.getcwd()}/stig-results/{dir_name}"):
    #         upload_to_s3(args.aws_s3_bucket_upload, f"stig-results/{dir_name}/{file}")


if __name__ == "__main__":
    main()
