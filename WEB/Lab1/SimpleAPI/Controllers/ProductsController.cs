using Microsoft.AspNetCore.Mvc;
using SimpleAPI.Services;

namespace SimpleAPI.Controllers;


[ApiController]
[Route("products")]
public class ProductsController : ControllerBase
{
    private readonly IProductService _productService;  


    public ProductsController(IProductService productService)
    {
        _productService = productService;
    }

    [HttpGet("{productId}")]  

    public IActionResult GetProduct(int productId)
    {
        try
        {
            var productName = _productService.GetProductName(productId);
            var product = new
            {
                id = productId.ToString(),
                name = productName
            };

            return Ok(product);
        }
        catch (FileNotFoundException)
        {
            return NotFound("Product data file not found.");
        }
        catch (ArgumentOutOfRangeException)
        {
            return NotFound($"Product with ID {productId} not found.");
        }
    }
}