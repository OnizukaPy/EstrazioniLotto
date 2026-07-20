using Microsoft.ML;
using ML.Lotto.Creators;
using ML.Lotto.Models;

public class Application
{
    DatasetCreator _datasetCreator { get; set; }
    PlotCreator _plotCreator { get; set; }

    // costruttore 
    public Application(DatasetCreator datasetCreator, PlotCreator plotCreator)
    {
        _datasetCreator = datasetCreator;
        _plotCreator = plotCreator;
    }

    // creiamo un metodo Init per inizializzare l'applicazione
    public void Init(string path)
    {
        // carichiamo il dataset dal file CSV
        Console.WriteLine();
        _datasetCreator.Load(path);

        // stampiamo le prime 10 estrazioni del dataset
        Console.WriteLine();
        _datasetCreator.PrintFirstN(10);

        // lanciamo l'analisi del dataset
        Console.WriteLine();
        _datasetCreator.Analyze();
        _datasetCreator.PrintNumbers();

        // stampiamo un grafico a barre prendendo tutti i numeri e ordinandoli in ordine decrescente di numero di uscite
        Console.WriteLine();
        _plotCreator.CreateBarPlot(
            numbers: _datasetCreator.Numbers,
            title: "Numero di uscite dei numeri",
            xLabel: "Numero",
            yLabel: "Numero di uscite");
        _plotCreator.SavePlot("plot_uscite.jpg");
        _plotCreator.ShowPlot();

    }

    // creiamo un metodo Run per eseguire l'applicazione
    public void Run(int number, string? plotFilePath = null)
    {
        // recuperiamo il numero dal dizionario dei numeri
        if (!_datasetCreator.Numbers.ContainsKey(number))
        {
            throw new ArgumentException($"Il numero {number} non esiste nel dataset.", nameof(number));
        }
        var n = _datasetCreator.Numbers[number];

        // generiamo il grafico del numero
        _plotCreator.CreateScatterPlot(
        //_plotCreator.CreateCandlestickPlot(
        // prendiamo le ultime 10 uscite del numero e le relative scompensazioni
            x: n.Estrazioni.TakeLast(10).ToList(),
            y: n.Scompensazioni.TakeLast(10).ToList(),
            title: $"Numero {n.Value}",
            xLabel: "Estrazione",
            yLabel: "scompensazione");

        if (plotFilePath != null)
            _plotCreator.SavePlot(plotFilePath);
        else
            _plotCreator.SavePlot();
        _plotCreator.ShowPlot();
    }
}