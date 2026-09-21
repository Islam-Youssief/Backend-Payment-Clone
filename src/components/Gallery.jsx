import { useCallback, useEffect, useRef, useState } from "react";
import { getImages } from "../api";

function Gallery({ accessToken }) {
    const [images, setImages] = useState([]);
    const [loading, setLoading] = useState(false);
    const [hasMore, setHasMore] = useState(true);
    const [error, setError] = useState(null);

    const cursorRef = useRef(null);
    const loadingRef = useRef(false);
    const hasMoreRef = useRef(true);
    const sentinelRef = useRef(null);
    const observerRef = useRef(null);

    const loadImages = useCallback(async () => {
        if (!accessToken) {
            setError("No access token found.");
            return;
        }

        if (loadingRef.current || !hasMoreRef.current) {
            return;
        }

        loadingRef.current = true;
        setLoading(true);
        setError(null);

        const currentCursor = cursorRef.current;

        try {
            const result = await getImages(
                accessToken,
                currentCursor,
                3
            );

            if (result.status !== 200) {
                setError(
                    result.data?.message ||
                    "Failed to load gallery"
                );
                return;
            }

            const data = result.data || {};

            const newImages =
                Array.isArray(data)
                    ? data
                    : Array.isArray(data.images)
                        ? data.images
                        : Array.isArray(data.Images)
                            ? data.Images
                            : Array.isArray(data.data)
                                ? data.data
                                : Array.isArray(data.data?.images)
                                    ? data.data.images
                                    : [];

            const nextCursor =
                data.next_cursor ??
                data.nextCursor ??
                data.next ??
                data.cursor ??
                data.pagination?.next_cursor ??
                data.pagination?.nextCursor ??
                data.pagination?.next ??
                null;

            const backendHasMore =
                data.has_more ??
                data.hasMore ??
                data.pagination?.has_more ??
                data.pagination?.hasMore;

            setImages((current) => {
                const existingIds = new Set(
                    current.map((image) => image.id)
                );

                const uniqueImages = newImages.filter(
                    (image) => !existingIds.has(image.id)
                );

                return [
                    ...current,
                    ...uniqueImages,
                ];
            });

            let nextHasMore;

            if (typeof backendHasMore === "boolean") {
                nextHasMore = backendHasMore;
            } else {
                nextHasMore =
                    nextCursor !== null &&
                    newImages.length > 0;
            }

            if (
                nextCursor !== null &&
                nextCursor !== currentCursor
            ) {
                cursorRef.current = nextCursor;
            } else if (newImages.length === 0) {
                cursorRef.current = null;
                nextHasMore = false;
            } else if (newImages.length < 3) {
                cursorRef.current = null;
                nextHasMore = false;
            }

            hasMoreRef.current = nextHasMore;
            setHasMore(nextHasMore);
        } catch (err) {
            setError(
                err.message ||
                "Failed to load gallery"
            );
        } finally {
            loadingRef.current = false;
            setLoading(false);
        }
    }, [accessToken]);

    const checkSentinel = useCallback(() => {
        if (
            !sentinelRef.current ||
            loadingRef.current ||
            !hasMoreRef.current
        ) {
            return;
        }

        const rect =
            sentinelRef.current.getBoundingClientRect();

        const distanceFromViewport =
            rect.top - window.innerHeight;

        if (distanceFromViewport <= 500) {
            loadImages();
        }
    }, [loadImages]);

    useEffect(() => {
        cursorRef.current = null;
        loadingRef.current = false;
        hasMoreRef.current = true;

        setImages([]);
        setHasMore(true);
        setError(null);

        loadImages();
    }, [accessToken, loadImages]);

    useEffect(() => {
        if (!sentinelRef.current) {
            return;
        }

        observerRef.current =
            new IntersectionObserver(
                (entries) => {
                    if (
                        entries.some(
                            (entry) => entry.isIntersecting
                        )
                    ) {
                        loadImages();
                    }
                },
                {
                    root: null,
                    rootMargin: "800px 0px",
                    threshold: 0,
                }
            );

        observerRef.current.observe(
            sentinelRef.current
        );

        return () => {
            if (observerRef.current) {
                observerRef.current.disconnect();
                observerRef.current = null;
            }
        };
    }, [loadImages]);

    useEffect(() => {
        const handleScroll = () => {
            checkSentinel();
        };

        const handleResize = () => {
            checkSentinel();
        };

        window.addEventListener(
            "scroll",
            handleScroll,
            { passive: true }
        );

        window.addEventListener(
            "resize",
            handleResize
        );

        const interval = setInterval(
            checkSentinel,
            500
        );

        checkSentinel();

        return () => {
            window.removeEventListener(
                "scroll",
                handleScroll
            );

            window.removeEventListener(
                "resize",
                handleResize
            );

            clearInterval(interval);
        };
    }, [checkSentinel]);

    useEffect(() => {
        if (
            !loading &&
            hasMore &&
            images.length > 0
        ) {
            const timer = setTimeout(
                checkSentinel,
                100
            );

            return () => clearTimeout(timer);
        }
    }, [
        images,
        loading,
        hasMore,
        checkSentinel,
    ]);

    return (
        <div className="gallery">
            <h2>Gallery</h2>

            {error && (
                <p>{error}</p>
            )}

            <div className="gallery-grid">
                {images.map((image, index) => {
                    const imageUrl =
                        image.path ||
                        image.url ||
                        image.image_url ||
                        image.imageUrl;

                    if (!imageUrl) {
                        return null;
                    }

                    return (
                        <div
                            className="gallery-item"
                            key={
                                image.id ??
                                `${imageUrl}-${index}`
                            }
                        >
                            <img
                                src={imageUrl}
                                alt=""
                                loading="lazy"
                                width="300"
                                height="200"
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
                    height: "20px",
                }}
            />

            {loading && (
                <p>Loading...</p>
            )}

            {!loading &&
                !error &&
                images.length === 0 && (
                    <p>No images found.</p>
                )}

            {!loading &&
                !hasMore &&
                images.length > 0 && (
                    <p>No more images.</p>
                )}
        </div>
    );
}

export default Gallery;