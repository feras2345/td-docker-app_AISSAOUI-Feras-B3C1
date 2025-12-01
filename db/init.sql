CREATE TABLE IF NOT EXISTS items (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO items (name, description) VALUES
    ('Tâche 1', 'Première tâche du TD Docker'),
    ('Tâche 2', 'Deuxième élément de test'),
    ('Tâche 3', 'Troisième item pour validation')
ON CONFLICT DO NOTHING;
