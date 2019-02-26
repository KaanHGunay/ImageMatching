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
        images.append(path + '\\' + f)
    # print(len(images), 'adet fotoğraf tespit edildi.')
    return images


# Verilen yolda bulunan tüm fotoğrafların karşılaştıralarak tüm aynı fotoğrafların tespit edilmesi
def compare_all_photos_in_path(path):
    photos = get_all_photos(path)
    delete_item = set()
    lenphoto = len(photos)
    print('Karşılaştırma işlemi başlatılıyor...')

    for i, photo in enumerate(photos):
        # print('Kontrol durumu', i+1, '/', lenphoto, end='\n')
        other_photos = photos[i + 1:]
        lenothers = len(other_photos)
        index = 1

        if len(other_photos) > 0:
            for ph in other_photos:
                if compare_photos(photo, ph):
                    img = compare_photos_resolutions(photo, ph)
                    print(img, 'fotoğrafının aynısı bulunmaktadır.')
                    delete_item.add(img)
                yuzde = (100 * index / lenothers)
                print('{0} / {1}. fotoğrafın karşılaştırma durumu: \t%{2:.2f}'.format((i + 1), lenphoto, yuzde), end='\r')
                index += 1
        # print('\n')
    print('Silinecek', len(delete_item), 'adet fotoğraf tespit edildi.')
    return delete_item


# Verilen tüm fotoğrafların silinmesi
def delete_same_photos(photos):
    for photo in photos:
        delete_low_res_photo(photo)


# Verilen fotoğrafı klasörde bulunan tüm fotoğraflar ile karşılaştırır. Aynı fotoğrafın bulunması durumunda iki
# fotoğrafı karşılaştırarak çözünürlüğü yüksek olanı tutar. Diğer fotoğrafı ise siler.
def compare_a_photo_in_path(photo, path):
    photos = get_all_photos(path)
    is_same_photo_exist = False

    if len(photos) > 0:
        for ph in photos:
            if compare_photos(photo, ph):
                is_same_photo_exist = True
                if compare_photos_resolutions(photo, ph) == ph:
                    replace_high_res_photo(photo, ph, path)
                    print('Aynı fotoğrafın daha yüksek çözünürlüğü hali eklenmiştir.')
                else:
                    print('Aynı fotoğraf : {0}'.format(photo))
        return is_same_photo_exist
    return is_same_photo_exist


# Yüksek çözünürlüklü fotoğraf ile düşük çözünürlüklü fotoğrafı değiştirme
def replace_high_res_photo(photo, ph, path):
    delete_low_res_photo(ph)
    copy(photo, path)


# Yeni fotoğraf ekleme
def upload_new_photo(photo, path):
    if not compare_a_photo_in_path(photo, path):
        copy(photo, path)


# Klasörde bulunan tüm fotoğrafların incelenerek farklı olan fotoğrafların belirtilen yola eklenmesi
def upload_all_photos(src, dest):
    photos = find_diff_photos(src)
    index = 1
    lenphotos = len(photos)

    for photo in photos:
        upload_new_photo(photo, dest)
        print('{0}/{1} fotoğraf eklendi'.format(index, lenphotos), end='\r')
        index += 1


# Klasörde bulunan farklı fotoğrafların tespit edilmesi
def find_diff_photos(path):
    diff_photos = []
    all_photos = get_all_photos(path)
    same_photos = compare_all_photos_in_path(path)

    for photo in all_photos:
        if photo not in same_photos:
            diff_photos.append(photo)
    print(len(diff_photos), 'farklı tespit edildi')
    return diff_photos
