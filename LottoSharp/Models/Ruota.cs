using System;
using Text.CSV.Models;

namespace LottoSharp.Models;

public class Ruota
{
    public string Name { get; set; }
    public string Path { get; set; }
    public CSVFile Archivio { get; set; }
    public Csv Data { get; set; }
    public List<Estrazione> Estrazioni { get; set; }
    public List<Numero> Numeri { get; set; }

    public Ruota(string name, string path)
    {
        Name = name;
        Path = path;
        Archivio = new CSVFile(Path);
        Data = new();
        Estrazioni = new();
        Numeri = new();
        for (int i = 1; i <= 90; i++)
        {
            Numeri.Add(new Numero(i));
        }
    }
}
