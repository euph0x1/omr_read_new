import cv2
import numpy as np

def preprocess_image(image_path):
    """
    Preprocess OMR sheet image (Adobe Scan–style):
    - Deskew & perspective correction
    - Shadow removal with CLAHE
    - Adaptive thresholding (robust to lighting)
    - Morphological ops for bubble clarity
    - Background flattening, bilateral filter, sharpening
    Returns: aligned original image, processed thresholded image
    """

    # 1. Load
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found: {image_path}")
    orig = image.copy()

    # 2. Grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 3. CLAHE (local contrast enhancement → handles shadows)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    gray = clahe.apply(gray)

    # 4. Noise removal (bilateral filter preserves edges better than Gaussian alone)
    gray = cv2.bilateralFilter(gray, d=9, sigmaColor=75, sigmaSpace=75)

    # 5. Background flattening using large Gaussian blur
    background = cv2.GaussianBlur(gray, (55, 55), 0)
    gray = cv2.subtract(gray, background)
    gray = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)

    # 6. Edge detection
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)

    # 7. Find largest contour (sheet boundary)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    if len(contours) > 0:
        sheet_contour = contours[0]
        peri = cv2.arcLength(sheet_contour, True)
        approx = cv2.approxPolyDP(sheet_contour, 0.02 * peri, True)

        if len(approx) == 4:
            pts = approx.reshape(4, 2)

            # Order points
            rect = np.zeros((4, 2), dtype="float32")
            s = pts.sum(axis=1)
            rect[0] = pts[np.argmin(s)]  # top-left
            rect[2] = pts[np.argmax(s)]  # bottom-right
            diff = np.diff(pts, axis=1)
            rect[1] = pts[np.argmin(diff)]  # top-right
            rect[3] = pts[np.argmax(diff)]  # bottom-left

            (tl, tr, br, bl) = rect
            widthA = np.linalg.norm(br - bl)
            widthB = np.linalg.norm(tr - tl)
            maxWidth = max(int(widthA), int(widthB))

            heightA = np.linalg.norm(tr - br)
            heightB = np.linalg.norm(tl - bl)
            maxHeight = max(int(heightA), int(heightB))

            dst = np.array([
                [0, 0],
                [maxWidth - 1, 0],
                [maxWidth - 1, maxHeight - 1],
                [0, maxHeight - 1]], dtype="float32")

            M = cv2.getPerspectiveTransform(rect, dst)
            image = cv2.warpPerspective(orig, M, (maxWidth, maxHeight))
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Apply CLAHE + Bilateral + Background flatten again after perspective warp
            gray = clahe.apply(gray)
            gray = cv2.bilateralFilter(gray, d=9, sigmaColor=75, sigmaSpace=75)
            background = cv2.GaussianBlur(gray, (55, 55), 0)
            gray = cv2.subtract(gray, background)
            gray = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)

    # 8. Adaptive threshold (handles shadows)
    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY_INV,
        25, 15
    )

    # 9. Morphological operations (remove noise + fill bubbles)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)

    # 10. Deskew (if tilted)
    coords = np.column_stack(np.where(thresh > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    (h, w) = thresh.shape
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    thresh = cv2.warpAffine(thresh, M, (w, h),
                            flags=cv2.INTER_CUBIC,
                            borderMode=cv2.BORDER_REPLICATE)

    # 11. Optional: sharpen the thresholded image for clearer bubbles
    kernel_sharp = np.array([[0, -1, 0],
                             [-1, 5, -1],
                             [0, -1, 0]])
    thresh = cv2.filter2D(thresh, -1, kernel_sharp)

    return image, thresh
