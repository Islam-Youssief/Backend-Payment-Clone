from api.services.image import ImageService


class ImageController:

    @staticmethod
    def get_images(limit=2, cursor=None):
        result = ImageService.get_images(
            limit=limit,
            cursor=cursor,
        )

        return {
            "images": [
                {
                    "id": image.id,
                    "path": image.path,
                }
                for image in result["images"]
            ],
            "next_cursor": result["next_cursor"],
            "has_more": result["has_more"],
        }