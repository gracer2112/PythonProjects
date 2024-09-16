-- SQLite
DROP TABLE IF EXISTS func_tecnologia;

DROP TABLE IF EXISTS Atividade;

DROP TABLE IF EXISTS tasks;


CREATE TABLE func_tecnologia (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,  -- Define a coluna ID como autoincrementável
    IDSuperintendente INTEGER,
    Nome TEXT,
    Cargo TEXT,
    Email TEXT,
    FOREIGN KEY (IDSuperintendente) REFERENCES Superintendentes(ID)  -- Define a chave estrangeira corretamente
);

delete from func_tecnologia;

INSERT INTO func_tecnologia (IDSuperintendente, Nome, Cargo, Email) 
VALUES (1, 'NomeTeste', 'CargoTeste', 'email@teste.com');
PRAGMA table_info(funcionarios);


PRAGMA table_info(func_tecnologia);

SELECT sql FROM sqlite_master WHERE type='table' AND name='funcionarios';

DBCC CHECKIDENT ('func_tecnologia', RESEED, 0);

-- Remova todos os registros da tabela
DELETE FROM func_tecnologia;

-- Resete o autoincremento
DELETE FROM sqlite_sequence WHERE name='func_tecnologia';