# 😍 Генератор красивых Ethereum кошельков

![Logo](pic.jpg)

## 📜 Описание проекта

Этот проект представляет собой утилиту на Python для генерации Ethereum-кошельков с кастомным началом и/или концом адреса. Программа работает с использованием многопроцессорности, что ускоряет генерацию кошельков на многопроцессорных системах.

Как только кошелек, удовлетворяющий условиям поиска, найден, программа завершает работу и выводит соответствующую информацию: сид-фразу, приватный ключ и Ethereum-адрес, а также записывает результат в файл.

## ⚙️ Настройка

### Параметры конфигурации:
Конфигурация программы задаётся через переменную `config`, которая содержит следующие параметры:

- `address_start`: строка с началом адреса, который нужно найти. Если параметр не важен, оставьте его пустым.
- `address_end`: строка с концом адреса, который нужно найти. Если параметр не важен, оставьте его пустым.
- `num_processes`: количество параллельных процессов для генерации кошельков. По умолчанию оно равно количеству логических ядер вашего процессора.
- `show_log`: логировать ли прогресс генерации. Если `True`, программа будет выводить информацию каждые 100 попыток для каждого процесса.
- `log_count`: периодичность логирования

### 🚀 Логика работы:
1. Программа создаёт несколько процессов для параллельной генерации Ethereum-кошельков. Каждый процесс работает независимо и генерирует кошельки до тех пор, пока не будет найден адрес, соответствующий условиям поиска (начало и/или конец).
2. На каждой итерации генерации процесс проверяет, соответствует ли сгенерированный адрес заданным критериям.
3. Если адрес удовлетворяет условиям, программа завершает все процессы, выводит найденный кошелек (сид-фразу, приватный ключ и адрес) и сохраняет данные в файл.
4. Логирование прогресса отображает количество попыток для каждого процесса через каждые 100 сгенерированных кошельков, если это включено в конфигурации.

# 😍 Pretty Ethereum Wallet Generator

## 📜 Project Description

This project is a Python utility for generating Ethereum wallets with a custom starting and/or ending address. The program utilizes multiprocessing, which speeds up wallet generation on multi-core systems.

Once a wallet that meets the search criteria is found, the program terminates and outputs the corresponding information: seed phrase, private key, and Ethereum address, as well as logs the result to a file.

## ⚙️ Configuration

### Configuration Parameters:
The program configuration is specified through the `config` variable, which contains the following parameters:

- `address_start`: a string with the starting address to search for. If this parameter is not important, leave it empty.
- `address_end`: a string with the ending address to search for. If this parameter is not important, leave it empty.
- `num_processes`: the number of parallel processes for generating wallets. By default, it is set to the number of logical cores on your processor.
- `show_log`: whether to log the generation progress. If `True`, the program will output information every 100 attempts for each process.

### 🚀 Logic of Operation:
1. The program creates multiple processes for parallel Ethereum wallet generation. Each process operates independently and generates wallets until an address matching the search criteria (start and/or end) is found.
2. On each iteration of generation, the process checks if the generated address meets the specified criteria.
3. If the address meets the conditions, the program terminates all processes, outputs the found wallet (seed phrase, private key, and address), and saves the data to a file.
4. Progress logging displays the number of attempts for each process every 100 generated wallets, if enabled in the configuration.
