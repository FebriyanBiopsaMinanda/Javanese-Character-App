import os
import cv2
import numpy as np

# =========================
# KONFIGURASI PATH
# =========================
dataset1 = "Dataset 1"
dataset2 = "Dataset 2"
output = "Dataset Gabungan"

# ukuran output gambar
img_size = 128

# ekstensi file gambar yang didukung
valid_ext = (".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff")


# =========================
# FUNGSI CENTER IMAGE
# =========================
def center_image(image, size=128):
    # jika gambar grayscale, ubah ke BGR dulu
    if len(image.shape) == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    # ubah ke grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # threshold untuk mengambil objek tulisan hitam di background putih
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

    # cari koordinat objek
    coords = cv2.findNonZero(thresh)

    # jika tidak ada objek terdeteksi, return canvas putih
    if coords is None:
        return np.ones((size, size, 3), dtype=np.uint8) * 255

    x, y, w, h = cv2.boundingRect(coords)

    # crop objek
    cropped = image[y:y+h, x:x+w]

    # resize proporsional jika objek lebih besar dari canvas
    if h > size or w > size:
        scale = min((size - 10) / w, (size - 10) / h)
        new_w = max(1, int(w * scale))
        new_h = max(1, int(h * scale))
        cropped = cv2.resize(cropped, (new_w, new_h), interpolation=cv2.INTER_AREA)
        h, w = new_h, new_w

    # buat canvas putih
    canvas = np.ones((size, size, 3), dtype=np.uint8) * 255

    # hitung posisi tengah
    x_offset = (size - w) // 2
    y_offset = (size - h) // 2

    # tempel objek ke tengah
    canvas[y_offset:y_offset+h, x_offset:x_offset+w] = cropped

    return canvas


# =========================
# FUNGSI GABUNGKAN DATASET
# =========================
def merge_and_center_datasets(source_folders, destination, size=128):
    os.makedirs(destination, exist_ok=True)

    # ambil semua label dari semua dataset
    all_labels = set()
    for source in source_folders:
        if not os.path.exists(source):
            print(f"Folder tidak ditemukan: {source}")
            continue

        for label in os.listdir(source):
            label_path = os.path.join(source, label)
            if os.path.isdir(label_path):
                all_labels.add(label)

    # proses tiap label
    for label in sorted(all_labels):
        dst_label_folder = os.path.join(destination, label)
        os.makedirs(dst_label_folder, exist_ok=True)

        counter = 1

        for source in source_folders:
            src_label_folder = os.path.join(source, label)

            if not os.path.exists(src_label_folder):
                continue

            # ambil file gambar saja
            files = [
                f for f in os.listdir(src_label_folder)
                if os.path.isfile(os.path.join(src_label_folder, f)) and f.lower().endswith(valid_ext)
            ]

            # urutkan agar konsisten
            files.sort()

            for file in files:
                src_file = os.path.join(src_label_folder, file)

                image = cv2.imread(src_file)
                if image is None:
                    print(f"Gagal membaca file: {src_file}")
                    continue

                centered = center_image(image, size=size)

                new_name = f"{counter}.png"
                dst_file = os.path.join(dst_label_folder, new_name)

                cv2.imwrite(dst_file, centered)
                counter += 1

        print(f"Label '{label}' selesai, total file: {counter - 1}")


# =========================
# JALANKAN PROGRAM
# =========================
merge_and_center_datasets(
    source_folders=[dataset1, dataset2],
    destination=output,
    size=img_size
)

print("Semua dataset berhasil digabung, diurutkan, dan objek dipusatkan.")