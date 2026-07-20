using Microsoft.ML.Data;

namespace ML.Lotto.Models;

public class Estrazione
{
    [LoadColumn(0)]
    public DateTime Data { get; set; }
    [LoadColumn(1)]
    public string Ruota { get; set; } = null!;
    [LoadColumn(2)]
    public int N1 { get; set; }
    [LoadColumn(3)]
    public int N2 { get; set; }
    [LoadColumn(4)]
    public int N3 { get; set; }
    [LoadColumn(5)]
    public int N4 { get; set; }
    [LoadColumn(6)]
    public int N5 { get; set; }
}