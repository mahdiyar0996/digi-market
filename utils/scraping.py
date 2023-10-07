# # # import os
# # # from products.models import Category
# #

tuple_list = (['mahdi', 'ali'], ['iran', 'haha'])
tuple_listt = (('mahdi', 'ali'), ('iran', 'haha'))
list_tuple = (('fuck', 'iran'), ('sssds', 'dick'))


print(dict(list_tuple))
print(dict(tuple_list))
my_tuple = ('haha', 'fuck', 'shit', None)

print(list(zip(tuple_list, list_tuple)))

print(dict(zip(list_tuple, tuple_listt)))


aaaaa = [{'name': 'ali', 'age': 20,'name_manager': 'mahdi', 'age_manager': 27}]




# # # name = True
# # # last = 'azimi'
# # # if username := name or last:
# # #     print(username)
# #
#
# s = ('sadsadasd',)
#
# print(''.join(s))
# #
# # # s = [{'name': 'mahdi', 'age': '20'}, {'name': 'ali', 'sds': 'sds'}]
# # #
# #
# # s = ('category_name', 'sdsad', 'category_avatar', 'sadsa')
# # sd = (('name', 'ali'),)
# # # print(len(sd))
# # print(dict(sd))
# #
# # my_keys = ['name', 'age']
# #
# # my_values = ['Bobby', 29]
# #
# # my_dict = list(zip(my_keys, my_values))
# #
# # print(my_dict)  # 👉️ {'name': 'Bobby', 'age': 29}
# # # for array, key in s:
# # #     print(array)
# #
# #
# #
# #
# # #
# # # file_list = os.listdir('/home/mahdiyar/Pictures/site_images')
# # # sored_list = []
# # # for file in file_list:
# # #     path = os.path.abspath(f'/home/mahdiyar/Pictures/site_images/{file}')
# # #     sored_list.append(path)
# # #
# # # lis = sorted(sored_list, key=lambda x: os.path.getctime(x))
# # # name_list = ['موبایل', 'کالا دیجیتال', 'خانه و اشپزخانه', 'مد و پوشاک',
# # #              'کالا های سوپر مارکتی', 'کتاب و لوازم التحریر',
# # #              'اسباب بازی مودک و نوزاد', 'زیبایی و سلامت',
# # #              'ورزش و سفر', 'ابزارآلات و تجهیزات', 'خودرو و موتور سیکلت', 'محصولا بومی و محلی ', 'کارت هدیه']
# # #
# # # for i in range(len(lis)):
# # #     Category.objects.create(name=name_list[i], avatar=lis[i])
# # # print(lis)
# #
# #
# # # import asyncio
# # #
# # # async def count():
# # #     print("One")
# # #     await asyncio.sleep(1)
# # #     print("Two")
# # #
# # # async def main():
# # #     await asyncio.gather(count(), count(), count())
# # #
# # # if __name__ == "__main__":
# # #     import time
# # #     s = time.perf_counter()
# # #     asyncio.run(main())
# # #     elapsed = time.perf_counter() - s
# # #     print(f"{__file__} executed in {elapsed:0.2f} seconds.")