using System;

namespace LottoSharp.Models;

public class Numero
{
    public int Value { get; set; }
    public int Occorrency { get; set; }
    public double Frequency { get; set; }
    public List<int> Ritardi { get; set; } = new();
    public List<int> EstrazioniPerCiclo { get; set; } = new();
    public List<int> EstrazioniPer10Cicli { get; set; } = new();
    public List<int> EstrazioniPer50Cicli { get; set; } = new();

    public int RitardoMax { get; set; }
    public int RitardoAttuale { get; set; }

    // lista di estrazioni in cui è uscito il numero
    public List<int> EstrattoIn { get; set; } = new();

    public Numero(int value)
    {
        Value = value;
        Occorrency = 0;
        Frequency = 0;
        // inizializiamo le uscite con 0
        EstrattoIn.Add(0);
    }
}
