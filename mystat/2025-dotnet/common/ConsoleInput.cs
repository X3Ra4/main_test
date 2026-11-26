using System.Text;

internal static class ConsoleInput
{
    public static string Read(string prompt, int length = 120)
    {
        Console.Write(prompt + ": ");
        var value = Console.ReadLine()?.Trim() ?? throw new EndOfStreamException();
        return value.Length is > 0 && value.Length <= length ? value : throw new ArgumentException($"Вкажіть від 1 до {length} символів.");
    }

    public static int Number(string prompt, int min = 1, int max = int.MaxValue)
    {
        return int.TryParse(Read(prompt), out int number) && number >= min && number <= max
            ? number : throw new ArgumentException($"Вкажіть число від {min} до {max}.");
    }

    public static string Secret(string prompt)
    {
        if (Console.IsInputRedirected) return Read(prompt, 120);
        Console.Write(prompt + ": ");
        var text = new StringBuilder();
        while (true)
        {
            var key = Console.ReadKey(intercept: true);
            if (key.Key == ConsoleKey.Enter) break;
            if (key.Key == ConsoleKey.Backspace && text.Length > 0) text.Length--;
            else if (!char.IsControl(key.KeyChar) && text.Length < 120) text.Append(key.KeyChar);
        }
        Console.WriteLine();
        return text.ToString();
    }
}
