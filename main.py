import concurrent.futures
from eth_account import Account
from mnemonic import Mnemonic
from eth_utils import to_checksum_address
import multiprocessing
from datetime import datetime


# ========================= CONFIG =========================

config = {
    "address_start": "0xaf",  # Начало адреса (оставьте пустым, если не важно)
    "address_end": "",  # Конец адреса (оставьте пустым, если не важно)
    "num_processes": multiprocessing.cpu_count()-1,  # Количество процессов для параллельной работы (оптимально multiprocessing.cpu_count()-1)
    "show_log": True,  # Логировать прогресс или нет
    "log_count": 50    # Логировать каждые N генераций
}

# ========================= CONFIG =========================

# Генерация сид-фразы и получение приватного ключа и адреса
mnemo = Mnemonic("english")
Account.enable_unaudited_hdwallet_features()


def matches_address(address: str, start: str, end: str) -> bool:
    """Проверяет, соответствует ли адрес заданному началу и/или концу (игнорируя регистр)."""
    address = address.lower()  # Приводим адрес к нижнему регистру
    start = start.lower()  # Приводим начало к нижнему регистру
    end = end.lower()  # Приводим конец к нижнему регистру
    return (start == "" or address.startswith(start)) and (end == "" or address.endswith(end))


def generate_wallet() -> dict:
    """Генерирует кошелек и возвращает сид-фразу, приватный ключ и адрес."""
    seed_phrase = mnemo.generate(strength=128)
    account = Account.from_mnemonic(seed_phrase)
    private_key = account.key.hex()
    address = to_checksum_address(account.address)
    return {"seed_phrase": seed_phrase, "private_key": private_key, "address": address}


def log_progress(process_id, attempts):
    """Логирование прогресса генераций каждых 100 попыток."""
    if config["show_log"] and attempts % config["log_count"] == 0:
        print(f"Процесс {process_id}: {attempts} попыток генераций")


def save_wallet_to_file(wallet, address_start):
    """Сохраняет информацию о найденном кошельке в файл."""
    filename = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_{address_start}.txt"
    with open(filename, "w", encoding='utf-8') as f:
        f.write(f"Сид фраза: {wallet['seed_phrase']}\n")
        f.write(f"Приватный ключ: {wallet['private_key']}\n")
        f.write(f"Адрес: {wallet['address']}\n")
    print(f"Информация записана в файл: {filename}")


def wallet_search(process_id: int, stop_event) -> dict:
    """Функция для параллельного поиска нужного адреса."""
    attempts = 0

    while not stop_event.is_set():  # Проверяем флаг остановки
        wallet = generate_wallet()
        attempts += 1

        # Логирование прогресса
        log_progress(process_id, attempts)

        if matches_address(wallet["address"], config["address_start"], config["address_end"]):
            stop_event.set()  # Устанавливаем флаг остановки для других процессов
            save_wallet_to_file(wallet, config["address_start"])
            return wallet  # Возвращаем найденный кошелек


def main():
    with multiprocessing.Manager() as manager:
        stop_event = manager.Event()  # Создаем общий флаг остановки

        with concurrent.futures.ProcessPoolExecutor(max_workers=config["num_processes"]) as executor:
            # Запуск параллельных задач с передачей номера процесса и флага остановки
            futures = [executor.submit(wallet_search, process_id=i + 1, stop_event=stop_event) for i in
                       range(config["num_processes"])]

            for future in concurrent.futures.as_completed(futures):
                # Как только один из процессов найдет нужный кошелек, завершаем программу
                wallet = future.result()
                if wallet:
                    print(f"Найден кошелек!")
                    print(f"Сид фраза: {wallet['seed_phrase']}")
                    print(f"Приватный ключ: {wallet['private_key']}")
                    print(f"Адрес: {wallet['address']}")
                    break


if __name__ == "__main__":
    main()
