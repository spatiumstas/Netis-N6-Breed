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

