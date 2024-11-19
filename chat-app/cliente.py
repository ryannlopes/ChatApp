import tkinter as tk
from tkinter import scrolledtext
import socket
import threading

# Função para enviar mensagens
def send_message():
    message = f"{nickname}: {msg_entry.get()}"
    client_socket.send(message.encode('utf-8'))
    display_message(message, True)  # Mostrar no balão como mensagem do próprio usuário
    msg_entry.delete(0, tk.END)

# Função para exibir mensagens na tela
def display_message(message, own_message=False):
    chat_area.config(state='normal')

    # Criar um frame para organizar a mensagem em balão
    msg_frame = tk.Frame(chat_area, bg="#DCF8C6" if own_message else "#FFFFFF", bd=2, relief="solid")
    msg_label = tk.Label(msg_frame, text=message, bg="#DCF8C6" if own_message else "#FFFFFF", font=("Helvetica", 12), wraplength=250, anchor="w", justify="left")
    msg_label.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    # Inserir no final do scrolledtext como widget embutido
    chat_area.window_create(tk.END, window=msg_frame)
    chat_area.insert(tk.END, '\n')  # Adicionar uma quebra de linha para espaçamento
    chat_area.config(state='disabled')
    chat_area.yview(tk.END)  # Rolagem automática para a última mensagem

# Função para receber mensagens do servidor
def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            display_message(message)  # Mostrar mensagem recebida de outros usuários
        except:
            print("Conexão com o servidor perdida.")
            break

# Configuração do cliente
server_host = '127.0.0.1'
server_port = 5555
nickname = input("Escolha seu nickname: ")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_host, server_port))

# Envia o nickname para o servidor
client_socket.send(nickname.encode('utf-8'))

# Interface Gráfica
app = tk.Tk()
app.title("WhatsApp Clone")
app.geometry("400x500")
app.config(bg="#128C7E")

# Área de chat com mensagens em balão
chat_area = scrolledtext.ScrolledText(app, wrap=tk.WORD, state='disabled', bg="#ECE5DD", font=("Helvetica", 12))
chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Campo de entrada de mensagem e botão de envio
bottom_frame = tk.Frame(app, bg="#128C7E")
bottom_frame.pack(padx=10, pady=5, fill=tk.X)

msg_entry = tk.Entry(bottom_frame, font=("Helvetica", 12))
msg_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)

send_button = tk.Button(bottom_frame, text="Enviar", bg="#25D366", fg="white", font=("Helvetica", 10, "bold"), command=send_message)
send_button.pack(side=tk.RIGHT, padx=5, pady=5)

# Thread para receber mensagens
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# Loop da interface
app.mainloop()
