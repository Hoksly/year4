using Microsoft.AspNetCore.Mvc;

namespace SimpleAPI.Controllers;

[ApiController]
[Route("products")]
public class ProductsController : ControllerBase
{
    [HttpGet("{productId}")]
    public IActionResult GetProduct(int productId)
    {
        var product = new 
        {
            id = productId.ToString(),
            name = $"{productId} name"
        };

        return Ok(product);
    }
}