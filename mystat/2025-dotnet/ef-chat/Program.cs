using System.Net;
using System.Net.Sockets;
using System.Text.Json;
using Microsoft.EntityFrameworkCore;

Console.OutputEncoding = System.Text.Encoding.UTF8;
const int port = 8133;
if (args.FirstOrDefault() == "server")
{
    using (var db = new ChatDb())
    {
        db.Database.EnsureCreated();
        if (!db.Admins.Any())
        {
            string initial = Environment.GetEnvironmentVariable("MYSTAT_CHAT_ADMIN_PASSWORD")
                ?? throw new InvalidOperationException("Задайте MYSTAT_CHAT_ADMIN_PASSWORD.");
            db.Admins.Add(new Admin { Name = "admin", Hash = Passwords.Hash(initial) });
            db.SaveChanges();
        }
    }
    var listener = new TcpListener(IPAddress.Loopback, port);
    listener.Start();
    Console.WriteLine($"Chat on 127.0.0.1:{port}");
    while (true)
    {
        var client = await listener.AcceptTcpClientAsync();
        _ = Task.Run(async () =>
        {
            try { await Handle(client); }
            catch (Exception error) when (error is IOException or SocketException or DbUpdateException)
            { Console.Error.WriteLine("Помилка сесії."); }
        });
    }
}
else if (args.FirstOrDefault() == "client")
{
    using var client = new TcpClient();
    await client.ConnectAsync(IPAddress.Loopback, port);
    using var reader = new StreamReader(client.GetStream());
    using var writer = new StreamWriter(client.GetStream()) { AutoFlush = true };
    await Send(new Command("login", ConsoleInput.Read("Логін", 50), ConsoleInput.Secret("Пароль")));
    if (await reader.ReadLineAsync() != "OK") { Console.WriteLine("Не вдалося увійти."); return; }
    Console.WriteLine("send | history | add-client | add-admin | remove-client | quit");
    while (Console.ReadLine() is string action)
    {
        Command? command = action switch
        {
            "send" => new Command(action, ConsoleInput.Read("Повідомлення", 500)),
            "add-client" or "add-admin" => new Command(action, ConsoleInput.Read("Логін", 50), ConsoleInput.Secret("Пароль")),
            "remove-client" => new Command(action, ConsoleInput.Read("Логін", 50)),
            "history" or "quit" => new Command(action),
            _ => null
        };
        if (command is null) continue;
        await Send(command);
        var result = await reader.ReadLineAsync();
        if (result is null || action == "quit") return;
        Console.WriteLine(result == "OK" ? "Готово." : result);
    }

    Task Send(Command value) => writer.WriteLineAsync(JsonSerializer.Serialize(value));
}
else Console.WriteLine("dotnet run -- server | client");

static async Task Handle(TcpClient client)
{
    using (client)
    using (var reader = new StreamReader(client.GetStream()))
    using (var writer = new StreamWriter(client.GetStream()) { AutoFlush = true })
    {
        string? name = null;
        bool admin = false;
        while (await reader.ReadLineAsync() is string line)
        {
            if (line.Length > 4096) return;
            Command? command;
            try { command = JsonSerializer.Deserialize<Command>(line); }
            catch (JsonException) { await writer.WriteLineAsync("Некоректний запит"); continue; }
            if (command is null) continue;
            if (command.Action == "quit") return;
            using var db = new ChatDb();
            if (name is null)
            {
                if (command.Action != "login" || !Valid(command.Text, 50) || !Valid(command.Password, 120))
                { await writer.WriteLineAsync("Відмовлено"); return; }
                string login = command.Text!.ToLowerInvariant();
                var adminAccount = await db.Admins.FindAsync(login);
                var userAccount = adminAccount is null ? await db.Clients.FindAsync(login) : null;
                string? hash = adminAccount?.Hash ?? userAccount?.Hash;
                if (hash is null || !Passwords.Verify(command.Password!, hash))
                { await writer.WriteLineAsync("Відмовлено"); return; }
                name = login;
                admin = adminAccount is not null;
                await writer.WriteLineAsync("OK");
                continue;
            }
            if (!admin && await db.Clients.FindAsync(name) is null)
            { await writer.WriteLineAsync("Клієнта видалено"); return; }

            if (command.Action == "history")
            {
                var history = await db.Messages.OrderByDescending(x => x.Id).Take(20).ToListAsync();
                await writer.WriteLineAsync(JsonSerializer.Serialize(history.OrderBy(x => x.Id).Select(x => $"{x.Author}: {x.Text}")));
            }
            else if (command.Action == "send" && Valid(command.Text, 500))
            {
                db.Messages.Add(new Message { Author = name, Text = command.Text!, CreatedAt = DateTime.UtcNow });
                await db.SaveChangesAsync();
                await File.AppendAllTextAsync("chat.log", $"{DateTime.UtcNow:O} message-saved author={name}\n");
                await writer.WriteLineAsync("OK");
            }
            else if (admin && Valid(command.Text, 50))
            {
                string target = command.Text!.ToLowerInvariant();
                var existing = await db.Clients.FindAsync(target);
                if (command.Action == "remove-client" && existing is not null) db.Remove(existing);
                else if ((command.Action is "add-client" or "add-admin") && Valid(command.Password, 120)
                    && command.Password!.Length >= 8 && existing is null && await db.Admins.FindAsync(target) is null)
                {
                    string hash = Passwords.Hash(command.Password);
                    if (command.Action == "add-admin") db.Admins.Add(new Admin { Name = target, Hash = hash });
                    else db.Clients.Add(new Client { Name = target, Hash = hash });
                }
                else { await writer.WriteLineAsync("Операцію відхилено"); continue; }
                await db.SaveChangesAsync();
                await writer.WriteLineAsync("OK");
            }
            else await writer.WriteLineAsync("Операцію відхилено");
        }
    }
}

static bool Valid(string? value, int max) =>
    !string.IsNullOrWhiteSpace(value) && value.Length <= max && !value.Any(char.IsControl);

record Command(string Action, string? Text = null, string? Password = null);
sealed class Admin { public string Name { get; set; } = ""; public string Hash { get; set; } = ""; }
sealed class Client { public string Name { get; set; } = ""; public string Hash { get; set; } = ""; }
sealed class Message
{
    public int Id { get; set; }
    public string Author { get; set; } = "";
    public string Text { get; set; } = "";
    public DateTime CreatedAt { get; set; }
}
sealed class ChatDb : DbContext
{
    public DbSet<Admin> Admins => Set<Admin>();
    public DbSet<Client> Clients => Set<Client>();
    public DbSet<Message> Messages => Set<Message>();
    protected override void OnConfiguring(DbContextOptionsBuilder options) => options.UseSqlite("Data Source=chat.db");
    protected override void OnModelCreating(ModelBuilder model)
    {
        model.Entity<Admin>().HasKey(x => x.Name);
        model.Entity<Client>().HasKey(x => x.Name);
    }
}
