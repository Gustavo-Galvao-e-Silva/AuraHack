CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS researchers (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    institution TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS papers (
    id SERIAL PRIMARY KEY,
    researcher_id INT REFERENCES researchers(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    abstract TEXT,
    published_at DATE,
    doi TEXT UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS paper_embeddings (
    id SERIAL PRIMARY KEY,
    paper_id INT REFERENCES papers(id) ON DELETE CASCADE,
    embedding VECTOR(1536)
);

CREATE INDEX IF NOT EXISTS paper_embeddings_vector_idx
ON paper_embeddings
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);