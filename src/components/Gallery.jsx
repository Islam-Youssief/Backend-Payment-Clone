import {
    useCallback,
    useEffect,
    useRef,
    useState,
} from "react";

import { getImages } from "../api";

function Gallery({ accessToken }) {
    const [images, setImages] = useState([]);
    const [loading, setLoading] = useState(false);
    const [hasMore, setHasMore] = useState(true);
    const [error, setError] = useState(null);

    const cursorRef = useRef(null);
    const loadingRef = useRef(false);
    const hasMoreRef = useRef(true);
    const observerRef = useRef(null);

    const loadImages = useCallback(async () => {
        if (
            loadingRef.current ||
            !hasMoreRef.current
        ) {
            return;
        }

        loadingRef.current = true;
        setLoading(true);
        setError(null);

        try {
            const result = await getImages(
                accessToken,
                cursorRef.current,
                3
            );

            if (result.status !== 200) {
                setError(
                    result.data?.message ||
                    "Failed to load gallery"
                );
                return;
            }

            const data = result.data;

            const newImages = Array.isArray(data)
                ? data
                : Array.isArray(data.images)
                    ? data.images
                    : Array.isArray(data.Images)
                        ? data.Images
                        : [];

            setImages((current) => [
                ...current,
                ...newImages,
            ]);

            const nextCursor =
                data.next_cursor ??
                data.nextCursor ??
                data.pagination?.next_cursor ??
                null;

            const nextHasMore =
                data.has_more ??
                data.hasMore ??
                data.pagination?.has_more ??
                false;

            cursorRef.current = nextCursor;
            hasMoreRef.current = nextHasMore;

            setHasMore(nextHasMore);
        } catch (error) {
            setError(error.message);
        } finally {
            loadingRef.current = false;
            setLoading(false);
        }
    }, [accessToken]);

    useEffect(() => {
        cursorRef.current = null;
        hasMoreRef.current = true;

        setImages([]);
        setHasMore(true);

        loadImages();
    }, [accessToken, loadImages]);

    const sentinelRef = useCallback(
        (node) => {
            if (observerRef.current) {
                observerRef.current.disconnect();
            }

            if (!node) {
                return;
            }

            observerRef.current =
                new IntersectionObserver(
                    (entries) => {
                        if (
                            entries[0].isIntersecting &&
                            !loadingRef.current &&
                            hasMoreRef.current
                        ) {
                            loadImages();
                        }
                    },
                    {
                        rootMargin: "400px",
                    }
                );

            observerRef.current.observe(node);
        },
        [loadImages]
    );

    useEffect(() => {
        return () => {
            if (observerRef.current) {
                observerRef.current.disconnect();
            }
        };
    }, []);

    return (
        <div className="gallery">
            <h2>Gallery</h2>

            {error && (
                <p>
                    {error}
                </p>
            )}

            <div className="gallery-grid">
                {images.map((image) => {
                    const imageUrl =
                        image.path ||
                        image.url ||
                        image.image_url ||
                        image.imageUrl;

                    return (
                        <div
                            className="gallery-item"
                            key={image.id}
                        >
                            <img
    src={imageUrl}
    alt=""
    loading="lazy"
    style={{
        width: "300px",
        height: "200px",
        objectFit: "cover",
        display: "block",
    }}
/>
                        </div>
                    );
                })}
            </div>

            <div
                ref={sentinelRef}
                style={{
                    width: "100%",
                    height: "1px",
                }}
            />

            {loading && (
                <p>
                    Loading...
                </p>
            )}

            {!loading &&
                !error &&
                images.length === 0 && (
                    <p>
                        No images found.
                    </p>
                )}

            {!loading &&
                !hasMore &&
                images.length > 0 && (
                    <p>
                        No more images.
                    </p>
                )}
        </div>
    );
}

export default Gallery;