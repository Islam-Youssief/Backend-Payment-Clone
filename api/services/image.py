from api.models import Image


class ImageService:

    @staticmethod
    def get_images(limit=20, cursor=None):
        query = Image.query

        if cursor:
            query = query.filter(Image.id < cursor)

        images = (
            query
            .order_by(Image.id.desc())
            .limit(limit + 1)
            .all()
        )

        has_more = len(images) > limit

        images = images[:limit]

        next_cursor = images[-1].id if has_more else None

        return {
            "images": images,
            "next_cursor": next_cursor,
            "has_more": has_more,
        }