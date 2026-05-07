import tkinter as tk
from tkinter import messagebox, ttk
import requests
import json
import os

# Константы
FAVORITES_FILE = 'favorites.json'

# Загрузка избранных пользователей
def load_favorites():
    if os.path.exists(FAVORITES_FILE):
        with open(FAVORITES_FILE, 'r') as f:
            return json.load(f)
    return []

# Сохранение избранных пользователей
def save_favorites(favorites):
    with open(FAVORITES_FILE, 'w') as f:
        json.dump(favorites, f, indent=4)

# Функция поиска пользователя
def search_user():
    username = search_entry.get().strip()
    if not username:
        messagebox.showwarning("Ошибка", "Поле поиска не должно быть пустым")
        return
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)
    if response.status_code == 200:
        user_data = response.json()
        display_results(user_data)
    else:
        messagebox.showerror("Ошибка", "Пользователь не найден")

# Отображение результатов поиска
def display_results(user_data):
    results_list.delete(0, tk.END)
    user_info = f"{user_data['login']} - {user_data.get('name', 'Нет имени')}"
    results_list.insert(tk.END, user_info)
    # Добавляем кнопку "Добавить в избранное"
    add_fav_button.config(command=lambda: add_to_favorites(user_data))

# Добавление в избранное
def add_to_favorites(user_data):
    favorites = load_favorites()
    # Проверка, есть ли уже в избранных
    if any(user['login'] == user_data['login'] for user in favorites):
        messagebox.showinfo("Информация", "Этот пользователь уже в избранных")
        return
    favorites.append(user_data)
    save_favorites(favorites)
    messagebox.showinfo("Успех", "Пользователь добавлен в избранные")

# Создание GUI
root = tk.Tk()
root.title("GitHub User Finder")

# Поле поиска
search_label = tk.Label(root, text="Введите имя пользователя GitHub:")
search_label.pack(pady=5)

search_entry = tk.Entry(root, width=40)
search_entry.pack(pady=5)

search_button = tk.Button(root, text="Поиск", command=search_user)
search_button.pack(pady=5)

# Результаты поиска
results_list = tk.Listbox(root, width=50)
results_list.pack(pady=5)

# Кнопка для добавления в избранное
add_fav_button = tk.Button(root, text="Добавить в избранное")
add_fav_button.pack(pady=5)

# Загрузка и отображение избранных при запуске (по желанию)

root.mainloop()