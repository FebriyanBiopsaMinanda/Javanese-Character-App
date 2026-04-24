import os
import cv2
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# =========================================================
# KONFIGURASI
# =========================================================
dataset_folder = "Dataset Gabungan"
font_folder = "Javanese Font"
output_folder = "Dataset Augmentasi"

img_size = 128
target_per_class = 500

valid_img_ext = (".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff")
valid_font_ext = (".ttf", ".otf")

# mapping nama folder -> karakter aksara Jawa
char_map = {
    "ha": "ꦲ",
    "na": "ꦤ",
    "ca": "ꦕ",
    "ra": "ꦫ",
    "ka": "ꦏ",
    "da": "ꦢ",
    "ta": "ꦠ",
    "sa": "ꦱ",
    "wa": "ꦮ",
    "la": "ꦭ",
    "pa": "ꦥ",
    "dha": "ꦝ",
    "ja": "ꦗ",
    "ya": "ꦪ",
    "nya": "ꦚ",
    "ma": "ꦩ",
    "ga": "ꦒ",
    "ba": "ꦧ",
    "tha": "ꦛ",
    "nga": "ꦔ"
}


# =========================================================
# UTILITAS
# =========================================================
def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def list_image_files(folder):
    if not os.path.exists(folder):
        return []
    return sorted([
        f for f in os.listdir(folder)
        if os.path.isfile(os.path.join(folder, f)) and f.lower().endswith(valid_img_ext)
    ])


def list_font_files(folder):
    if not os.path.exists(folder):
        return []
    return sorted([
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if os.path.isfile(os.path.join(folder, f)) and f.lower().endswith(valid_font_ext)
    ])


def center_cv_image(image, size=128, bg_color=255, margin=8):
    if image is None:
        return np.ones((size, size, 3), dtype=np.uint8) * bg_color

    if len(image.shape) == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
    coords = cv2.findNonZero(thresh)

    if coords is None:
        return np.ones((size, size, 3), dtype=np.uint8) * bg_color

    x, y, w, h = cv2.boundingRect(coords)
    cropped = image[y:y+h, x:x+w]

    max_w = size - 2 * margin
    max_h = size - 2 * margin

    scale = min(max_w / w, max_h / h)
    new_w = max(1, int(w * scale))
    new_h = max(1, int(h * scale))

    resized = cv2.resize(cropped, (new_w, new_h), interpolation=cv2.INTER_AREA)

    canvas = np.ones((size, size, 3), dtype=np.uint8) * bg_color
    x_offset = (size - new_w) // 2
    y_offset = (size - new_h) // 2
    canvas[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = resized

    return canvas


def pil_to_cv(img_pil):
    return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)


def cv_to_pil(img_cv):
    return Image.fromarray(cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB))


# =========================================================
# BUAT GAMBAR DARI FONT
# =========================================================
def render_char_from_font(char, font_path, size=128):
    canvas_size = size * 2
    img = Image.new("RGB", (canvas_size, canvas_size), "white")
    draw = ImageDraw.Draw(img)

    font_size = random.randint(int(size * 0.7), int(size * 1.2))

    try:
        font = ImageFont.truetype(font_path, font_size)
    except:
        return None

    try:
        bbox = draw.textbbox((0, 0), char, font=font)
    except:
        return None

    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    if text_w <= 0 or text_h <= 0:
        return None

    x = (canvas_size - text_w) // 2 - bbox[0]
    y = (canvas_size - text_h) // 2 - bbox[1]

    draw.text((x, y), char, font=font, fill="black")

    angle = random.uniform(-8, 8)
    img = img.rotate(angle, expand=True, fillcolor="white")

    img_cv = pil_to_cv(img)
    img_cv = center_cv_image(img_cv, size=size, margin=8)

    return img_cv


# =========================================================
# AUGMENTASI
# =========================================================
def add_gaussian_noise(img, sigma_range=(3, 12)):
    sigma = random.uniform(*sigma_range)
    noise = np.random.normal(0, sigma, img.shape).astype(np.float32)
    noisy = img.astype(np.float32) + noise
    noisy = np.clip(noisy, 0, 255).astype(np.uint8)
    return noisy


def apply_blur(img):
    choice = random.choice(["gaussian", "median", "none"])
    if choice == "gaussian":
        k = random.choice([3, 5])
        return cv2.GaussianBlur(img, (k, k), 0)
    elif choice == "median":
        k = random.choice([3, 5])
        return cv2.medianBlur(img, k)
    return img


def apply_morphology(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    op = random.choice(["erode", "dilate", "none"])
    k = random.choice([1, 2, 3])
    kernel = np.ones((k, k), np.uint8)

    if op == "erode":
        gray = cv2.erode(gray, kernel, iterations=1)
    elif op == "dilate":
        gray = cv2.dilate(gray, kernel, iterations=1)

    result = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    return result


def random_shift(img, max_shift=6):
    h, w = img.shape[:2]
    tx = random.randint(-max_shift, max_shift)
    ty = random.randint(-max_shift, max_shift)
    M = np.float32([[1, 0, tx], [0, 1, ty]])
    shifted = cv2.warpAffine(
        img, M, (w, h),
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=(255, 255, 255)
    )
    shifted = center_cv_image(shifted, size=w, margin=8)
    return shifted


def augment_image(img):
    aug = img.copy()

    if random.random() < 0.8:
        aug = apply_morphology(aug)

    if random.random() < 0.8:
        aug = apply_blur(aug)

    if random.random() < 0.5:
        aug = add_gaussian_noise(aug)

    if random.random() < 0.6:
        aug = random_shift(aug, max_shift=5)

    aug = center_cv_image(aug, size=img.shape[0], margin=8)
    return aug


# =========================================================
# SIMPAN DATA AWAL + TAMBAHAN
# =========================================================
def save_image(path, img):
    cv2.imwrite(path, img)


def copy_existing_images(label, dst_folder, start_idx=1):
    src_folder = os.path.join(dataset_folder, label)
    files = list_image_files(src_folder)

    idx = start_idx
    saved = 0

    for file in files:
        src_path = os.path.join(src_folder, file)
        img = cv2.imread(src_path)

        if img is None:
            continue

        img = center_cv_image(img, size=img_size, margin=8)
        save_path = os.path.join(dst_folder, f"{idx}.png")
        save_image(save_path, img)
        idx += 1
        saved += 1

    return idx, saved


def generate_base_pool_from_fonts(label, char, fonts, desired_count=200):
    pool = []

    if not fonts:
        return pool

    tries = 0
    max_tries = desired_count * 10

    while len(pool) < desired_count and tries < max_tries:
        font_path = random.choice(fonts)
        img = render_char_from_font(char, font_path, size=img_size)
        tries += 1

        if img is not None:
            pool.append(img)

    return pool


def build_dataset_for_label(label, char):
    print(f"Proses label: {label}")

    dst_folder = os.path.join(output_folder, label)
    ensure_dir(dst_folder)

    idx = 1

    # 1) simpan data asli dari Dataset Gabungan
    idx, existing_count = copy_existing_images(label, dst_folder, start_idx=idx)
    print(f"  - data asli tersalin: {existing_count}")

    # 2) ambil semua font
    fonts = list_font_files(font_folder)
    print(f"  - jumlah font ditemukan: {len(fonts)}")

    # 3) buat pool image dasar dari font
    base_pool = generate_base_pool_from_fonts(label, char, fonts, desired_count=min(300, target_per_class))
    print(f"  - base image dari font berhasil dibuat: {len(base_pool)}")

    # 4) jika belum cukup, tambahkan gambar font asli dulu
    pool_index = 0
    while idx <= target_per_class and pool_index < len(base_pool):
        img = base_pool[pool_index]
        save_path = os.path.join(dst_folder, f"{idx}.png")
        save_image(save_path, img)
        idx += 1
        pool_index += 1

    # 5) augmentasi sampai mencapai target_per_class
    if len(base_pool) == 0 and existing_count == 0:
        print(f"  - label {label} dilewati karena tidak ada data dan font tidak berhasil dirender")
        return

    current_images = []

    # ambil semua gambar yang sudah ada sebagai sumber augmentasi
    for file in list_image_files(dst_folder):
        img = cv2.imread(os.path.join(dst_folder, file))
        if img is not None:
            current_images.append(img)

    if not current_images:
        print(f"  - label {label} gagal karena tidak ada sumber augmentasi")
        return

    while idx <= target_per_class:
        source_img = random.choice(current_images)
        aug_img = augment_image(source_img)

        save_path = os.path.join(dst_folder, f"{idx}.png")
        save_image(save_path, aug_img)

        current_images.append(aug_img)
        idx += 1

    print(f"  - total akhir: {target_per_class}")


# =========================================================
# MAIN
# =========================================================
def main():
    ensure_dir(output_folder)

    for label, char in char_map.items():
        build_dataset_for_label(label, char)

    print("\nSelesai. Dataset augmentasi berhasil dibuat.")


if __name__ == "__main__":
    main()