import ImageMatching


if __name__ == '__main__':
    src = r'C:\Users\silopi\Desktop\test1'
    dest = r'C:\Users\silopi\Desktop\test2'
    file = r'C:\Users\silopi\Desktop\test1\1.jpg'
    file2 = r'C:\Users\silopi\Desktop\test2\2.jpg'
    # print(ImageMatching.get_all_photos(src))
    ImageMatching.upload_all_photos(src, dest)
