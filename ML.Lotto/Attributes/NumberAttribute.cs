// creiamo un attributo che possa stabilire il nome della variabile da recuperare poi in un secondo momento
namespace ML.Lotto.Attributes;

[AttributeUsage(AttributeTargets.Property, Inherited = false, AllowMultiple = false)]
public class PropertyNameAttribute : Attribute
{
    public string Name { get; set; }

    public PropertyNameAttribute(string name)
    {
        Name = name;
    }
}

[AttributeUsage(AttributeTargets.Property, Inherited = false, AllowMultiple = false)]
public class DimAttribute : Attribute
{
    public int Dim { get; set; }

    public DimAttribute(int dim)
    {
        Dim = dim;
    }
}

[AttributeUsage(AttributeTargets.Property, Inherited = false, AllowMultiple = false)]
public class OrderAttribute : Attribute
{
    public int Order { get; set; }

    public OrderAttribute(int order)
    {
        Order = order;
    }
}