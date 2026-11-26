using Dapper;
using Microsoft.Data.SqlClient;

Console.OutputEncoding = System.Text.Encoding.UTF8;
var connection = Environment.GetEnvironmentVariable("MYSTAT_LIBRARY_SQL");
if (string.IsNullOrWhiteSpace(connection))
{
    Console.Error.WriteLine("Задайте MYSTAT_LIBRARY_SQL.");
    return;
}
using var db = new SqlConnection(connection);
db.Open();
while (true)
{
    Console.WriteLine("1 Книга | 2 Клієнт | 3 Видати | 4 Активні позики | 5 Повернути | 6 Видалити книгу | 7 Видалити клієнта | 8 Каталог | 0 Вихід");
    try
    {
        switch (Console.ReadLine()?.Trim())
        {
            case null or "0": return;
            case "1":
                db.Execute("INSERT Books(Title, Author, [Year]) VALUES (@Title,@Author,@Year)",
                    new {Title=ConsoleInput.Read("Назва"), Author=ConsoleInput.Read("Автор"), Year=ConsoleInput.Number("Рік",1,DateTime.UtcNow.Year)});
                break;
            case "2":
                var name = ConsoleInput.Read("Ім’я");
                var email = new System.Net.Mail.MailAddress(ConsoleInput.Read("Email")).Address;
                db.Execute("INSERT Clients(Name, Email) VALUES (@name,@email)", new {name,email});
                break;
            case "3":
                var bookId = ConsoleInput.Number("ID книги");
                var clientId = ConsoleInput.Number("ID клієнта");
                using (var transaction = db.BeginTransaction(System.Data.IsolationLevel.Serializable))
                {
                    var changed = db.Execute("""
                        INSERT BookLoans(BookId, ClientId) SELECT b.Id, c.Id
                        FROM Books b CROSS JOIN Clients c
                        WHERE b.Id=@bookId AND c.Id=@clientId AND b.IsDeleted=0 AND c.IsDeleted=0
                        AND NOT EXISTS(SELECT 1 FROM BookLoans l WHERE l.BookId=b.Id AND l.ReturnDate IS NULL)
                        """, new {bookId,clientId}, transaction);
                    transaction.Commit();
                    Console.WriteLine(changed == 1 ? "Видано" : "Книгу або клієнта не знайдено, або книгу вже видано.");
                }
                break;
            case "4":
                foreach (var row in db.Query("""
                    SELECT l.Id,b.Title,c.Name,l.LoanDate FROM BookLoans l
                    JOIN Books b ON b.Id=l.BookId JOIN Clients c ON c.Id=l.ClientId
                    WHERE l.ReturnDate IS NULL ORDER BY l.LoanDate, l.Id
                    """)) Console.WriteLine($"{row.Id} | {row.Title} | {row.Name} | {row.LoanDate:u}");
                break;
            case "5":
                Console.WriteLine(db.Execute("UPDATE BookLoans SET ReturnDate=SYSUTCDATETIME() WHERE Id=@id AND ReturnDate IS NULL",
                     new {id=ConsoleInput.Number("ID позики")}) == 1 ? "Повернуто" : "Активну позику не знайдено.");
                break;
            case "6":
                Remove(db, true);
                break;
            case "7":
                Remove(db, false);
                break;
            case "8":
                foreach (var row in db.Query("SELECT Id, Title, Author FROM Books WHERE IsDeleted=0 ORDER BY Title"))
                    Console.WriteLine($"Книга {row.Id} | {row.Title} | {row.Author}");
                foreach (var row in db.Query("SELECT Id, Name FROM Clients WHERE IsDeleted=0 ORDER BY Name"))
                    Console.WriteLine($"Клієнт {row.Id} | {row.Name}");
                break;
        }
    }
    catch (EndOfStreamException) { return; }
    catch (Exception error) when (error is ArgumentException or FormatException or SqlException)
    { Console.WriteLine("Операцію не виконано: " + (error is SqlException ? "помилка бази даних" : error.Message)); }
}

static void Remove(SqlConnection db, bool book)
{
    var id = ConsoleInput.Number("ID");
    using var transaction = db.BeginTransaction(System.Data.IsolationLevel.Serializable);
    var sql = book
        ? "UPDATE Books SET IsDeleted=1 WHERE Id=@id AND IsDeleted=0 AND NOT EXISTS(SELECT 1 FROM BookLoans WHERE BookId=@id AND ReturnDate IS NULL)"
        : "UPDATE Clients SET IsDeleted=1 WHERE Id=@id AND IsDeleted=0 AND NOT EXISTS(SELECT 1 FROM BookLoans WHERE ClientId=@id AND ReturnDate IS NULL)";
    int changed = db.Execute(sql, new {id}, transaction);
    transaction.Commit();
    Console.WriteLine(changed == 1 ? "Видалено з каталогу" : "Запис не знайдено або існує активна позика.");
}
