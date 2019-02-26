import ImageMatching
import time


if __name__ == '__main__':
    src = r'C:\Users\silopi\Desktop\a'
    dest = r'C:\Users\silopi\Desktop\b'
    dest2 = r'C:\Users\silopi\Desktop\c'
    file = r'C:\Users\silopi\Desktop\test1\1.jpg'
    file2 = r'C:\Users\silopi\Desktop\test2\2.jpg'
    # print(ImageMatching.get_all_photos(src))
    '''
    a = time.time()'''
    # ImageMatching.upload_all_photos(src, dest)
    # a = time.time() - a
    # b = time.time()
    ImageMatching.compare_photos_in_path(src, dest2)
    # b = time.time() - b

    # print('İlk algoritma: {}\nİkinci algoritma: {}\nFark: {}'.format(a, b, b-a))
