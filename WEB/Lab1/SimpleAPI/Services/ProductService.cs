namespace SimpleAPI.Services;

public class ProductService : IProductService
{
    private const string ProductFilePath = "data/products.txt";

    public string GetProductName(int productId)
    {
        if (!File.Exists(ProductFilePath))
        {
            throw new FileNotFoundException($"Product file '{ProductFilePath}' not found.");
        }

        var lines = File.ReadAllLines(ProductFilePath);

        if (productId <= 0 || productId > lines.Length)
        {
            throw new ArgumentOutOfRangeException(nameof(productId), $"Product with ID {productId} not found.");
        }

        return lines[productId - 1];
    }
}

public interface IProductService
{
    string GetProductName(int productId);
}