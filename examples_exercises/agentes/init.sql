CREATE TABLE IF NOT EXISTS conversations (
    id SERIAL PRIMARY KEY,
    ticket_id INT NOT NULL,
    conversation_id INT NOT NULL,
    user_id INT NOT NULL,
    speaker VARCHAR(50) NOT NULL,
    message TEXT NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    ticket_status VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS agent_configs (
    id SERIAL PRIMARY KEY,
    agent_name VARCHAR(100) NOT NULL UNIQUE,
    agent_type VARCHAR(100) NOT NULL,
    objective TEXT NOT NULL,
    system_prompt TEXT NOT NULL,
    model_name VARCHAR(100) DEFAULT 'gpt-4.1-mini',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS agent_runs (
    id SERIAL PRIMARY KEY,
    agent_name VARCHAR(100) NOT NULL,
    ticket_id INT,
    input_text TEXT,
    output_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS feedbacks (
    feedback_id INT PRIMARY KEY,
    feedback_text TEXT,
    created_at TIMESTAMP,
    channel VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS ticket_memory (
    ticket_id INT PRIMARY KEY,
    problem TEXT,
    attempted_solutions TEXT,
    current_status TEXT,
    last_client_message TEXT,
    resolved BOOLEAN,
    signals TEXT,
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS sensitive_items (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    type TEXT NOT NULL,
    risk TEXT NOT NULL,
    category TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS internal_notes (
    id SERIAL PRIMARY KEY,
    ticket_id INT,
    note_text TEXT NOT NULL,
    note_status TEXT NOT NULL,
    blocked_reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS tickets (
    id SERIAL PRIMARY KEY,
    cliente VARCHAR(100),
    mensagem TEXT,
    categoria VARCHAR(50),
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS backlog (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    responsavel VARCHAR(100),
    status VARCHAR(50) NOT NULL,
    prioridade VARCHAR(20) NOT NULL,
    story_points INTEGER,
    dias_em_aberto INTEGER DEFAULT 0,
    bugs_relacionados INTEGER DEFAULT 0,
    sprint VARCHAR(50),
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS knowledge_bases (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS kb_documents (
    id SERIAL PRIMARY KEY,
    kb_id INT NOT NULL REFERENCES knowledge_bases(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    source VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS kb_chunks (
    id SERIAL PRIMARY KEY,
    document_id INT NOT NULL REFERENCES kb_documents(id) ON DELETE CASCADE,
    chunk_order INT NOT NULL,
    content TEXT NOT NULL,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO tickets (cliente, mensagem, categoria)
SELECT * FROM (
    VALUES
    ('Maria', 'App crashed when trying to pay', 'bug'),
    ('João', 'I really liked the new interface', 'praise'),
    ('Ana', 'I cannot log in', 'bug'),
    ('Carlos', 'Payment was charged twice', 'payment'),
    ('Fernanda', 'System is very slow', 'performance')
) AS v(cliente, mensagem, categoria)
WHERE NOT EXISTS (SELECT 1 FROM tickets);

INSERT INTO knowledge_bases (name, description)
VALUES
('support_kb', 'Common support issues'),
('policy_kb', 'Internal policies'),
('product_faq', 'Product FAQ')
ON CONFLICT (name) DO NOTHING;

INSERT INTO kb_documents (kb_id, title, source)
SELECT kb.id, v.title, v.source
FROM (
    VALUES
    ('support_kb', 'Payment errors', 'manual'),
    ('support_kb', 'Login issues', 'manual'),
    ('support_kb', 'System slowness', 'manual'),
    ('support_kb', 'Mobile app failures', 'manual'),
    ('policy_kb', 'Refund policy', 'manual'),
    ('policy_kb', 'Security policy', 'manual'),
    ('policy_kb', 'Data privacy', 'manual'),
    ('product_faq', 'Mobile app FAQ', 'manual'),
    ('product_faq', 'Account and registration FAQ', 'manual')
) AS v(kb_name, title, source)
JOIN knowledge_bases kb ON kb.name = v.kb_name
WHERE NOT EXISTS (
    SELECT 1
    FROM kb_documents d
    WHERE d.kb_id = kb.id AND d.title = v.title
);

INSERT INTO kb_chunks (document_id, chunk_order, content, metadata)
SELECT d.id, v.chunk_order, v.content, v.metadata::jsonb
FROM (
    VALUES
    ('Payment errors', 1, 'Duplicate charges may occur due to transaction confirmation failure', '{"category":"payment"}'),
('Payment errors', 2, 'Always check history before requesting a refund', '{"category":"payment"}'),
('Payment errors', 3, 'Failures may occur due to timeout or provider rejection', '{"category":"payment"}'),
('Login issues', 1, 'Users should verify email and password before resetting access', '{"category":"login"}'),
('Login issues', 2, 'Temporary blocks occur after multiple invalid attempts', '{"category":"login"}'),
('Login issues', 3, 'Password recovery must be done via registered email', '{"category":"login"}'),
('System slowness', 1, 'System may become slow during peak hours', '{"category":"performance"}'),
('System slowness', 2, 'It is recommended to check user connection', '{"category":"performance"}'),
('System slowness', 3, 'Local cache may impact app performance', '{"category":"performance"}'),
('Mobile app failures', 1, 'Issues may occur on older versions of the application', '{"category":"mobile"}'),
('Mobile app failures', 2, 'Updating the app may solve most errors', '{"category":"mobile"}'),
('Mobile app failures', 3, 'Sync failures may occur without internet', '{"category":"mobile"}'),
('Refund policy', 1, 'Refunds can be requested within 7 days', '{"category":"policy"}'),
('Refund policy', 2, 'Exceptional cases must be reviewed manually', '{"category":"policy"}'),
('Security policy', 1, 'Users must keep their credentials secure', '{"category":"security"}'),
('Security policy', 2, 'Do not share passwords with others', '{"category":"security"}'),
('Data privacy', 1, 'Personal data is protected according to LGPD', '{"category":"privacy"}'),
('Data privacy', 2, 'Users can request data deletion', '{"category":"privacy"}'),
('Mobile app FAQ', 1, 'App is available for Android and iOS', '{"category":"faq"}'),
('Mobile app FAQ', 2, 'Requires internet connection', '{"category":"faq"}'),
('Account and registration FAQ', 1, 'Registration requires a valid email', '{"category":"faq"}'),
('Account and registration FAQ', 2, 'Account can be deleted via support', '{"category":"faq"}')
) AS v(title, chunk_order, content, metadata)
JOIN kb_documents d ON d.title = v.title
WHERE NOT EXISTS (
    SELECT 1
    FROM kb_chunks c
    WHERE c.document_id = d.id AND c.chunk_order = v.chunk_order
);

