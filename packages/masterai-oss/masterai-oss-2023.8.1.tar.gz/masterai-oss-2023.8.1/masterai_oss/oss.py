
import logging
from typing import Iterable, Union, IO, Optional

import boto3
import botocore.config
from botocore.exceptions import ClientError

from .models import (
    CopyObjectResponse,
    PutObjectResponse,
    DeleteObjectResponse,
    HeadObjectResponse,
    GetObjectResponse,
    ListObjectResponse,
    ListObjectV2Response,
    ObjectSummary,
    OwnerObj
)


logger = logging.getLogger(__name__)



class S3Client(object):

    def __init__(
        self,
        access_key: str,
        secret_key: str,
        bucket_name: str,
        endpoint: str = 'http://aoss-internal.cn-sh-01.sensecoreapi-oss.cn',
        max_pool_connections: int = 256,
        proxies: dict = None
    ) -> None:
        self._bucket_name = bucket_name
        service_name = 's3'
        kwargs: dict = {
            "service_name": service_name,
            "endpoint_url": endpoint,
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "config": botocore.config.Config(max_pool_connections=max_pool_connections, proxies=proxies)
        }
        self.s3_client = boto3.client(**kwargs)
        self.s3_resource_service_client = boto3.resource(**kwargs)
        self.s3_bucket = self.s3_resource_service_client.Bucket(bucket_name)

    @staticmethod
    def _drop_none_value(data: dict) -> dict:
        return {k: v for k, v in data.items() if v is not None}

    def copy_object(
            self,
            key: str,
            copy_source_key: str,
            copy_source_bucket: str = None,
            content_type: str = None,
            meta_data: dict = None,
    ) -> CopyObjectResponse:
        """
        Creates a copy of an object that is already stored in Amazon S3.
        """
        kws: dict = {
            "Metadata": meta_data,
            "ContentType": content_type,
        }
        response: dict = self.s3_client.copy_object(
            Bucket=self._bucket_name,
            CopySource={
                "Bucket": copy_source_bucket or self._bucket_name,
                "Key": copy_source_key
            },
            Key=key,
            **self._drop_none_value(kws)
        )
        return CopyObjectResponse(**response)

    def delete_object(self, key: str) -> DeleteObjectResponse:
        """
        Removes the null version (if there is one) of an object and inserts a delete marker, which becomes the latest version of the object. If there isn't a null version, Amazon S3 does not remove any objects but will still respond that the command was successful.
        """
        response: dict = self.s3_client.delete_object(
            Bucket=self._bucket_name,
            Key=key
        )
        return DeleteObjectResponse(**response)

    def get_object(self, key: str) -> GetObjectResponse:
        """
        Retrieves objects from Amazon S3. To use ``GET`` , you must have ``READ`` access to the object. If you grant ``READ`` access to the anonymous user, you can return the object without using an authorization header.
        """
        response: dict = self.s3_client.get_object(
            Bucket=self._bucket_name,
            Key=key
        )
        return GetObjectResponse(**response)

    def head_object(self, key: str) -> HeadObjectResponse:
        """
        The HEAD action retrieves metadata from an object without returning the object itself. This action is useful if you're only interested in an object's metadata. To use HEAD, you must have READ access to the object.
        """
        response: dict = self.s3_client.head_object(
            Bucket=self._bucket_name,
            Key=key
        )
        return HeadObjectResponse(**response)

    def put_object(
            self,
            key: str,
            body: Union[bytes, IO],
            meta_data: dict = None,
            content_type: str = None
    ) -> PutObjectResponse:
        """
        Adds an object to a bucket. You must have WRITE permissions on a bucket to add an object to it.
        """
        kws: dict = {
            "Metadata": meta_data,
            "ContentType": content_type,
        }
        response: dict = self.s3_client.put_object(
            Bucket=self._bucket_name,
            Key=key,
            Body=body,
            **self._drop_none_value(kws)
        )
        return PutObjectResponse(**response)

    def list_objects(
            self,
            prefix: str = None,
            delimiter: str = '/',
            encoding_type: str = None,
            marker: str = None,
            max_keys: int = 1000
    ) -> ListObjectResponse:
        """
        Returns some or all (up to 1,000) of the objects in a bucket. You can use the request parameters as selection criteria to return a subset of the objects in a bucket. A 200 OK response can contain valid or invalid XML. Be sure to design your application to parse the contents of the response and handle it appropriately.
        """
        kws: dict = {
            "Delimiter": delimiter,
            "EncodingType": encoding_type,
            "Marker": marker,
            "MaxKeys": max_keys,
            "Prefix": prefix
        }
        response = self.s3_client.list_objects(
            Bucket=self._bucket_name,
            **self._drop_none_value(kws)
        )
        return ListObjectResponse(**response)

    def list_objects_v2(
            self,
            prefix: str = None,
            delimiter: str = '/',
            encoding_type: str = None,
            marker: str = None,
            max_keys: int = 1000,
            start_after: str = None
    ) -> ListObjectV2Response:
        """
        Returns some or all (up to 1,000) of the objects in a bucket with each request. You can use the request parameters as selection criteria to return a subset of the objects in a bucket. A ``200 OK`` response can contain valid or invalid XML. Make sure to design your application to parse the contents of the response and handle it appropriately. Objects are returned sorted in an ascending order of the respective key names in the list. For more information about listing objects, see `Listing object keys programmatically <https://docs.aws.amazon.com/AmazonS3/latest/userguide/ListingKeysUsingAPIs.html>`__
        """
        kws: dict = {
            "Delimiter": delimiter,
            "EncodingType": encoding_type,
            "Marker": marker,
            "MaxKeys": max_keys,
            "Prefix": prefix,
            "StartAfter": start_after,
        }
        response = self.s3_client.list_objects_v2(
            Bucket=self._bucket_name,
            **self._drop_none_value(kws)
        )
        return ListObjectV2Response(**response)

    @staticmethod
    def _summary_obj2object_summary(obj: object) -> ObjectSummary:
        summary: ObjectSummary = ObjectSummary(
            bucket_name=obj.bucket_name,
            checksum_algorithm=obj.checksum_algorithm,
            e_tag=obj.e_tag,
            key=obj.key,
            last_modified=obj.last_modified,
            size=obj.size,
            storage_class=obj.storage_class,
            owner=OwnerObj(
                DisplayName=obj.owner["DisplayName"],
                ID=obj.owner["ID"]
            )
        )
        return summary
    
    def filter(
            self,
            prefix: str,
            delimiter: str = "/",
            encoding_type: str = None,
            marker: str = None,
            max_keys: int = None
    ) -> Iterable[ObjectSummary]:
        """
        Creates an iterable of all ObjectSummary resources in the collection filtered by kwargs passed to method. A ObjectSummary collection will include all resources by default if no filters are provided, and extreme caution should be taken when performing actions on all resources.
        """
        kws: dict = {
            "Delimiter": delimiter,
            "EncodingType": encoding_type,
            "Marker": marker,
            "MaxKeys": max_keys,
            "Prefix": prefix,
        }
        for obj in self.s3_bucket.objects.filter(**self._drop_none_value(kws)):
            obj: object
            yield self._summary_obj2object_summary(obj)

    def all(self) -> Iterable[ObjectSummary]:
        """
        Creates an iterable of all ObjectSummary resources in the collection.
        """
        for obj in self.s3_bucket.objects.all():
            obj: object
            yield self._summary_obj2object_summary(obj)

    def download_file(self, key: str, file_name: str) -> None:
        """
        Download an S3 object to a file.
        """
        self.s3_client.download_file(
            Bucket=self._bucket_name,
            Key=key,
            Filename=file_name
        )

    def download_fileobj(self, key: str, file_obj: IO) -> None:
        """
        The file-like object must be in binary mode.
        """
        self.s3_client.download_fileobj(
            Bucket=self._bucket_name,
            Key=key,
            Fileobj=file_obj
        )

    def upload_file(self, key: str, file_name: str):
        """
        Upload a file to an S3 object.
        """
        self.s3_client.upload_file(
            Filename=file_name,
            Bucket=self._bucket_name,
            Key=key
        )

    def upload_fileobj(self, key: str, file_obj: IO):
        """
        Upload a file-like object to S3.

        The file-like object must be in binary mode.
        
        This is a managed transfer which will perform a multipart upload in
        multiple threads if necessary.
        """
        self.s3_client.upload_fileobj(
            Fileobj=file_obj,
            Bucket=self._bucket_name,
            Key=key
        )

    def check_object_exist(self, key: str) -> bool:
        try:
            self.head_object(key)
        except ClientError as e:
            return int(e.response['Error']['Code']) != 404
        return True

    def upload_if_not_exist(
            self,
            key: str,
            body: bytes,
            meta_data: dict = None,
            content_type: str = None
    ) -> Optional[PutObjectResponse]:
        if self.check_object_exist(key):
            return
        response: PutObjectResponse = self.put_object(
            key,
            body=body,
            meta_data=meta_data,
            content_type=content_type
        )
        return response
