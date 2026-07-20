namespace ML.Lotto.Models;

public class EstrazionePlus : Estrazione
{
    public static int Count { get; set; } = 0;
    public int Id { get; set; } = ++Count;

    public List<Number> Numbers { get; set; } = new List<Number>();

    // costruttore della classe EstrazionePlus
    public EstrazionePlus()
    {
        Numbers.Add(new Number { Value = N1 });
        Numbers.Add(new Number { Value = N2 });
        Numbers.Add(new Number { Value = N3 });
        Numbers.Add(new Number { Value = N4 });
        Numbers.Add(new Number { Value = N5 });
    }
}