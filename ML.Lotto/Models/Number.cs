using ML.Lotto.Creators;
using ML.Lotto.Attributes;

namespace ML.Lotto.Models;

public class Number
{
    [PropertyName("N")]
    [Dim(3)]
    [Order(1)]
    public int Value { get; set; }

    // lista delle estrazioni in cui è uscito il numero
    public List<int> Estrazioni { get; set; } = new List<int>();

    [PropertyName("NU")]
    [Dim(5)]
    [Order(3)]
    public int NumeroUscite => Estrazioni.Count;
    public int DeltaUscite { get; set; } = 0;

    [PropertyName("Ultima estrazione")]
    [Dim(20)]
    [Order(2)]
    public int NumeroUltimaEstrazione => Estrazioni.OrderBy(e => e).Last();

    [PropertyName("FA")]
    [Dim(5)]
    [Order(4)]
    public int FrequenzaAttuale { get; set; } = 0;

    [PropertyName("IF")]
    [Dim(5)]
    [Order(9)]
    public bool IsFrequent => FrequenzaAttuale <= DatasetCreator.FREQUENCY;

    // lista dei ritardi del numero, calcolata a partire dalla lista delle estrazioni
    public List<int> Ritardi => Estrazioni.OrderBy(e => e)
                                          .Select((e, i) => i == 0 ? 0 : e - Estrazioni.OrderBy(e => e).ElementAt(i - 1))
                                          .ToList();

    [PropertyName("RUU")]
    [Dim(5)]
    [Order(6)]
    public int RitardoUltimaUscita => Ritardi.Last();

    // il ritardo attuale è estrazione massima - ultima estrazione in cui è uscito il numero
    [PropertyName("RA")]
    [Dim(5)]
    [Order(5)]
    public int RitardoAttuale { get; set; } = 0;

    [PropertyName("RM")]
    [Dim(5)]
    [Order(7)]
    public int RitardoMassimo => Ritardi.Max();

    // scompensazione
    public List<int> Scompensazioni { get; set; } = new List<int>();

    [PropertyName("S")]
    [Dim(5)]
    [Order(8)]
    public int Scompensazione => Scompensazioni.Sum();

    // head della tabella di stampa
    public static string Header = GetHeader();

    static string GetHeader()
    {
        // prendiamo l'oggetto stesso, prendiamo solo le proprietà che hanno l'attributo PropertyName, 
        // e le ordiniamo per l'ordine di stampa prendendo l'attriubuto Dim per fare il padding della stampa
        var properties = typeof(Number).GetProperties()
            .Where(p => p.GetCustomAttributes(typeof(PropertyNameAttribute), false).Length > 0)
            .Select(p => new
            {
                Property = p,
                // prendiamo l'attributo PropertyNameAttribute della proprietà, l'ordine e la dimensione per il padding della stampa
                Attribute = (PropertyNameAttribute)p.GetCustomAttributes(typeof(PropertyNameAttribute), false).First(),
                Dim = ((DimAttribute)p.GetCustomAttributes(typeof(DimAttribute), false).First()).Dim,
                Order = ((OrderAttribute)p.GetCustomAttributes(typeof(OrderAttribute), false).First()).Order
            })
            .OrderBy(p => p.Order)
            .ToList();
        // restiutuiamo la stringa di header con il padding della stampa a sinistra usando il padding costum
        return string.Join(" ", properties.Select(p => $"{p.Attribute.Name.PadLeft(p.Dim)}"));
    }

    // metodo di calcolo del ritardo attuale, dato l'id dell'ultima estrazione
    public void CalcolaRitardoAttuale(int idUltimaEstrazione)
    {
        RitardoAttuale = idUltimaEstrazione - NumeroUltimaEstrazione;
    }

    // metodo per calcolare la frequenza attuale del numero, dato il numero di estrazioni totali
    public void CalcolaFrequenzaAttuale(int numeroEstrazioniTotali)
    {
        FrequenzaAttuale = (int)Math.Round((double)numeroEstrazioniTotali / NumeroUscite);
    }

    // metodo per il calcolo della differenza tra le uscite totali e il numero di uscite medio dato il numero totale delle estrazioni
    public void CalcolaDeltaUscite(int numeroEstrazioniTotali)
    {
        int usciteMedie = (int)Math.Round((double)numeroEstrazioniTotali / DatasetCreator.FREQUENCY);
        DeltaUscite = NumeroUscite - usciteMedie;
    }

    // metodo per stampare l'oggetto Number in formato tabellare
    public override string ToString()
    {
        // prendiamo l'oggetto stesso, prendiamo solo i valori delle proprietà che hanno l'attributo PropertyName,
        // e le ordiniamo per l'ordine di stampa prendendo l'attriubuto Dim per fare il padding della stampa
        var properties = typeof(Number).GetProperties()
            .Where(p => p.GetCustomAttributes(typeof(PropertyNameAttribute), false).Length > 0)
            .Select(p => new
            {
                Property = p,
                // prendiamo l'attributo PropertyNameAttribute della proprietà, l'ordine e la dimensione per il padding della stampa
                Attribute = (PropertyNameAttribute)p.GetCustomAttributes(typeof(PropertyNameAttribute), false).First(),
                Dim = ((DimAttribute)p.GetCustomAttributes(typeof(DimAttribute), false).First()).Dim,
                Order = ((OrderAttribute)p.GetCustomAttributes(typeof(OrderAttribute), false).First()).Order
            })
            .OrderBy(p => p.Order)
            .ToList();
        return string.Join(" ", properties.Select(p => $"{p?.Property?.GetValue(this)?.ToString()?.PadLeft(p.Dim)}"));
    }


}