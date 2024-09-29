"""
Исполняющий модуль программы.

Func:

    monitoring_price: Функция мониторинга,
        раз в час проверяет актуальную цену на товар,
        добавляет её в базу данных.
    main: Создаёт таски, для асинхронного выполнения кода.
"""
import asyncio

from database.FDataBase import (get_session,
                                select_all_item,
                                add_item_price)
from backend.backend import get_html, get_price_item


async def monitoring_price():
    """
    Функция мониторинга цены на товары.


    """
    async for session in get_session(): 
        while True:
                products = await select_all_item(session=session)
                products_list = products['message']
                if products_list == []:
                     print("Отсутствуют товары для мониторинга!")
                else:
                    for product in products_list:
                            url_price = str(product['url_price'])
                            id_item = product['id']
                            data_html = await get_html(url=url_price)
                            data_price = await get_price_item(data_price=data_html)
                            result = await add_item_price(product_id=int(id_item),
                                                        price=float(data_price['price']),
                                                        session=session)
                            print(result["message"])
                await asyncio.sleep(3600)


async def main():
    monitoring_task = asyncio.create_task(monitoring_price())
    await monitoring_task


if __name__ == "__main__":
    asyncio.run(main())