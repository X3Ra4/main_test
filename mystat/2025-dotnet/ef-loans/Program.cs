using Microsoft.EntityFrameworkCore;

Console.OutputEncoding = System.Text.Encoding.UTF8;
using var db = new LoanContext();
db.Database.EnsureCreated();
if (!db.Loans.Any())
{
    var client = new Client { Name = "Олена" };
    db.Loans.AddRange(new BookLoan { Book = new Book { Title = "Місто" }, Client = client },
                      new BookLoan { Book = new Book { Title = "Лісова пісня" }, Client = client });
    db.SaveChanges();
}

while (true)
{
    Console.WriteLine("Активні позики:");
    foreach (var loan in db.Loans.Where(x => x.ReturnDate == null).Include(x => x.Book).Include(x => x.Client).ToList())
        Console.WriteLine($"{loan.Id} · {loan.Book.Title} · {loan.Client.Name}");
    Console.Write("ID позики для повернення (0 — вихід): ");
    var command = Console.ReadLine();
    if (command is null or "0") break;
    if (!int.TryParse(command, out int id)) { Console.WriteLine("Введіть число."); continue; }
    var changed = db.Loans.Where(x => x.Id == id && x.ReturnDate == null)
        .ExecuteUpdate(setters => setters.SetProperty(x => x.ReturnDate, DateTime.UtcNow));
    Console.WriteLine(changed == 1 ? "Книгу повернуто." : "Активну позику не знайдено.");
}

sealed class Book { public int Id { get; set; } public string Title { get; set; } = ""; }
sealed class Client { public int Id { get; set; } public string Name { get; set; } = ""; }
sealed class BookLoan
{
    public int Id { get; set; }
    public Book Book { get; set; } = null!;
    public Client Client { get; set; } = null!;
    public DateTime LoanDate { get; set; } = DateTime.UtcNow;
    public DateTime? ReturnDate { get; set; }
}
sealed class LoanContext : DbContext
{
    public DbSet<BookLoan> Loans => Set<BookLoan>();
    protected override void OnConfiguring(DbContextOptionsBuilder options) => options.UseSqlite("Data Source=loans.db");
    protected override void OnModelCreating(ModelBuilder model) => model.Entity<BookLoan>().ToTable("BookLoans");
}
