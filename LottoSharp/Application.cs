

using System.Data;
using System.Reflection.Metadata;
using System.Threading.Tasks.Dataflow;
using ConsolePB.Models;

namespace LottoSharp;

public class Application 
{

    // proprietà
    private string WORKING_DIRECTORY = string.Empty;
    private List<Ruota> Ruote { get; set; } = new();

    public Application() { }     
    
    public void Init()
    {
        Console.WriteLine("Inizializzazione dell'applicazione...");
        SetWorkingDirectory();
        Console.WriteLine($"Directory di lavoro: {WORKING_DIRECTORY}");

        // leggiamo tutti i file presenti nella directory di lavoro
        var files = Directory.GetFiles(Path.Combine(WORKING_DIRECTORY, Constants.ARCHIVIO_FILE))
            .Select(f => Path.GetFileName(f))
            // filtriamo solo i .csv
            .Where(f => f.EndsWith(".csv"))
            // filtriamo con quelli corrispondenti ai nomi delle ruote
            .Where(f => Constants.RUOTE.Any(r => f.StartsWith(r)))
            // ricaviamo il path completo dei file
            .Select(f => Path.Combine(WORKING_DIRECTORY, Constants.ARCHIVIO_FILE, f))
            .ToList();

        Console.WriteLine("File trovati:");
        files.ForEach(f => 
        {
            Console.WriteLine(f);
            Ruote.Add(new Ruota(Path.GetFileNameWithoutExtension(f), f));
        });

        // carichiamo le estrazioni per ogni ruota
        Ruote.ForEach(r => 
        {
            Console.WriteLine($"Caricamento estrazioni per la ruota {r.Name}...");
            // carichiamo il file CSV
            r.Archivio.Load();
            // convertiamo i dati in estrazioni
            r.Data = r.Archivio.ToCsv();
            r.Estrazioni = r.Data.GetRows().Select(row => Estrazione.FromRow(row)).ToList();

            // elaboriamo le statistiche per ogni numero
            r.Estrazioni.ForEach(e => 
            {
                // per ogni numero estratto, aggiorniamo le statistiche di uscita 
                e.Numeri.ForEach(n => 
                {
                    var numero = r.Numeri.First(num => num.Value == n);
                    numero.Occorrency++;
                    numero.EstrattoIn.Add(r.Estrazioni.IndexOf(e));
                });

                // aggiorniamo la frequenza per ogni numero
                r.Numeri.ForEach(num => 
                {
                    num.Frequency = (double)num.Occorrency / r.Estrazioni.Count;
                });

                // aggiorniamo i ritardi per ogni numero non estratto
                r.Numeri.ForEach(num =>
                {
                    // i ritardi sono tutte le differenze tra l'estrazione al momento t e t-1
                    for (int i = 1; i < num.EstrattoIn.Count; i++)
                    {
                        var ritardo = num.EstrattoIn[i] - num.EstrattoIn[i - 1];
                        num.Ritardi.Add(ritardo);
                    }

                    // calcoliamo il ritardo attuale come la differenza tra l'estrazione corrente e l'ultima estrazione in cui è uscito il numero
                    num.RitardoAttuale = r.Estrazioni.Count - num.EstrattoIn.Last() - 1;

                    // calcoliamo il ritardo massimo come il massimo dei ritardi
                    num.RitardoMax = num.Ritardi.Count > 0 ? num.Ritardi.Max() : num.RitardoAttuale;

                });

                // dividiamo le estrazioni in cicli di 18 estrazioni e calcoliamo per ogni numero quante volte è uscito nel ciclo
                for (int i = 0; i < r.Estrazioni.Count; i += Constants.ESTRAZIONI_PER_CICLO)
                {
                    var ciclo = r.Estrazioni.Skip(i).Take(Constants.ESTRAZIONI_PER_CICLO).ToList();
                    r.Numeri.ForEach(num =>
                    {
                        var count = ciclo.Count(e => e.Numeri.Contains(num.Value));
                        num.EstrazioniPerCiclo.Add(count);
                    });
                }

                // dividiamo le estrazioni in cicli di 10 cicli (180 estrazioni) e calcoliamo per ogni numero quante volte è uscito nel ciclo
                for (int i = 0; i < r.Estrazioni.Count; i += Constants.ESTRAZIONI_PER_CICLO * 10)
                {
                    var ciclo = r.Estrazioni.Skip(i).Take(Constants.ESTRAZIONI_PER_CICLO * 10).ToList();
                    r.Numeri.ForEach(num =>
                    {
                        var count = ciclo.Count(e => e.Numeri.Contains(num.Value));
                        num.EstrazioniPer10Cicli.Add(count);
                    });
                }

                // dividiamo le estrazioni in cicli di 50 cicli (900 estrazioni) e calcoliamo per ogni numero quante volte è uscito nel ciclo
                for (int i = 0; i < r.Estrazioni.Count; i += Constants.ESTRAZIONI_PER_CICLO * 50)
                {
                    var ciclo = r.Estrazioni.Skip(i).Take(Constants.ESTRAZIONI_PER_CICLO * 50).ToList();
                    r.Numeri.ForEach(num =>
                    {
                        var count = ciclo.Count(e => e.Numeri.Contains(num.Value));
                        num.EstrazioniPer50Cicli.Add(count);
                    });
                }

            });

             // calcoliamo la frequenza, il ritardo e il ritardo massimo per ogni numero
        });
        

        Console.WriteLine("Inizializzazione completata.");
        Ruote.ForEach(r => Console.WriteLine($"Ruota: {r.Name}, dimensioni: {string.Join(", ", r.Data.Size)}, estrazioni: {r.Estrazioni.Count}"));
        
    }

    private void SetWorkingDirectory()
    {
        Directory.SetCurrentDirectory("..");
        WORKING_DIRECTORY = Directory.GetCurrentDirectory();
    }

    public void Run()
    {
        Console.WriteLine("Esecuzione dell'applicazione...");
        // qui puoi inserire il codice principale del programma, ad esempio la logica di business, interazione con l'utente, ecc.
    }
}
