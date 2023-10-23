# # # # import os
# # # # from products.models import Category
# # #
import sys

# import requests
# from threading import Thread
# import redis
# s = redis.StrictRedis(host='127.0.0.1', db=1)
# import sys
# from main.settings import cache
# s = s.get(':1:views.decorators.cache.cache_header.users-api.820077858725d2b984ea9950019aa29f.en-us.UTC')
# print(sys.getsizeof(s))
# def request_to_site():
#     for i in range(1, 10000):
#         a = requests.get('http://127.0.0.1:8000/')
# t1 = Thread(target=request_to_site)
# t2 = Thread(target=request_to_site)
# t3 = Thread(target=request_to_site)
# t4 = Thread(target=request_to_site)
# t5 = Thread(target=request_to_site)
# t6 = Thread(target=request_to_site)
# t7 = Thread(target=request_to_site)
# t8 = Thread(target=request_to_site)
# t1.start()
# t2.start()
# t3.start()
# t4.start()
# t5.start()
# t6.start()
# t7.start()
# t8.start()
#


#
# mylist = [21,54,76,3,5,8,6,21,876,34,87,45,54,232,875,121]
#
# def sort_list(array):
#     for i in range(len(array)):
#         if array[i] > array[i+1]:

# sort_list(mylist)


# Python3 program for Bubble Sort Algorithm Implementation





# tuple_list = (['mahdi', 'ali'], ['iran', 'haha'])
# tuple_listt = (('mahdi', 'ali'), ('iran', 'haha'))
# list_tuple = (('fuck', 'iran'), ('sssds', 'dick'))
#
#
# print(dict(list_tuple))
# print(dict(tuple_list))
# my_tuple = ('haha', 'fuck', 'shit', None)
#
# print(list(zip(tuple_list, list_tuple)))
#
# print(dict(zip(list_tuple, tuple_listt)))
#
#
# aaaaa = [{'name': 'ali', 'age': 20,'name_manager': 'mahdi', 'age_manager': 27}]
#
#
#
#
# # # # name = True
# # # # last = 'azimi'
# # # # if username := name or last:
# # # #     print(username)
# # #
# #
# # s = ('sadsadasd',)
# #
# # print(''.join(s))
# # #
# # # # s = [{'name': 'mahdi', 'age': '20'}, {'name': 'ali', 'sds': 'sds'}]
# # # #
# # #
# # # s = ('category_name', 'sdsad', 'category_avatar', 'sadsa')
# # # sd = (('name', 'ali'),)
# # # # print(len(sd))
# # # print(dict(sd))
# # #
# # # my_keys = ['name', 'age']
# # #
# # # my_values = ['Bobby', 29]
# # #
# # # my_dict = list(zip(my_keys, my_values))
# # #
# # # print(my_dict)  # 👉️ {'name': 'Bobby', 'age': 29}
# # # # for array, key in s:
# # # #     print(array)
# # #
# # #
# # #
# # #
# # # #
# # # # file_list = os.listdir('/home/mahdiyar/Pictures/site_images')
# # # # sored_list = []
# # # # for file in file_list:
# # # #     path = os.path.abspath(f'/home/mahdiyar/Pictures/site_images/{file}')
# # # #     sored_list.append(path)
# # # #
# # # # lis = sorted(sored_list, key=lambda x: os.path.getctime(x))
# # # # name_list = ['موبایل', 'کالا دیجیتال', 'خانه و اشپزخانه', 'مد و پوشاک',
# # # #              'کالا های سوپر مارکتی', 'کتاب و لوازم التحریر',
# # # #              'اسباب بازی مودک و نوزاد', 'زیبایی و سلامت',
# # # #              'ورزش و سفر', 'ابزارآلات و تجهیزات', 'خودرو و موتور سیکلت', 'محصولا بومی و محلی ', 'کارت هدیه']
# # # #
# # # # for i in range(len(lis)):
# # # #     Category.objects.create(name=name_list[i], avatar=lis[i])
# # # # print(lis)
# # #
# # #
# # # # import asyncio
# # # #
# # # # async def count():
# # # #     print("One")
# # # #     await asyncio.sleep(1)
# # # #     print("Two")
# # # #
# # # # async def main():
# # # #     await asyncio.gather(count(), count(), count())
# # # #
# # # # if __name__ == "__main__":
# # # #     import time
# # # #     s = time.perf_counter()
# # # #     asyncio.run(main())
# # # #     elapsed = time.perf_counter() - s
# # # #     print(f"{__file__} executed in {elapsed:0.2f} seconds.")