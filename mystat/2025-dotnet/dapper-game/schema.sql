CREATE TABLE Users (
    Id int IDENTITY PRIMARY KEY, Username nvarchar(50) NOT NULL UNIQUE, Password nvarchar(255) NOT NULL
);
CREATE TABLE CharacterClasses (
    Id int IDENTITY PRIMARY KEY, ClassName nvarchar(50) NOT NULL UNIQUE, Description nvarchar(250) NOT NULL
);
CREATE TABLE Characters (
    Id int IDENTITY PRIMARY KEY, Name nvarchar(50) NOT NULL, Level int NOT NULL DEFAULT 1,
    Experience int NOT NULL DEFAULT 0, Damage int NOT NULL, Protection int NOT NULL, HP int NOT NULL, MP int NOT NULL,
    UserId int NOT NULL REFERENCES Users(Id), ClassId int NOT NULL REFERENCES CharacterClasses(Id)
);
INSERT CharacterClasses(ClassName,Description) VALUES
(N'Воїн',N'Міцний захист'),(N'Маг',N'Висока мана'),(N'Слідопит',N'Збалансовані характеристики');
