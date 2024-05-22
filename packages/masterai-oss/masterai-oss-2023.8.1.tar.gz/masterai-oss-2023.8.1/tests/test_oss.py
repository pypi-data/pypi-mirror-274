import os
import unittest
import tempfile
from io import BytesIO
from datetime import date

from masterai_oss import (
    S3Client,
    CopyObjectResponse,
    PutObjectResponse,
    DeleteObjectResponse,
    GetObjectResponse,
    ListObjectResponse,
    ListObjectV2Response,
    ObjectSummary
)


class TestOss(unittest.TestCase):

    def setUp(self):
        self.oss: S3Client = S3Client(
            access_key=os.environ["ACCESS_KEY"],
            secret_key=os.environ["SECRET_KEY"],
            bucket_name=os.environ["BUCKET_NAME"],
            endpoint='https://aoss.cn-sh-01.sensecoreapi-oss.cn',
        )
        self.key: str = f"crawl/test/{date.today()}.txt"
        self.copy_source_key = f"{self.key}.copy"
        self.body: bytes = f"{date.today()}".encode()

        self.oss.put_object(
            self.key,
            body=self.body
        )

    def tearDown(self):
        if self.oss.check_object_exist(self.key):
            self.oss.delete_object(key=self.key)
        if self.oss.check_object_exist(self.copy_source_key):
            self.oss.delete_object(key=self.copy_source_key)

    def test_put_object_with_bytes(self):
        response: PutObjectResponse = self.oss.put_object(
            self.key,
            body=self.body
        )
        self.assertEqual(response.ResponseMetadata.HTTPStatusCode, 200)

    def test_put_object_with_io(self):
        response: PutObjectResponse = self.oss.put_object(
            self.key,
            body=BytesIO(self.body),
            content_type="application/json"
        )
        self.assertEqual(response.ResponseMetadata.HTTPStatusCode, 200)

    def test_copy_object(self):
        response: CopyObjectResponse = self.oss.copy_object(
            self.copy_source_key,
            copy_source_key=self.key
        )
        self.assertEqual(response.ResponseMetadata.HTTPStatusCode, 200)
        self.assertEqual(self.oss.check_object_exist(self.copy_source_key), True)

    def test_delete_object(self):
        response: DeleteObjectResponse = self.oss.delete_object(
            self.key
        )
        self.assertEqual(response.ResponseMetadata.HTTPStatusCode, 204)

    def test_get_object(self):
        response: GetObjectResponse = self.oss.get_object(
            self.key
        )
        self.assertEqual(response.ResponseMetadata.HTTPStatusCode, 200)
        self.assertEqual(response.Body.read(), self.body)

    def test_list_objects(self):
        max_keys = 2
        response: ListObjectResponse = self.oss.list_objects(max_keys=2)
        self.assertEqual(response.ResponseMetadata.HTTPStatusCode, 200)
        self.assertEqual(len(response.CommonPrefixes), max_keys)

    def test_list_objects_v2(self):
        max_keys = 2
        response: ListObjectV2Response = self.oss.list_objects_v2(max_keys=max_keys)
        self.assertEqual(response.ResponseMetadata.HTTPStatusCode, 200)
        self.assertEqual(len(response.CommonPrefixes), max_keys)

    def test_download_file(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            file_name = "tmp.file"
            fp = f"{tmpdirname}/{file_name}"
            self.oss.download_file(self.key, fp)
            fp_content = open(fp, 'rb').read()
            self.assertEqual(self.body, fp_content)

    def test_download_fileobj(self):
        with tempfile.TemporaryFile() as fp:
            self.oss.download_fileobj(self.key, fp)
            fp.seek(0)
            fp_content = fp.read()
            self.assertEqual(self.body, fp_content)

    def test_upload_file(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            file_name = "tmp.file"
            fp = f"{tmpdirname}/{file_name}"
            with open(fp, 'wb+') as f:
                f.write(self.body)
            self.oss.upload_file(self.key, fp)

            response: GetObjectResponse = self.oss.get_object(
                self.key
            )
            self.assertEqual(self.body, response.Body.read())

    def test_upload_fileobj(self):
        with tempfile.TemporaryFile() as fp:
            fp.write(self.body)
            fp.seek(0)
            self.oss.upload_fileobj(self.key, fp)

            response: GetObjectResponse = self.oss.get_object(
                self.key
            )
            self.assertEqual(self.body, response.Body.read())

    def test_all(self):
        obj = None
        for obj in self.oss.all():
            obj: ObjectSummary
            break
        self.assertIsNotNone(obj)

    def test_filter(self):
        obj = None
        prefix: str = self.key.rsplit('/', 1)[0] + '/'
        for obj in self.oss.filter(prefix=prefix):
            obj: ObjectSummary
            break
        self.assertIsNotNone(obj)
