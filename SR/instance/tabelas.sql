-- SQLite
CREATE TABLE ProjetoKeyUser (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    projeto_id INTEGER,
    funcionario_id INTEGER,
    FOREIGN KEY (projeto_id) REFERENCES Projeto(id),
    FOREIGN KEY (funcionario_id) REFERENCES Funcionarios(id)
);

CREATE TABLE ProjetoSuperintendencia (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    projeto_id INTEGER,
    superintendencia_id INTEGER,
    FOREIGN KEY (projeto_id) REFERENCES Projeto(id),
    FOREIGN KEY (superintendencia_id) REFERENCES Superintendentes(id)
);