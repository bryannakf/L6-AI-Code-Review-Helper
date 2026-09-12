from services.csharp_service import analyse_csharp

code = """
using System;

class Program
{
    static void Main()
    {
        Console.WriteLine("Hello");
    
}
"""

result = analyse_csharp(code)

print(result)