import socket
import threading
import os
import random
import customtkinter as ctk
import configparser
import time

# Global paths
scanfile_path = os.path.join(r"")  # Belirtilen bir dosya taranabilir
gud = os.path.join(r"C:\Users\ASUS\Desktop\Hack-Game\GUD")
GDLCS =  os.path.join(r"C:\Users\ASUS\Desktop\Hack-Game\DLCS")
logged_in_user_id = None

# Config parser initialization
config = configparser.ConfigParser()

# Global giriş durumu
is_logged_in = False  # Giriş yapılmadıysa False, yapıldıysa True


# Hesap oluşturma sistemi
def create_account_sys():
    create_account_win = ctk.CTk()
    create_account_win.title("Hesap Oluştur")
    create_account_win.geometry("200x150")

    def get_information():
        global gud
        names = names_entry.get().strip()
        gıdc = GIDC_entry.get().strip()
        if not names or not gıdc:
            result_label.configure(text="Ad ve GIDC gerekli!", text_color="red")
            return
        try:
            file_path = os.path.join(gud, f"{gıdc}.txt")
            if os.path.exists(file_path):
                result_label.configure(text="Bu bilgilerle hesap zaten var!", text_color="red")
                return

            with open(file_path, "w") as user_data:
                ıd_creat = random.randint(1000, 9999)
                user_data.write(f"Name: {names}\n")
                user_data.write(f"GIDC: {gıdc}\n")
                user_data.write(f"ID:{ıd_creat}\n")
            result_label.configure(text="Hesap başarıyla oluşturuldu!", text_color="green")
        except Exception as e:
            result_label.configure(text=f"Hata: {e}", text_color="red")

    # Entry fields
    names_entry = ctk.CTkEntry(create_account_win, placeholder_text="Ad")
    names_entry.pack()
    GIDC_entry = ctk.CTkEntry(create_account_win, placeholder_text="GIDC")
    GIDC_entry.pack()

    # Button
    Create_button = ctk.CTkButton(create_account_win, text="Oluştur", command=get_information)
    Create_button.pack()

    # Label
    result_label = ctk.CTkLabel(create_account_win, text="")
    result_label.pack(pady=5)

    create_account_win.mainloop()


# LUIWINX GUI window

def open_luiwinx_window():
    global logged_in_user_id

    luiwinx_window = ctk.CTk()
    luiwinx_window.title("LUIWINX Penceresi")
    luiwinx_window.geometry("300x200")
    #gui
    #functions
    #button
    #Label
    if logged_in_user_id:
        id_label = ctk.CTkLabel(luiwinx_window, text=f"Giriş Yapılan ID: {logged_in_user_id}")
        id_label.pack(pady=10)

    luiwinx_window.mainloop()


# Terminal window
def open_terminal(client_socket):
    global is_logged_in

    terminal_window = ctk.CTk()
    terminal_window.title("CRESOURC Terminal")
    terminal_window.geometry("500x300")
    terminal_window._set_appearance_mode("Dark")

    # Terminal output
    terminal_output = ctk.CTkTextbox(terminal_window, text_color="green")
    terminal_output.pack(fill="both", expand=True)

    def receive_data():
        while True:
            try:
                data = client_socket.recv(1024)
                if data:
                    terminal_output.insert("end", f"Sunucudan alınan veri: {data.decode()}\n")
                else:
                    break
            except Exception as e:
                terminal_output.insert("end", f"Bağlantı hatası: {e}\n")
                break

    threading.Thread(target=receive_data, daemon=True).start()
#Set False in loged
    def loged_system_xstats():
        is_logged_in= False

    # Command system
    def process_command(command):
        if command == "/LUIWINX":
            if not is_logged_in:
                terminal_output.insert("end", "Hata: Önce giriş yapmalısınız!\n")
            else:
                open_luiwinx_window()
        elif command == "/creataccount":
            create_account_sys()
        elif command == "/cls":
            terminal_output.delete("1.0", "end")
            os.system('cls' if os.name == 'nt' else 'clear')
        elif command == "/login":
            open_login_window()
        elif command == "/exit":
            terminal_output.insert("end", "Uygulama kapanıyor..")
            time.sleep(2)
            terminal_window.quit()
            terminal_window.destroy()
        else:
            terminal_output.insert("end", f"Komut bulunamadı: {command}\n")

    # Send data to server
    def send_data(event=None):
        send_message = terminal_input.get()
        if send_message.strip():
            if send_message.startswith("/"):  # Command check
                process_command(send_message.strip())
            else:
                client_socket.sendall(send_message.encode())
                terminal_output.insert("end", f"Sunucuya gönderilen mesaj: {send_message}\n")
            terminal_input.delete(0, "end")

    # Input
    terminal_input = ctk.CTkEntry(terminal_window, placeholder_text="Mesajınızı yazın...", text_color="green")
    terminal_input.pack(fill="x", pady=5)
    terminal_input.bind("<Return>", send_data)

    terminal_window.mainloop()


# Login window
def open_login_window():
    global is_logged_in, logged_in_user_id

    login_window = ctk.CTk()
    login_window.title("Giriş Yap")
    login_window.geometry("300x200")

    #entrys
    ad_entry = ctk.CTkEntry(login_window, placeholder_text="Ad")
    ad_entry.pack(pady=10)
    gidc_entry = ctk.CTkEntry(login_window, placeholder_text="GIDC")
    gidc_entry.pack(pady=10)

    # Giriş doğrulama fonksiyonu
    def login():
        global is_logged_in, logged_in_user_id

        ad = ad_entry.get().strip()
        gidc = gidc_entry.get().strip()
        if not ad or not gidc:
            result_label.configure(text="Ad ve GIDC gerekli!", text_color="red")
            return

        # GIDC'ye göre dosya yolu oluştur
        file_path = os.path.join(gud, f"{gidc}.txt")
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                lines = file.readlines()
                stored_name = lines[0].split(":")[1].strip()
                stored_gidc = lines[1].split(":")[1].strip()
                if ad == stored_name and gidc == stored_gidc:
                    logged_in_user_id = lines[2].split(":")[1].strip()  # ID'yi kaydet
                    is_logged_in = True
                    result_label.configure(text="Giriş başarılı!", text_color="green")
                    login_window.destroy()
                else:
                    result_label.configure(text="Hatalı giriş bilgisi!", text_color="red")
        else:
            result_label.configure(text="Hesap bulunamadı!", text_color="red")

    # Button
    login_button = ctk.CTkButton(login_window, text="Giriş Yap", command=login)
    login_button.pack(pady=10)

    # Label
    result_label = ctk.CTkLabel(login_window, text="")
    result_label.pack(pady=10)

    login_window.mainloop()


# Main lobby
def main():
    lobi = ctk.CTk()
    lobi.title("Lobi")
    lobi.geometry("300x200")

    def connect_server():
        lobi.destroy()

        connect_window = ctk.CTk()
        connect_window.title("IP ve Port Girişi")
        connect_window.geometry("300x150")

        ip_entry = ctk.CTkEntry(connect_window, placeholder_text="IP")
        ip_entry.pack(pady=10)

        port_entry = ctk.CTkEntry(connect_window, placeholder_text="Port")
        port_entry.pack(pady=10)

        def establish_connection():
            ip = ip_entry.get().strip()
            port = int(port_entry.get().strip())

            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                client_socket.connect((ip, port))
                connect_window.destroy()
                open_terminal(client_socket)
            except Exception as e:
                print(f"Bağlantı hatası: {e}")

        connect_button = ctk.CTkButton(connect_window, text="Bağlan", command=establish_connection)
        connect_button.pack(pady=10)

        connect_window.mainloop()

    connect_button = ctk.CTkButton(lobi, text="Sunucuya Bağlan", command=connect_server)
    connect_button.pack(pady=50)

    lobi.mainloop()


main()