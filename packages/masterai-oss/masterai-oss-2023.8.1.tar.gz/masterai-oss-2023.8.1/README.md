# masterai-oss
> 基于[boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html)封装, 返回值更加清晰


## 支持

### 原生函数
1. copy_object
1. delete_object
1. get_object
1. head_object
1. put_object
1. list_objects
1. list_objects_v2
1. filter
1. all
1. download_file
1. download_fileobj
1. upload_file
1. upload_fileobj

### 扩展函数
1. check_object_exist
1. upload_if_not_exist


#### 使用方式
```python
from masterai_oss import S3Client, PutObjectResponse, HeadObjectResponse

client = S3Client(
    access_key="your access_key",
    secret_key="your secret_key",
    bucket_name="your bucket_name",
    endpoint="your endpoint",
)

key = "path/of/obj.suffix"
put_response: PutObjectResponse = client.put_object(
    key=key,
    body=b"file content",
)

head_response: HeadObjectResponse = client.head_object(
    key=key
)
print(head_response.ContentLength)
```