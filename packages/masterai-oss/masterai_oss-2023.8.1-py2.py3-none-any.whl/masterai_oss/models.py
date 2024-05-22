from typing import Any, List
from pydantic import BaseModel

from datetime import datetime



class ResponseMetadata(BaseModel):
    RequestId: str = None
    HostId: str = None
    HTTPStatusCode: int = None
    HTTPHeaders: dict = None
    RetryAttempts: int = None

    class BaseConfig:
        extra = 'allow'
        use_enum_values = True


class BaseObjectResult(BaseModel):
    ETag: str = None
    LastModified: datetime = None

    class BaseConfig:
        extra = 'allow'
        use_enum_values = True


class CopyObjectResponse(BaseModel):
    """
    {
        "ResponseMetadata": {
            "RequestId": "tx00000000000000006e650-00649d4016-23ab6da1-cn-sh-01-01",
            "HostId": "",
            "HTTPStatusCode": 200,
            "HTTPHeaders": {
                "x-amz-request-id": "tx00000000000000006e650-00649d4016-23ab6da1-cn-sh-01-01",
                "content-type": "application/xml",
                "content-length": "221",
                "date": "Thu, 29 Jun 2023 08:25:58 GMT"
            },
            "RetryAttempts": 0
        },
        "CopyObjectResult": {
            "ETag": "931e2bc22001b568ed1edf7bfcf9cf66",
            "LastModified": datetime.datetime(2023, 6, 29, 8, 25, 58, 76000, tzinfo=tzutc())
        }
    }
    """
    ResponseMetadata: ResponseMetadata
    CopyObjectResult: BaseObjectResult


class PutObjectResponse(BaseModel):
    """
    {
        "ResponseMetadata": {
            "RequestId": "tx0000000000000002b8f7f-00649d4461-239d8eb7-cn-sh-01-01",
            "HostId": "",
            "HTTPStatusCode": 200,
            "HTTPHeaders": {
                "content-length": "0",
                "etag": "9336ebf25087d91c818ee6e9ec29f8c1",
                "accept-ranges": "bytes",
                "x-amz-request-id": "tx0000000000000002b8f7f-00649d4461-239d8eb7-cn-sh-01-01",
                "date": "Thu, 29 Jun 2023 08:44:17 GMT"
            },
            "RetryAttempts": 0
        },
        "ETag": "9336ebf25087d91c818ee6e9ec29f8c1"
    }
    """
    ResponseMetadata: ResponseMetadata
    ETag: str = None


class DeleteObjectResponse(BaseModel):
    """
    {
        "ResponseMetadata": {
            "RequestId": "tx0000000000000002b8f7f-00649d4461-239d8eb7-cn-sh-01-01",
            "HostId": "",
            "HTTPStatusCode": 200,
            "HTTPHeaders": {
                "content-length": "0",
                "etag": "9336ebf25087d91c818ee6e9ec29f8c1",
                "accept-ranges": "bytes",
                "x-amz-request-id": "tx0000000000000002b8f7f-00649d4461-239d8eb7-cn-sh-01-01",
                "date": "Thu, 29 Jun 2023 08:44:17 GMT"
            },
            "RetryAttempts": 0
        },
        "ETag": "9336ebf25087d91c818ee6e9ec29f8c1"
        "DeleteMarker": True|False,
        "VersionId": 'string',
        "RequestCharged": 'requester'
    }
    """
    ResponseMetadata: ResponseMetadata
    ETag: str = None
    DeleteMarker: bool = None
    VersionId: str = None
    RequestCharged: str = None


class HeadObjectResponse(BaseModel):
    """
    {
        "ResponseMetadata": {
            "RequestId": "tx00000000000000013e927-00649d3222-23a1d8f6-cn-sh-01-01",
            "HostId": "",
            "HTTPStatusCode": 200,
            "HTTPHeaders": {
                "content-length": "146341",
                "accept-ranges": "bytes",
                "last-modified": "Thu, 29 Jun 2023 01:27:53 GMT",
                "etag": "931e2bc22001b568ed1edf7bfcf9cf66",
                "x-amz-storage-class": "STANDARD",
                "x-amz-request-id": "tx00000000000000013e927-00649d3222-23a1d8f6-cn-sh-01-01",
                "content-type": "binary/octet-stream",
                "date": "Thu, 29 Jun 2023 07:26:26 GMT"
            },
            "RetryAttempts": 0
        },
        "AcceptRanges": "bytes",
        "LastModified": datetime.datetime(2023,6,29,1,27,53, tzinfo=tzutc()),
        "ContentLength": 146341,
        "ETag": "931e2bc22001b568ed1edf7bfcf9cf66",
        "ContentType": "binary/octet-stream",
        "Metadata": {},
        "StorageClass": "STANDARD"
    }
    """
    ResponseMetadata: ResponseMetadata
    AcceptRanges: str = None
    LastModified: datetime = None
    ContentLength: int = None
    ETag: str = None
    ContentType: str = None
    Metadata: dict = None
    StorageClass: str = None


class GetObjectResponse(BaseModel):
    """
    {
        "ResponseMetadata": {
            "RequestId": "tx000000000000000063b84-00649d4b7b-23ac0002-cn-sh-01-01",
            "HostId": "",
            "HTTPStatusCode": 200,
            "HTTPHeaders": {
                "content-length": "2",
                "accept-ranges": "bytes",
                "last-modified": "Thu, 29 Jun 2023 08:44:17 GMT",
                "etag": "9336ebf25087d91c818ee6e9ec29f8c1",
                "x-amz-storage-class": "STANDARD",
                "x-amz-request-id": "tx000000000000000063b84-00649d4b7b-23ac0002-cn-sh-01-01",
                "content-type": "binary/octet-stream",
                "date": "Thu, 29 Jun 2023 09:14:35 GMT"
            },
            "RetryAttempts": 0
        },
        "AcceptRanges": "bytes",
        "LastModified": datetime.datetime(2023, 6, 29, 8, 44, 17, tzinfo=tzutc()),
        "ContentLength": 2,
        "ETag": "9336ebf25087d91c818ee6e9ec29f8c1",
        "ContentType": "binary/octet-stream",
        "Metadata": {},
        "StorageClass": "STANDARD",
        "Body": <botocore.response.StreamingBody object at 0x7fd9447509a0>
    }
    """
    ResponseMetadata: ResponseMetadata
    AcceptRanges: str = None
    LastModified: datetime = None
    ContentLength: int = None
    ETag: str = None
    ContentType: str = None
    Metadata: dict = None
    StorageClass: str = None
    Body: Any = None


class CommonPrefixeObj(BaseModel):
    Prefix: str = None


class OwnerObj(BaseModel):
    DisplayName: str = None
    ID: str = None


class ContentObj(BaseModel):
    Key: str = None
    LastModified: datetime = None
    ETag: str = None
    Size: int = None
    StorageClass: str = None
    Owner: OwnerObj = None


class ListObjectResponse(BaseModel):
    """
    {
        "ResponseMetadata": {
            "RequestId": "tx0000000000000002dd817-00649d52ae-23a6f20d-cn-sh-01-01",
            "HostId": "",
            "HTTPStatusCode": 200,
            "HTTPHeaders": {
                "x-amz-request-id": "tx0000000000000002dd817-00649d52ae-23a6f20d-cn-sh-01-01",
                "content-type": "application/xml",
                "content-length": "703",
                "date": "Thu, 29 Jun 2023 09:45:25 GMT"
            },
            "RetryAttempts": 0
        },
        "IsTruncated": True,
        "Marker": "",
        "NextMarker": "README.md",
        "Contents": [
            {
                "Key": "README.md",
                "LastModified": datetime.datetime(2023, 4, 3, 3, 38, 1, 20000, tzinfo=tzutc()),
                "ETag": "1c868aaa0888e198d89f716fcafde332",
                "Size": 78,
                "StorageClass": "STANDARD",
                "Owner": {
                    "DisplayName": "f0a978ca-fe91-4240-bfb3-f8006a262e6c",
                    "ID": "f0a978ca-fe91-4240-bfb3-f8006a262e6c"
                }
            }
        ],
        "Name": "opendata",
        "Prefix": "",
        "Delimiter": "/",
        "MaxKeys": 2,
        "CommonPrefixes": [
            {
                "Prefix": "LAION5B/"
            }
        ],
        "EncodingType": "url"
    }
    """
    ResponseMetadata: ResponseMetadata
    IsTruncated: bool = None
    Marker: str = None
    NextMarker: str = None
    Contents: List[ContentObj] = None
    Name: str = None
    Prefix: str = None
    Delimiter: str = None
    MaxKeys: int = None
    CommonPrefixes: List[CommonPrefixeObj] = None
    EncodingType: str = None


class ListObjectV2Response(BaseModel):
    """
    {
        "ResponseMetadata": {
            "RequestId": "tx0000000000000000a6be1-00649d54bd-23ab6da1-cn-sh-01-01",
            "HostId": "",
            "HTTPStatusCode": 200,
            "HTTPHeaders": {
                "x-amz-request-id": "tx0000000000000000a6be1-00649d54bd-23ab6da1-cn-sh-01-01",
                "content-type": "application/xml",
                "content-length": "703",
                "date": "Thu, 29 Jun 2023 09:54:17 GMT"
            },
            "RetryAttempts": 0
        },
        "IsTruncated": True,
        "Contents": [
            {
                "Key": "README.md",
                "LastModified": datetime.datetime(2023, 4, 3, 3, 38, 1, 20000, tzinfo=tzutc()),
                "ETag": "1c868aaa0888e198d89f716fcafde332",
                "Size": 78,
                "StorageClass": "STANDARD",
                "Owner": {
                    "DisplayName": "f0a978ca-fe91-4240-bfb3-f8006a262e6c",
                    "ID": "f0a978ca-fe91-4240-bfb3-f8006a262e6c"
                }
            }
        ],
        "Name": "opendata",
        "Prefix": "",
        "Delimiter": "/",
        "MaxKeys": 2,
        "CommonPrefixes": [
            {
                "Prefix": "LAION5B/"
            }
        ],
        "EncodingType": "url"
    }
    """
    ResponseMetadata: ResponseMetadata
    IsTruncated: bool = None
    Marker: str = None
    NextMarker: str = None
    Contents: List[ContentObj] = None
    Name: str = None
    Prefix: str = None
    Delimiter: str = None
    MaxKeys: int = None
    CommonPrefixes: List[CommonPrefixeObj] = None
    EncodingType: str = None


class ObjectSummary(BaseModel):
    bucket_name: str = None
    checksum_algorithm: str = None
    e_tag: str = None
    key: str = None
    last_modified: datetime = None
    size: int = None
    storage_class: str = None
    owner: OwnerObj = None
