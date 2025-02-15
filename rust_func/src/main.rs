use std::fs::File;                      // Работа с файлами
use std::io::{Read, Write};             // Чтение и запись в файлы
use rand::rngs::OsRng;                  // Генерация случайных чисел
use rand::RngCore;                      // Методы для случайных чисел
use aes_gcm::{Aes256Gcm, Key, Nonce};   // AES-GCM криптография
use aes_gcm::aead::{Aead, KeyInit};     // Интерфейсы шифрования
use hex;                                // Работа с HEX-кодировкой


fn generate_key() -> String {
    let mut key = [0u8; 32];
    OsRng.fill_bytes(&mut key); // Генерация случайных байт для ключа
    hex::encode(key)
}

fn encrypt_file(input_path: &str, output_path: &str, key_hex: &str) {
    let key_bytes = hex::decode(key_hex).expect("Неверный формат ключа");
    let key = aes_gcm::Key::<Aes256Gcm>::from_slice(&key_bytes); // Инициализация ключа
    let cipher = Aes256Gcm::new(key);

    let mut file = File::open(input_path).expect("Не удалось открыть файл для чтения");
    let mut data = Vec::new();
    file.read_to_end(&mut data).expect("Ошибка чтения файла");

    let mut nonce = [0u8; 12];
    OsRng.fill_bytes(&mut nonce); // Генерация nonce
    let nonce_obj = Nonce::from_slice(&nonce);

    let encrypted_data = cipher.encrypt(nonce_obj, data.as_ref()).expect("Ошибка шифрования");

    let mut output_file = File::create(output_path).expect("Ошибка создания выходного файла");
    output_file.write_all(&nonce).expect("Ошибка записи nonce");
    output_file.write_all(&encrypted_data).expect("Ошибка записи зашифрованных данных");
}

fn decrypt_file(input_path: &str, output_path: &str, key_hex: &str) {
    let key_bytes = hex::decode(key_hex).expect("Неверный формат ключа");
    let key = Key::<Aes256Gcm>::from_slice(&key_bytes);
    let cipher = Aes256Gcm::new(key);

    let mut file = File::open(input_path).expect("Не удалось открыть файл");
    let mut encrypted_data = Vec::new();
    file.read_to_end(&mut encrypted_data).expect("Ошибка чтения файла");

    if encrypted_data.len() < 12 {
        panic!("Данные слишком короткие для извлечения nonce!");
    }

    let nonce = &encrypted_data[..12]; // Первые 12 байт — это nonce
    let data = &encrypted_data[12..];  // Остальное — зашифрованный текст

    let nonce_obj = Nonce::from_slice(nonce);

    match cipher.decrypt(nonce_obj, data.as_ref()) {
        Ok(decrypted_data) => {
            let mut output_file = File::create(output_path).expect("Ошибка создания файла");
            output_file.write_all(&decrypted_data).expect("Ошибка записи данных");
            println!("Файл успешно расшифрован и сохранён как {}", output_path);
        }
        Err(e) => {
            panic!("Ошибка дешифрования: {:?}", e);
        }
    }
}


fn main() {
    let args: Vec<String> = std::env::args().collect();
    
    if args.len() < 2 {
        println!("Ошибка: недостаточно аргументов.");
        println!("Использование: <action> <input_path> <output_path> <key_hex>");
        return;
    }

    let action = &args[1];
    
    match action.as_str() {
        "encrypt" => {
            if args.len() != 5 {
                println!("Ошибка: недостаточно аргументов для шифрования.");
                return;
            }
            let input_path = &args[2];
            let output_path = &args[3];
            let key_hex = &args[4];
            encrypt_file(input_path, output_path, key_hex);
        },
        "decrypt" => {
            if args.len() != 5 {
                println!("Ошибка: недостаточно аргументов для дешифрования.");
                return;
            }
            let input_path = &args[2];
            let output_path = &args[3];
            let key_hex = &args[4];
            decrypt_file(input_path, output_path, key_hex);
        },
        "generate_key" => {
            let key = generate_key();
            println!("Сгенерированный ключ: {}", key);
        },
        _ => println!("Некорректное действие, используйте 'encrypt', 'decrypt' или 'generate_key'"),
    }
}
