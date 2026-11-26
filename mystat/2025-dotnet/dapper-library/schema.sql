CREATE TABLE Books (
    Id int IDENTITY PRIMARY KEY, Title nvarchar(120) NOT NULL, Author nvarchar(120) NOT NULL,
    [Year] int NOT NULL, IsDeleted bit NOT NULL DEFAULT 0
);
CREATE TABLE Clients (
    Id int IDENTITY PRIMARY KEY, Name nvarchar(120) NOT NULL, Email nvarchar(120) NOT NULL,
    IsDeleted bit NOT NULL DEFAULT 0
);
CREATE TABLE BookLoans (
    Id int IDENTITY PRIMARY KEY, BookId int NOT NULL REFERENCES Books(Id),
    ClientId int NOT NULL REFERENCES Clients(Id), LoanDate datetime2 NOT NULL DEFAULT SYSUTCDATETIME(),
    ReturnDate datetime2 NULL
);
CREATE UNIQUE INDEX UX_BookLoans_ActiveBook ON BookLoans(BookId) WHERE ReturnDate IS NULL;
CREATE INDEX IX_BookLoans_Client ON BookLoans(ClientId, ReturnDate);
