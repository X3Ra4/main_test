using Microsoft.EntityFrameworkCore;

Console.OutputEncoding = System.Text.Encoding.UTF8;
var connection = Environment.GetEnvironmentVariable("MYSTAT_CARS_SQL");
if (string.IsNullOrWhiteSpace(connection)) { Console.WriteLine("Задайте MYSTAT_CARS_SQL."); return; }
using var db = new CarContext(connection);
db.Database.EnsureCreated();
while (true)
{
    Console.WriteLine("1 Додати | 2 Список | 3 Редагувати | 4 Видалити | 5 Пошук | 0 Вихід");
    try
    {
        switch (Console.ReadLine())
        {
            case null or "0": return;
            case "1": var car = new Car(); Fill(car); db.Add(car); db.SaveChanges(); break;
            case "2": Print(db.Cars.AsNoTracking().OrderBy(item => item.LicensePlate)); break;
            case "3":
                var found = db.Cars.Find(ConsoleInput.Number("ID"));
                if (found is null) { Console.WriteLine("Автомобіль не знайдено."); break; }
                Fill(found); db.SaveChanges(); break;
            case "4":
                var removed = db.Cars.Find(ConsoleInput.Number("ID"));
                if (removed is null) { Console.WriteLine("Автомобіль не знайдено."); break; }
                db.Remove(removed); db.SaveChanges(); break;
            case "5":
                var search = ConsoleInput.Read("Номер, марка, модель, власник або ID");
                var id = int.TryParse(search, out var parsed) ? parsed : -1;
                Print(db.Cars.AsNoTracking().Where(item => item.Id == id || item.Brand.Contains(search)
                    || item.LicensePlate.Contains(search) || item.OwnerName.Contains(search) || item.Model.Contains(search)));
                break;
        }
    }
    catch (EndOfStreamException) { return; }
    catch (Exception e) when (e is ArgumentException or DbUpdateException)
    {
        db.ChangeTracker.Clear();
        Console.WriteLine(e is DbUpdateException ? "Не вдалося зберегти. Перевірте, чи номер унікальний." : e.Message);
    }
}

static void Fill(Car car)
{
    var plate = ConsoleInput.Read("Номер", 12).ToUpperInvariant();
    if (!plate.All(char.IsAsciiLetterOrDigit)) throw new ArgumentException("Номер має містити лише латинські літери та цифри.");
    var brand = ConsoleInput.Read("Марка", 60);
    var model = ConsoleInput.Read("Модель", 60);
    var year = ConsoleInput.Number("Рік", 1886, DateTime.UtcNow.Year + 1);
    var owner = ConsoleInput.Read("ПІБ власника");
    (car.LicensePlate, car.Brand, car.Model, car.Year, car.OwnerName) = (plate, brand, model, year, owner);
}

static void Print(IEnumerable<Car> values)
{
    foreach (var item in values) Console.WriteLine($"{item.Id} | {item.LicensePlate} | {item.Brand} {item.Model} {item.Year} | {item.OwnerName}");
}

sealed class CarContext(string connection) : DbContext
{
    public DbSet<Car> Cars => Set<Car>();
    protected override void OnConfiguring(DbContextOptionsBuilder options) => options.UseSqlServer(connection);
    protected override void OnModelCreating(ModelBuilder model) => model.Entity<Car>().HasIndex(car => car.LicensePlate).IsUnique();
}

sealed class Car
{
    public int Id { get; set; }
    [System.ComponentModel.DataAnnotations.MaxLength(12)] public string LicensePlate { get; set; } = "";
    public string Brand { get; set; } = "";
    public string Model { get; set; } = "";
    public int Year { get; set; }
    public string OwnerName { get; set; } = "";
}
