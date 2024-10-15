# bot/database.py

import asyncpg
import os

async def conectar_db():
    return await asyncpg.connect(os.getenv("DATABASE_URL"))

async def criar_tabelas(conn):
    await conn.execute("""
    CREATE TABLE IF NOT EXISTS jogadores (
        id SERIAL PRIMARY KEY,
        user_id BIGINT UNIQUE,
        saldo INTEGER DEFAULT 0,
        banco INTEGER DEFAULT 0,
        nivel INTEGER DEFAULT 1,
        experiencia INTEGER DEFAULT 0,
        karma INTEGER DEFAULT 0,
        reputacao INTEGER DEFAULT 0
    );

    CREATE TABLE IF NOT EXISTS pets (
        id SERIAL PRIMARY KEY,
        user_id BIGINT,
        nome VARCHAR(50),
        nivel INTEGER DEFAULT 1,
        habilidade VARCHAR(50),
        FOREIGN KEY (user_id) REFERENCES jogadores (user_id)
    );

    CREATE TABLE IF NOT EXISTS missoes (
        id SERIAL PRIMARY KEY,
        descricao TEXT,
        recompensa INTEGER,
        tipo VARCHAR(20),
        ativo BOOLEAN DEFAULT TRUE
    );

    CREATE TABLE IF NOT EXISTS crafting_materials (
        id SERIAL PRIMARY KEY,
        user_id BIGINT,
        nome VARCHAR(50),
        quantidade INTEGER DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES jogadores (user_id)
    );

    CREATE TABLE IF NOT EXISTS alianças (
        id SERIAL PRIMARY KEY,
        nome VARCHAR(50),
        lider BIGINT,
        FOREIGN KEY (lider) REFERENCES jogadores (user_id)
    );

    CREATE TABLE IF NOT EXISTS propriedades (
        id SERIAL PRIMARY KEY,
        user_id BIGINT,
        tipo VARCHAR(50),
        nivel INTEGER DEFAULT 1,
        FOREIGN KEY (user_id) REFERENCES jogadores (user_id)
    );

    CREATE TABLE IF NOT EXISTS inventario (
        id SERIAL PRIMARY KEY,
        user_id BIGINT,
        item_nome VARCHAR(50),
        quantidade INTEGER DEFAULT 1,
        FOREIGN KEY (user_id) REFERENCES jogadores (user_id)
    );

    CREATE TABLE IF NOT EXISTS leiloes (
        id SERIAL PRIMARY KEY,
        item_nome VARCHAR(50),
        preco_inicial INTEGER,
        preco_atual INTEGER,
        dono_id BIGINT,
        comprador_id BIGINT,
        FOREIGN KEY (dono_id) REFERENCES jogadores (user_id),
        FOREIGN KEY (comprador_id) REFERENCES jogadores (user_id)
    );

    CREATE TABLE IF NOT EXISTS eventos (
        id SERIAL PRIMARY KEY,
        tipo VARCHAR(50),
        descricao TEXT,
        data_inicio TIMESTAMP,
        data_fim TIMESTAMP
    );
    """)

async def inicializar_db():
    conn = await conectar_db()
    await criar_tabelas(conn)
    return conn
