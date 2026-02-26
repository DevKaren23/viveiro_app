CREATE TABLE IF NOT EXISTS especies (
    id SERIAL PRIMARY KEY,
    nome_popular TEXT NOT NULL,
    nome_cientifico TEXT NOT NULL,
    observacoes TEXT,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS lotes (
    id SERIAL PRIMARY KEY,
    especie_id INTEGER NOT NULL REFERENCES especies(id) ON DELETE CASCADE,
    codigo_lote TEXT NOT NULL,
    quantidade INTEGER NOT NULL,
    data_semeadura DATE,
    status TEXT
);

CREATE TABLE IF NOT EXISTS qualidade (
    id SERIAL PRIMARY KEY,
    lote_id INTEGER NOT NULL REFERENCES lotes(id) ON DELETE CASCADE,
    altura REAL,
    diametro REAL,
    sanidade TEXT,
    vigor TEXT,
    nota REAL,
    classificacao TEXT,
    data_avaliacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS movimentacoes (
    id SERIAL PRIMARY KEY,
    lote_id INTEGER NOT NULL REFERENCES lotes(id) ON DELETE CASCADE,
    tipo TEXT NOT NULL,
    quantidade INTEGER NOT NULL,
    motivo TEXT,
    data_movimentacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);