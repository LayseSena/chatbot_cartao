import sqlite3

def inicializar_e_alimentar():
    conn = sqlite3.connect('cartao.db')
    cursor = conn.cursor()

    # Reset para garantir que a nova estrutura e dados sejam aplicados
    cursor.execute("DROP TABLE IF EXISTS usuarios") 
    
    cursor.execute("""
        CREATE TABLE usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            conta TEXT NOT NULL UNIQUE, 
            senha_acesso TEXT NOT NULL,  
            valor_fatura REAL NOT NULL,
            limite REAL NOT NULL,
            vencimento_fatura TEXT NOT NULL
        )
    """)

    # Lista expandida de exemplos
    exemplos = [
        ('Ricardo Oliveira', '1234-5', '1234', 2500.80, 10000.0, '05/05'),
        ('Fernanda Lima',    '9876-0', '4321', 0.0,     15000.0, '10/05'),
        ('Gabriel Santos',   '5555-1', '5555', 890.00,  3000.0,  '15/05'),
        ('Ana Beatriz',      '1111-2', '1111', 450.30,  5000.0,  '08/05'),
        ('Bruno Souza',      '2222-3', '2222', 12000.0, 20000.0, '15/05'),
        ('Carla Dias',       '3333-4', '3333', 55.00,   1200.0,  '20/05'),
        ('Diego Costa',      '4444-5', '4444', 3200.00, 8000.0,  '10/05'),
        ('Elena Torres',     '0000-1', '0001', 0.0,     50000.0, '05/05'),
        ('Fabio Junior',     '7777-7', '7777', 150.00,  2500.0,  '12/05'),
        ('Gisele Bündchen',  '9999-9', '9999', 95000.0, 500000.0,'01/05')
    ]

    cursor.executemany('''INSERT INTO usuarios 
        (nome, conta, senha_acesso, valor_fatura, limite, vencimento_fatura) 
        VALUES (?, ?, ?, ?, ?, ?)''', exemplos)

    conn.commit()
    conn.close()
    print("✅ Banco de dados REINICIADO com sucesso!")

if __name__ == "__main__":
    inicializar_e_alimentar()