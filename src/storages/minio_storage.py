from datetime import timedelta

from minio import Minio
from minio.commonconfig import Tags


class MinioClient:
    def __init__(
            self,
            client: Minio
    ):
        self.__client = client

    def presign_object(
            self,
            bucket_name: str,
            object_name: str,
            expires: timedelta = timedelta(minutes=15),
    ) -> str:
        return self.__client.presigned_get_object(bucket_name, object_name, expires,)

    def __dict_to_tags(
            self,
            dict_tags: dict,
            is_object: bool = True
    ) -> Tags:
        tags = Tags.new_object_tags() if is_object else Tags.new_bucket_tags()
        for k, v in dict_tags.items():
            tags[k] = v
        return tags

    def set_object_tags(
            self,
            bucket_name: str,
            object_name: str,
            tags: dict = None
    ) -> None:
        tags = self.__dict_to_tags(tags) if tags else None
        self.__client.set_object_tags(bucket_name, object_name, tags)

    def get_object(
            self,
            bucket_name: str,
            object_name: str,
    ) -> bytes:
        response = None
        try:
            response = self.__client.get_object(bucket_name, object_name)
            data = response.read()
        finally:
            if response:
                response.release_conn()
        return data
