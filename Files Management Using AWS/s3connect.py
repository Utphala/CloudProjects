import boto3
import botocore
import time

# Creating Connection
s3 = boto3.resource('s3')
print 'Connection established!!'

bucket_name = "aws-cse6331-utphala"
# Creating bucket
s3.create_bucket(Bucket='aws-cse6331-utphala')
s3.create_bucket(Bucket='aws-cse6331-utphala', CreateBucketConfiguration={
    'LocationConstraint': 'us-east-1'})

print 'Bucket ' + bucket_name +'created succesfully!!'


# Accessing the bucket
bucket = s3.Bucket('aws-cse6331-utphala')
exists = True
try:
    s3.meta.client.head_bucket(Bucket='aws-cse6331-utphala')
except botocore.exceptions.ClientError as e:
    # If a client error is thrown, then check that it was a 404 error.
    # If it was a 404 error, then the bucket does not exist.
    error_code = int(e.response['Error']['Code'])
    if error_code == 404:
        exists = False

#Start timer
startTime = int(time.time())
print 'start time is' + str(time.clock())

#Storing data
#s3.Object('aws-cse6331-utphala', 'data/all_month.csv').put(Body=open('/Users/Chethan/Downloads/all_month.csv', 'rb'))

#End timer
endTime = int(time.time())
print 'end time is' + str(time.clock())

totalTime = endTime - startTime
print 'Time to load data into S3 is '+str(totalTime)+' seconds'

# Access control
bucket.Acl().put(ACL='public-read')
obj = bucket.Object('data/all_month.csv')
obj.Acl().put(ACL='public-read')

# Iteration of buckets and key
for bucket in s3.buckets.all():
    for key in bucket.objects.all():
        print(key.key)

# Deleting a bucket

for key in bucket.objects.all():
    key.delete()
bucket.delete()
