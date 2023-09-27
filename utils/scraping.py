import os
from products.models import Category

file_list = os.listdir('/home/mahdiyar/Pictures/site_images')
sored_list = []
for file in file_list:
    path = os.path.abspath(f'/home/mahdiyar/Pictures/site_images/{file}')
    sored_list.append(path)

lis = sorted(sored_list, key=lambda x: os.path.getctime(x))
name_list = ['موبایل', 'کالا دیجیتال', 'خانه و اشپزخانه', 'مد و پوشاک',
             'کالا های سوپر مارکتی', 'کتاب و لوازم التحریر',
             'اسباب بازی مودک و نوزاد', 'زیبایی و سلامت',
             'ورزش و سفر', 'ابزارآلات و تجهیزات', 'خودرو و موتور سیکلت', 'محصولا بومی و محلی ', 'کارت هدیه']

for i in range(len(lis)):
    Category.objects.create(name=name_list[i], avatar=lis[i])
print(lis)
