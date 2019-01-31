from image_match.goldberg import ImageSignature
from PIL import Image
from shutil import copy
import os


# Parametre olarak verilen iki fotoğrafın benzerliklerini karşılaştırır ve farklılık oranı %40 tan aşağı ise True
# döndürür.
def compare_photos(photo_1, photo_2):
    gis = ImageSignature()
    a = gis.generate_signature(photo_1)
    b = gis.generate_signature(photo_2)
    normalized_distance = gis.normalized_distance(a, b)

    if normalized_distance < 0.4:
        return True
    return False


# Parametre olarak verilen fotoğrafın çözünürlüğünü döndürür.
def get_resolution(photo):
    im = Image.open(photo)
    return im.size


# Parametre olarak verilen iki fotoğrafın çözünürlüğünü karşılaştırır ve çözünürlüğü düşük olan fotoğrafı döndürür.
def compare_photos_resolutions(photo_1, photo_2):
    photo_1_res = get_resolution(photo_1)
    photo_2_res = get_resolution(photo_2)
    resolution_1 = photo_1_res[0] * photo_1_res[1]
    resolution_2 = photo_2_res[0] * photo_2_res[1]

    if resolution_1 <= resolution_2:
        return photo_1
    return photo_2


# Düşük çözünürlüklü fotoğrafı silme fonksiyonu
def delete_low_res_photo(photo):
    os.remove(photo)


# Fotoğrafları karşılaştırır ve aynı olanları siler
def find_same_photos(photo_1, photo_2):
    if compare_photos(photo_1, photo_2):
        low_resolution = compare_photos_resolutions(photo_1, photo_2)
        delete_low_res_photo(low_resolution)
    else:
        print("{0} ile {1} isimli fotoğraların farklı olması nedeniyle işlem yapılmamıştır.".format(photo_1, photo_2))


# Klasörde bulunan tüm fotoğrafları döndürür.
def get_all_photos(path):
    images = []
    path = path
    valid_images = [".jpg", ".gif", ".png", ".jpeg"]
    for f in os.listdir(path):
        ext = os.path.splitext(f)[1]
        if ext.lower() not in valid_images:
            continue
        images.append(f)
    return images


# Verilen yolda bulunan tüm fotoğrafların karşılaştıralarak tüm aynı fotoğrafların tespit edilmesi
def compare_all_photos_in_path(path):
    photos = get_all_photos(path)
    delete_item = []

    for i, photo in enumerate(photos):
        other_photos = photos[i + 1:]

        if len(other_photos) > 0:
            for ph in other_photos:
                if compare_photos(photo, ph):
                    delete_item.append(compare_photos_resolutions(photo, ph))
    return set(delete_item)


# Verilen tüm fotoğrafların silinmesi
def delete_same_photos(photos):
    for photo in photos:
        delete_low_res_photo(photo)


# Verilen fotoğrafı klasörde bulunan tüm fotoğraflar ile karşılaştırır. Aynı fotoğrafın bulunması durumunda iki
# fotoğrafı karşılaştırarak çözünürlüğü yüksek olanı tutar. Diğer fotoğrafı ise siler.
def compare_a_photo_in_path(photo, path):
    if len(get_all_photos(path)) > 0:
        for ph in get_all_photos(path):
            if compare_photos(photo, ph):
                if compare_photos_resolutions(photo, ph) == ph:
                    delete_low_res_photo(ph)
                    copy(photo, os.getcwd())
                    print('Fotoğraf başarı ile eklenmiştir.')
                else:
                    print('Eklemeye çalıştığınısz fotoğrafın aynısı veya daha yüksek çözünürlüklü hali bulunması '
                          'nedeniyle fotoğraf eklenmemiştir.')
                break
    else:
        print('Belirtilen yolda herhangi bir fotoğraf bulunamamıştır!')