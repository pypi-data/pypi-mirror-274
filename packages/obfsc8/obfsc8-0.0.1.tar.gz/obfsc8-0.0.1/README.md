## obfsc8: Obfuscate CSV file data within Amazon S3
**obfsc8** provides a simple way to obfuscate specific fields within CSV files that are stored in the Amazon S3 service.
Designed to be used within Amazon Lambda, EC2 and ECS services, **obfsc8** returns a bytes object of the obfuscated file data that
can be easily processed, for example by the boto3 S3.Client.put_object function.


## Setup
Install the latest version of obfsc8 with:
```
pip install obfsc8
```