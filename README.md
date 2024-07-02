# Установка Breed
https://telegra.ph/KeeneticOS-407-na-Netis-N6-02-28

[Скачать архив](https://github.com/spatiumstas/Netis-N6-Breed/archive/refs/heads/main.zip)
1. Ставим LEDE из папки Firmware поверх стока простым обновлением 
2. После перезагрузки обновляем поверх до OpenWRT из той же папки. Первый запуск займёт до 5 минут
![image](https://github.com/spatiumstas/Netis-N6-Breed/assets/79056064/0f407c46-addb-4d1b-9c17-7b8a0b24bda7)

3. После запуска OpenWRT запускаем !Start.bat
Скрипт сделает бекап стокового загрузчика, factory раздела (он же mtd2, он же eeprom) в папку Data. Установит и выполнит перезагрузку в Breed
![image](https://github.com/spatiumstas/Netis-N6-Breed/assets/79056064/a4602e80-363d-4970-ab0c-5970e66f9076)

4. В Breed обязательно делаем full backup на случай отката
![image](https://github.com/spatiumstas/Netis-N6-Breed/assets/79056064/a67b8db4-fc3e-407e-b246-3034fb72f01e)


# Откат на OpenWRT
1. Открываем свой бекап в HxD
2. Выделяем первый кусок в котором содержится Breed и стираем

![Screenshot_2](https://github.com/spatiumstas/Netis-N6-Breed/assets/79056064/0f938411-9a03-42cf-b70f-cd79f0f06ef6)
![Screenshot_1](https://github.com/spatiumstas/Netis-N6-Breed/assets/79056064/0b55d9c4-17e3-4b08-9c7d-cfc9e31e4926)

4. Сохраняем полученный файл. Его вес будет составлять 127 МБ (133 693 440 байт)
5. Запускаем Breed через зажатие Reset(10 секунд) при включении роутера
6. Добавляем бекап в HFS
7. В Putty вводим команды на стирание и запись нашего бекапа

**- flash erase 0x80000 0x7f00000**

**- wget на файл в HFS**

**- flash write 0x80000 0x80001000 0x7f80000**

8. Через интерфейс Breed обновляем загрузчик на стоковый STOCK_u-boot.bin из папки Firmware
Upgrade -> Bootloader -> Upload

После перезагрузки загрузится OpenWRT
