import os
import cv2
import random
import numpy as np

# ==========================================
# KONFIGURASI
# ==========================================
source_folder = "Dataset Augmentasi"
output_folder = "Dataset"
target_per_class = 500
img_size = 128

valid_ext = (".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff")


# ==========================================
# UTIL
# ==========================================
def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def list_images(folder):
    return sorted([
        f for f in os.listdir(folder)
        if os.path.isfile(os.path.join(folder, f)) and f.lower().endswith(valid_ext)
    ])


def center_image(image, size=128, margin=8):
    if image is None:
        return np.ones((size, size, 3), dtype=np.uint8) * 255

    if len(image.shape) == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
    coords = cv2.findNonZero(thresh)

    if coords is None:
        return np.ones((size, size, 3), dtype=np.uint8) * 255

    x, y, w, h = cv2.boundingRect(coords)
    cropped = image[y:y+h, x:x+w]

    scale = min((size - 2 * margin) / w, (size - 2 * margin) / h)
    new_w = max(1, int(w * scale))
    new_h = max(1, int(h * scale))

    resized = cv2.resize(cropped, (new_w, new_h), interpolation=cv2.INTER_AREA)

    canvas = np.ones((size, size, 3), dtype=np.uint8) * 255
    x_offset = (size - new_w) // 2
    y_offset = (size - new_h) // 2

    canvas[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = resized
    return canvas


# ==========================================
# AUGMENTASI
# ==========================================
def augment(img):
    result = img.copy()

    # erosi / dilasi
    if random.random() < 0.8:
        kernel = np.ones((random.choice([1, 2, 3]), random.choice([1, 2, 3])), np.uint8)
        if random.random() < 0.5:
            result = cv2.erode(result, kernel, iterations=1)
        else:
            result = cv2.dilate(result, kernel, iterations=1)

    # blur
    if random.random() < 0.7:
        k = random.choice([3, 5])
        result = cv2.GaussianBlur(result, (k, k), 0)

    # rotasi
    if random.random() < 0.6:
        h, w = result.shape[:2]
        angle = random.uniform(-10, 10)
        M = cv2.getRotationMatrix2D((w // 2, h // 2), angle, 1.0)
        result = cv2.warpAffine(
            result, M, (w, h),
            borderMode=cv2.BORDER_CONSTANT,
            borderValue=(255, 255, 255)
        )

    # shift
    if random.random() < 0.6:
        h, w = result.shape[:2]
        tx = random.randint(-5, 5)
        ty = random.randint(-5, 5)
        M = np.float32([[1, 0, tx], [0, 1, ty]])
        result = cv2.warpAffine(
            result, M, (w, h),
            borderMode=cv2.BORDER_CONSTANT,
            borderValue=(255, 255, 255)
        )

    # noise
    if random.random() < 0.4:
        noise = np.random.normal(0, 10, result.shape)
        result = np.clip(result.astype(np.float32) + noise, 0, 255).astype(np.uint8)

    result = center_image(result, size=img_size)
    return result


# ==========================================
# PROSES PER FOLDER
# ==========================================
def process_folder(class_name):
    src_path = os.path.join(source_folder, class_name)
    dst_path = os.path.join(output_folder, class_name)

    ensure_dir(dst_path)

    files = list_images(src_path)

    if len(files) == 0:
        print(f"[SKIP] kosong: {src_path}")
        return

    pool = []
    counter = 1

    # salin dulu semua gambar dari Dataset Augmentasi ke Dataset
    for f in files:
        img = cv2.imread(os.path.join(src_path, f))
        if img is None:
            continue

        img = center_image(img, size=img_size)

        save_path = os.path.join(dst_path, f"{counter}.png")
        cv2.imwrite(save_path, img)

        pool.append(img)
        counter += 1

    original_count = len(pool)
    print(f"{class_name}: data awal {original_count}")

    # augment sampai 500
    while len(pool) < target_per_class:
        base = random.choice(pool)
        aug_img = augment(base)

        save_path = os.path.join(dst_path, f"{counter}.png")
        cv2.imwrite(save_path, aug_img)

        pool.append(aug_img)
        counter += 1

    print(f"selesai jadi {len(pool)} gambar")


# ==========================================
# MAIN
# ==========================================
def main():
    ensure_dir(output_folder)

    folders = [
        f for f in os.listdir(source_folder)
        if os.path.isdir(os.path.join(source_folder, f))
    ]
    folders.sort()

    for folder_name in folders:
        process_folder(folder_name)

    print("\nSelesai! Hasil disimpan di folder 'Dataset'.")


if __name__ == "__main__":
    main()