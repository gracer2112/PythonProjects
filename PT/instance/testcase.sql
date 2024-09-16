-- SQLite
CREATE TABLE test_case (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    seq INTEGER,
    dependencia TEXT,
    id_cenario INTEGER,
    modulo TEXT,
    caso_teste TEXT,
    info_teste TEXT,
    passos TEXT,
    resultado_esperado TEXT,
    status TEXT,
    id_responsavel INTEGER,
    id_coordenador INTEGER,
    data_inicio_planejada DATE,
    data_fim_planejada DATE,
    data_inicio_realizada DATE,
    data_fim_realizada DATE,
    observacao TEXT,
    id_projeto INTEGER,
    FOREIGN KEY (id_projeto) REFERENCES projeto(id),
    FOREIGN KEY (id_responsavel) REFERENCES funcionarios(ID),
    FOREIGN KEY (id_coordenador) REFERENCES funcionarios(ID)
);