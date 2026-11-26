using System.Security.Cryptography;

internal static class Passwords
{
    const int Iterations = 310000;

    public static string Hash(string password)
    {
        if (password.Length < 8) throw new ArgumentException("Пароль має містити щонайменше 8 символів.");
        var salt = RandomNumberGenerator.GetBytes(16);
        return $"{Convert.ToBase64String(salt)}:{Convert.ToBase64String(Derive(password, salt))}";
    }

    public static bool Verify(string password, string stored)
    {
        var parts = stored.Split(':');
        if (parts.Length != 2) return false;
        byte[] salt = Convert.FromBase64String(parts[0]);
        return CryptographicOperations.FixedTimeEquals(Derive(password, salt), Convert.FromBase64String(parts[1]));
    }

    private static byte[] Derive(string password, byte[] salt) =>
        Rfc2898DeriveBytes.Pbkdf2(password, salt, Iterations, HashAlgorithmName.SHA256, 32);
}
