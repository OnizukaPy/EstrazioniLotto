using System;
using Text.CSV.Models.Base;

namespace LottoSharp.Models;

public class Estrazione
{
    public string Ruota { get; set; }
    public DateTime Data { get; set; }
    public List<int> Numeri { get; set; }

    public Estrazione(DateTime data, string ruota, List<int> numeri)
    {
        Data = data;
        Ruota = ruota;
        Numeri = numeri;
    }

    public static Estrazione FromRow(Row row)
    {
        var values = row.GetValues();
        var data = DateTime.Parse(values[0]);
        var ruota = values[1];
        var numeri = values.Skip(2).Take(5).Select(int.Parse).ToList();
        return new Estrazione(data, ruota, numeri);
    }

}
