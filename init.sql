-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Drop tables if they exist
DROP TABLE IF EXISTS participantes_ranking CASCADE;
DROP TABLE IF EXISTS rankings CASCADE;
DROP TABLE IF EXISTS itens_comanda CASCADE;
DROP TABLE IF EXISTS comandas CASCADE;
DROP TABLE IF EXISTS agendamentos CASCADE;
DROP TABLE IF EXISTS produtos CASCADE;
DROP TABLE IF EXISTS alunos CASCADE;
DROP TABLE IF EXISTS professores CASCADE;
DROP TABLE IF EXISTS quadras CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Create enum types
CREATE TYPE user_type AS ENUM ('admin', 'professor', 'cliente');
CREATE TYPE status_comanda AS ENUM ('aberta', 'fechada', 'paga');
CREATE TYPE status_agendamento AS ENUM ('pendente', 'confirmado', 'cancelado');
CREATE TYPE categoria_ranking AS ENUM ('iniciante', 'intermediario', 'avancado');
CREATE TYPE tipo_ranking AS ENUM ('masculino', 'feminino', 'misto');

-- Create users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    user_type user_type NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create quadras table
CREATE TABLE quadras (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    valor_hora DECIMAL(10,2) NOT NULL,
    coberta BOOLEAN DEFAULT false,
    iluminacao BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create professores table
CREATE TABLE professores (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    especialidade VARCHAR(100) NOT NULL,
    percentual_padrao DECIMAL(5,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id)
);

-- Create alunos table
CREATE TABLE alunos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    professor_id INTEGER REFERENCES professores(id),
    percentual_desconto DECIMAL(5,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create produtos table
CREATE TABLE produtos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    preco DECIMAL(10,2) NOT NULL,
    estoque INTEGER NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create comandas table
CREATE TABLE comandas (
    id SERIAL PRIMARY KEY,
    cliente_id INTEGER REFERENCES users(id),
    status status_comanda NOT NULL DEFAULT 'aberta',
    valor_total DECIMAL(10,2) DEFAULT 0.0,
    forma_pagamento VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create itens_comanda table
CREATE TABLE itens_comanda (
    id SERIAL PRIMARY KEY,
    comanda_id INTEGER REFERENCES comandas(id),
    produto_id INTEGER REFERENCES produtos(id),
    quantidade INTEGER NOT NULL,
    valor_unitario DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create rankings table
CREATE TABLE rankings (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    categoria categoria_ranking NOT NULL,
    tipo tipo_ranking NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create participantes_ranking table
CREATE TABLE participantes_ranking (
    id SERIAL PRIMARY KEY,
    ranking_id INTEGER REFERENCES rankings(id),
    jogador_id INTEGER REFERENCES users(id),
    pontos INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create agendamentos table
CREATE TABLE agendamentos (
    id SERIAL PRIMARY KEY,
    quadra_id INTEGER REFERENCES quadras(id),
    cliente_id INTEGER REFERENCES users(id),
    data_hora_inicio TIMESTAMP NOT NULL,
    data_hora_fim TIMESTAMP NOT NULL,
    status status_agendamento NOT NULL DEFAULT 'pendente',
    valor DECIMAL(10,2) NOT NULL,
    observacoes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_alunos_professor ON alunos(professor_id);
CREATE INDEX idx_comandas_cliente ON comandas(cliente_id);
CREATE INDEX idx_agendamentos_quadra ON agendamentos(quadra_id);
CREATE INDEX idx_agendamentos_cliente ON agendamentos(cliente_id);
CREATE INDEX idx_participantes_ranking ON participantes_ranking(ranking_id, jogador_id);

-- Insert initial admin user (password: admin123)
INSERT INTO users (email, username, hashed_password, full_name, user_type) 
VALUES ('admin@arena.com', 'admin', 
        '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewKyNiLR5P3PseLy', 
        'Administrador', 'admin');

-- Insert sample quadras
INSERT INTO quadras (nome, descricao, valor_hora, coberta, iluminacao) VALUES
('Quadra 1', 'Quadra principal coberta', 100.00, true, true),
('Quadra 2', 'Quadra descoberta', 80.00, false, true),
('Quadra 3', 'Quadra de saibro', 120.00, false, true);

-- Insert sample produtos
INSERT INTO produtos (nome, descricao, preco, estoque, categoria) VALUES
('Água Mineral 500ml', 'Água mineral sem gás', 5.00, 100, 'Bebidas'),
('Isotônico 500ml', 'Bebida isotônica sabor laranja', 8.00, 50, 'Bebidas'),
('Bola de Tênis', 'Tubo com 3 bolas', 25.00, 30, 'Equipamentos'),
('Aluguel Raquete', 'Aluguel de raquete por hora', 20.00, 10, 'Equipamentos');

-- Create trigger for updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply trigger to all tables
CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_quadras_updated_at
    BEFORE UPDATE ON quadras
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_professores_updated_at
    BEFORE UPDATE ON professores
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_alunos_updated_at
    BEFORE UPDATE ON alunos
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_produtos_updated_at
    BEFORE UPDATE ON produtos
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_comandas_updated_at
    BEFORE UPDATE ON comandas
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_itens_comanda_updated_at
    BEFORE UPDATE ON itens_comanda
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_rankings_updated_at
    BEFORE UPDATE ON rankings
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_participantes_ranking_updated_at
    BEFORE UPDATE ON participantes_ranking
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_agendamentos_updated_at
    BEFORE UPDATE ON agendamentos
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();