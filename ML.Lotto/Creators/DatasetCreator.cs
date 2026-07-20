using Microsoft.ML;
using ML.Lotto.Models;

namespace ML.Lotto.Creators;

public class DatasetCreator
{

    // costanti
    public const int FREQUENCY = 90/5;

    // proprietà di IDataView per contenere i dati del dataset
    public IDataView? Data { get; private set; }
    public List<Estrazione> Estrazioni { get; set; } = new List<Estrazione>();
    public List<EstrazionePlus> Dataset { get; set; } = new List<EstrazionePlus>();

    // id ultima estrzione
    public int IdUltimaEstrazione => Dataset.OrderBy(e => e.Id).Last().Id;

    // dizionario dei numeri
    public Dictionary<int, Number> Numbers { get; set; } = new Dictionary<int, Number>();

    // dizionario dei numeri spia
    public Dictionary<int, List<Spia>> NumbersSpia { get; set; } = new Dictionary<int, List<Spia>>();

    // costruttore della classe Dataset
    public DatasetCreator()
    {
        // inizializziamo la proprietà Data a null
        Data = null;
    }

    public void Load(string path)
    {
        // verifichiamo se il percorso del file è valido
        if (string.IsNullOrEmpty(path))
        {
            throw new ArgumentException("Il percorso del file non può essere nullo o vuoto.", nameof(path));
        }

        // verichiamo se il file esiste
        if (!File.Exists(path))
        {
            throw new FileNotFoundException($"Il file {path} non esiste.");
        }

        // creiamo un'istanza di MLContext
        var mlContext = new MLContext();

        // carichiamo i dati dal file CSV
        Data = mlContext.Data.LoadFromTextFile<Estrazione>(path, hasHeader: true, separatorChar: ',');
        
        // convertiamo l'oggetto IDataView in IEnumerable<Estrazione> per poterlo enumerare
        Estrazioni = mlContext.Data.CreateEnumerable<Estrazione>(Data, reuseRowObject: false).ToList();    

        // creiamo una lista di EstrazionePlus a partire dalla lista di Estrazione
        Dataset = Estrazioni.Select(e => new EstrazionePlus
        {
            Data = e.Data,
            Ruota = e.Ruota,
            N1 = e.N1,
            N2 = e.N2,
            N3 = e.N3,
            N4 = e.N4,
            N5 = e.N5
        }).ToList();

        // verifichiamo se i dati sono stati caricati correttamente
        if (Estrazioni == null || Estrazioni.Count == 0)
        {
            throw new InvalidOperationException("Errore durante il caricamento dei dati, o file vuoto.");
        }

        // stampiamo il numero di righe caricate
        var rowCount = Estrazioni.Count;
        if (rowCount != 0)
        {
            Console.WriteLine($"Caricate '{rowCount}' righe dal file '{path}'.");
        }
        else
        {
            Console.WriteLine($"Il file '{path}' è vuoto.");
        }
    }

    public void PrintFirstN(int n, int startIndex = 0, int endIndex = -1)
    {
        // verifichiamo se il numero di righe da stampare è valido
        if (n <= 0)
        {
            throw new ArgumentException("Il numero di righe da stampare deve essere maggiore di zero.", nameof(n));
        }

        // verifichiamo se ci sono dati da stampare
        if (Dataset == null || Dataset.Count == 0)
        {
            Console.WriteLine("Nessun dato disponibile per la stampa.");
            return;
        }

        // stampiamo le prime n righe del dataset
        Console.WriteLine($"Prime {n} estrazioni del dataset:");
        Console.WriteLine($"{"Id",-5} {"Data",-12} {"Ruota",-10} {"N1",-5} {"N2",-5} {"N3",-5} {"N4",-5} {"N5",-5}");
        Dataset
            .Skip(startIndex)
            .Take(endIndex == -1 ? n : endIndex - startIndex + 1)
            .ToList()
            .ForEach(e => Console.WriteLine($"{e.Id,-5} {e.Data.ToShortDateString(),-12} {e.Ruota,-10} {e.N1,-5} {e.N2,-5} {e.N3,-5} {e.N4,-5} {e.N5,-5}"));
    }

    // metodo per eseguire l'analsi dei dati
    public void Analyze()
    {
        // verifichiamo se ci sono dati da analizzare
        if (Dataset == null || Dataset.Count == 0)
        {
            Console.WriteLine("Nessun dato disponibile per l'analisi.");
            return;
        }

        // analizziamo le estrazioni e popoliamo il dizionario dei numeri
        foreach (var estrazione in Dataset)
        {
            foreach (var numero in new[] { estrazione.N1, estrazione.N2, estrazione.N3, estrazione.N4, estrazione.N5 })
            {
                if (!Numbers.ContainsKey(numero))
                {
                    Numbers[numero] = new Number { Value = numero };
                }

                // aggiungiamo l'id dell'estrazione corrente alla lista delle estrazioni del numero
                Numbers[numero].Estrazioni.Add(estrazione.Id);

                // calcoliamo il ritardo attuale del numero
                Numbers[numero].CalcolaRitardoAttuale(IdUltimaEstrazione);

                // calcoliamo la frequenza attuale del numero
                Numbers[numero].CalcolaFrequenzaAttuale(Dataset.Count);

                // calcoliamo il deta delle uscite del numero
                Numbers[numero].CalcolaDeltaUscite(Dataset.Count);

                // aggiungiamo la scompensazione del numero all'estrazione in corso
                var scompensazione = FREQUENCY - Numbers[numero].RitardoUltimaUscita;
                Numbers[numero].Scompensazioni.Add(scompensazione);
            }
        }

        // stampiamo i risultati dell'analisi
        Console.WriteLine($"Analisi completata. Trovati '{Numbers.Count}' numeri unici.");
    }

    // metodo di determinazione dei numeri spia per ogni numero, data dall'analisi del dataset
    public void AnalyzeSpia(int numeroEstrazioni)
    {
        // inizializiamo il dizionario dei numeri spia
        NumbersSpia.Clear();
        // creiamo 90 liste vuote per i numeri spia
        for (int i = 1; i <= 90; i++)
        {
            NumbersSpia[i] = new List<Spia>();
        }

        // analizziamo le estrazioni e popoliamo il dizionario dei numeri spia
        for (var i = 0; i < Dataset.Count - numeroEstrazioni; i++)
        {
            var estrazione = Dataset[i];
            foreach (var numero in new[] { estrazione.N1, estrazione.N2, estrazione.N3, estrazione.N4, estrazione.N5 })
            {
                // prendiamo le 10 estrazioni successive a quella corrente
                var estrazioniSuccessive = Dataset.Skip(i + 1).Take(numeroEstrazioni).ToList();

                // estraiamo i numeri univoci e contiamo le occorrenze 
                var numeriSuccessivi = estrazioniSuccessive
                    .SelectMany(e => new[] { e.N1, e.N2, e.N3, e.N4, e.N5 })
                    .GroupBy(n => n)
                    .ToDictionary(g => g.Key, g => g.Count());
                
                // aggiungiamo i numeri spia al dizionario
                foreach (var kvp in numeriSuccessivi)
                {
                    // se il numero è già presente nella lista dei numeri spia, aggiorniamo l'occorrenza
                    var spia = NumbersSpia[numero].FirstOrDefault(s => s.Numero == kvp.Key);
                    if (spia != null)
                    {
                        spia.Occorrenza += kvp.Value;
                    }
                    else
                    {
                        // altrimenti aggiungiamo un nuovo numero spia
                        NumbersSpia[numero].Add(new Spia { Numero = kvp.Key, Occorrenza = kvp.Value });
                    }
                }
            }
        }
    }

    // metodo per stampare tutti i numeri con le loro informazioni
    public void PrintNumbers()
    {
        // verifichiamo se ci sono numeri da stampare
        if (Numbers == null || Numbers.Count == 0)
        {
            Console.WriteLine("Nessun numero disponibile per la stampa.");
            return;
        }

        // stampiamo tutti i numeri con le loro informazioni
        Console.WriteLine($"{Number.Header}");
        Numbers.Values
            .OrderBy(n => n.Value)
            .ToList()
            .ForEach(n => Console.WriteLine(n.ToString()));
    }
}