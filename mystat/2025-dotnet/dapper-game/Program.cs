using Dapper;
using Microsoft.Data.SqlClient;

Console.OutputEncoding = System.Text.Encoding.UTF8;
string? connection = Environment.GetEnvironmentVariable("MYSTAT_GAME_SQL");
if (string.IsNullOrWhiteSpace(connection))
{
    Console.Error.WriteLine("Задайте MYSTAT_GAME_SQL.");
    return;
}
using var db = new SqlConnection(connection);
db.Open();
var storage = new Repository(db);
User? active = null;
while (true)
{
    try
    {
        if (active is null)
        {
            Console.WriteLine("1 Реєстрація | 2 Увійти | 0 Вихід");
            var action = Console.ReadLine();
            if (action is null or "0") return;
            if (action is not ("1" or "2")) continue;
            var username = ConsoleInput.Read("Логін", 50);
            var password = ConsoleInput.Secret("Пароль");
            if (action == "1") { storage.Register(username, Passwords.Hash(password)); Console.WriteLine("Акаунт створено."); }
            else
            {
                var user = storage.Find(username);
                if (user is null || !Passwords.Verify(password, user.Password)) Console.WriteLine("Невірні дані.");
                else active = user;
            }
            continue;
        }

        Console.WriteLine("1 Створити | 2 Мої персонажі | 3 Видалити | 4 Редагувати | 5 Додати досвід | 6 Вийти з акаунта | 0 Завершити");
        switch (Console.ReadLine())
        {
            case null or "0": return;
            case "1": storage.Create(active.Id, ReadCharacter(storage)); break;
            case "2":
                foreach (var c in storage.List(active.Id))
                    Console.WriteLine($"{c.Id} | {c.Name} | рів. {c.Level} | XP {c.Experience} | DMG {c.Damage} | DEF {c.Protection} | HP {c.HP} | MP {c.MP}");
                break;
            case "3": Report(storage.Delete(active.Id, ConsoleInput.Number("ID"))); break;
            case "4": int id = ConsoleInput.Number("ID"); Report(storage.Update(active.Id, id, ReadCharacter(storage))); break;
            case "5":
                var result = storage.Grant(active.Id, ConsoleInput.Number("ID"), ConsoleInput.Number("Досвід"));
                Console.WriteLine(result ?? "Власного персонажа не знайдено.");
                break;
            case "6": active = null; break;
        }
    }
    catch (EndOfStreamException) { return; }
    catch (ArgumentException error) { Console.WriteLine(error.Message); }
    catch (SqlException error) { Console.WriteLine(error.Number is 2601 or 2627 ? "Логін уже існує." : "Помилка бази даних."); }
}

static void Report(bool changed) => Console.WriteLine(changed ? "Оновлено." : "Власного персонажа не знайдено.");

static Stats ReadCharacter(Repository repo)
{
    foreach (var item in repo.Classes()) Console.WriteLine($"{item.Id} {item.ClassName} · {item.Description}");
    var stats = new Stats(ConsoleInput.Read("Ім’я", 50), ConsoleInput.Number("Клас"),
        ConsoleInput.Number("Шкода"), ConsoleInput.Number("Захист", 0), ConsoleInput.Number("HP"), ConsoleInput.Number("MP", 0));
    if (!repo.Classes().Any(c => c.Id == stats.ClassId)) throw new ArgumentException("Невідомий клас.");
    return stats;
}

record User(int Id, string Username, string Password);
record CharacterClass(int Id, string ClassName, string Description);
record Character(int Id, string Name, int Level, int Experience, int Damage, int Protection, int HP, int MP);
record Stats(string Name, int ClassId, int Damage, int Protection, int HP, int MP);

static class Progression
{
    public static (int Level, int Xp) Add(int previousLevel, int oldXp, int points)
    {
        int xp = checked((int)Math.Min((long)oldXp + points, int.MaxValue));
        int level = previousLevel;
        long cost = 100L << (level - 1);
        while (level < 25 && xp >= cost)
        {
            xp -= (int)cost;
            ++level;
            cost *= 2;
        }
        return (level, xp);
    }
}

sealed class Repository(SqlConnection db)
{
    public void Register(string name, string hash) =>
        db.Execute("INSERT Users(Username,Password) VALUES(@name,@hash)", new { name, hash });
    public User? Find(string name) => db.QuerySingleOrDefault<User>(
        "SELECT Id,Username,Password FROM Users WHERE Username=@name", new {name});
    public IEnumerable<CharacterClass> Classes() => db.Query<CharacterClass>("SELECT Id,ClassName,Description FROM CharacterClasses ORDER BY Id");
    public IEnumerable<Character> List(int userId) => db.Query<Character>(
        "SELECT Id,Name,Level,Experience,Damage,Protection,HP,MP FROM Characters WHERE UserId=@userId ORDER BY Id", new {userId});
    public void Create(int userId, Stats s) => db.Execute("""
        INSERT Characters(Name,ClassId,Damage,Protection,HP,MP,UserId)
        VALUES(@Name,@ClassId,@Damage,@Protection,@HP,@MP,@userId)
        """, new {s.Name,s.ClassId,s.Damage,s.Protection,s.HP,s.MP,userId});
    public bool Update(int userId, int id, Stats s) => db.Execute("""
        UPDATE Characters SET Name=@Name,ClassId=@ClassId,Damage=@Damage,Protection=@Protection,HP=@HP,MP=@MP
        WHERE Id=@id AND UserId=@userId
        """, new {s.Name,s.ClassId,s.Damage,s.Protection,s.HP,s.MP,id,userId}) == 1;
    public bool Delete(int userId, int id) => db.Execute("DELETE Characters WHERE Id=@id AND UserId=@userId", new {id,userId}) == 1;

    public string? Grant(int userId, int id, int points)
    {
        using var transaction = db.BeginTransaction();
        var previous = db.QuerySingleOrDefault<Character>("""
            SELECT Id,Name,Level,Experience,Damage,Protection,HP,MP FROM Characters WITH (UPDLOCK)
            WHERE Id=@id AND UserId=@userId
            """, new {id,userId}, transaction);
        if (previous is null) return null;
        var (level, xp) = Progression.Add(previous.Level, previous.Experience, points);
        db.Execute("UPDATE Characters SET Level=@level,Experience=@xp WHERE Id=@id AND UserId=@userId", new {level,xp,id,userId}, transaction);
        transaction.Commit();
        return level > previous.Level ? $"Новий рівень: {level}, залишок XP: {xp}" : $"Поточні XP: {xp}";
    }
}
