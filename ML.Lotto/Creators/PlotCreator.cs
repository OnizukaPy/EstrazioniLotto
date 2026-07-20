// classe per generare un grafico passando l'oggetto Number
using ML.Lotto.Models;
using ScottPlot;

namespace ML.Lotto.Creators;

public class PlotCreator
{
    Plot _plt { get; set; } = null!;
    int _width { get; set; } = 2560;
    int _height { get; set; } = 1440;
    string _filepath { get; set; } = "plot.jpg";

    // costruttore
    public PlotCreator()
    {
        _plt = new Plot();
    }

    // metodo di set delle dimensioni
    public PlotCreator SetDimensions(int width, int height)
    {
        _width = width;
        _height = height;
        return this;
    }

    // metodo per importare le grandezze dei numeri e generare il grafico
    public PlotCreator CreateScatterPlot(List<int> x, List<int> y, string title, string xLabel, string yLabel)
    {
        double[] xValues = x.Select(n => (double)n).ToArray();
        double[] yValues = y.Select(n => (double)n).ToArray();

        // creiamo il grafico a dispersione
        _plt.Clear();
        _plt.Add.Scatter(xValues, yValues);
        _plt.Title(title);
        _plt.XLabel(xLabel);
        _plt.YLabel(yLabel);
        return this;
    }

    // creiamo invece un grafico a candelstick prendendo le estrazioni e le scompensazioni a gruppi di 5 estrazioni
    public PlotCreator CreateCandlestickPlot(List<int> x, List<int> y, string title, string xLabel, string yLabel)
    {
        double[] xValues = x.Select(n => (double)n).ToArray();
        double[] yValues = y.Select(n => (double)n).ToArray();

        OHLC[] ohlc = new OHLC[xValues.Length / 5];

        for (int i = 0; i < ohlc.Length; i++)
        {
            int startIndex = i * 5;
            int endIndex = Math.Min(startIndex + 5, xValues.Length);

            double open = yValues[startIndex];
            double close = yValues[endIndex - 1];
            double high = yValues.Skip(startIndex).Take(endIndex - startIndex).Max();
            double low = yValues.Skip(startIndex).Take(endIndex - startIndex).Min();

            ohlc[i] = new OHLC(open, high, low, close, DateTime.Now.AddDays(i), TimeSpan.FromDays(1));
        }

        // aggiungiamo i valori di x come etichette sull'asse x
        // creiamo il grafico a candelstick
        _plt.Clear();
        _plt.Add.OHLC(ohlc.ToList());
        _plt.Title(title);
        _plt.XLabel(xLabel);
        _plt.YLabel(yLabel);
        return this;
    }

    // metodo per creare un grafico a barre prendendo le grandezze dei numeri e generare il grafico
    public PlotCreator CreateBarPlot(Dictionary<int, Number> numbers, string title, string xLabel, string yLabel)
    {
        // creiamo le barre prendendo i numeri e il numero di uscite

        var ordinati = numbers.Values
            .OrderByDescending(n => n.NumeroUscite)
            .ToList();

        var media = ordinati.Average(n => n.NumeroUscite);

        var bars = ordinati
            .Select((n, i) =>
            {
                Color color;
                if (n.NumeroUscite > media + 5)
                    color = Colors.ForestGreen;
                else if (n.NumeroUscite < media - 5)
                    color = Colors.IndianRed;
                else
                    color = Colors.Gold;

                return new Bar
                {
                    Position = i,
                    Value = n.NumeroUscite,
                    FillColor = color
                };
            })
            .ToList();

        _plt.Add.Bars(bars);

        double[] positions = ordinati
            .Select((_, i) => (double)i)
            .ToArray();

        string[] labels = ordinati
            .Select(n => n.Value.ToString())
            .ToArray();

        _plt.Axes.Bottom.TickGenerator =
            new ScottPlot.TickGenerators.NumericManual(positions, labels);


        // creiamo il grafico a barre
        // _plt.Clear();
        // _plt.Add.Bars(bars);
        _plt.Title(title);
        _plt.XLabel(xLabel);
        _plt.YLabel(yLabel);
        return this;
    }

    // metodo per salvare
    public PlotCreator SavePlot(string? filePath = null)
    {
        // se il percorso del file non è valido, lanciamo un'eccezione
        if (!string.IsNullOrEmpty(filePath))
        {
            if (!filePath.EndsWith(".jpg") && !filePath.EndsWith(".png"))
            {
                throw new ArgumentException("Il percorso del file deve terminare con .jpg o .png.", nameof(filePath));
            }
            _filepath = filePath;
        }

        _plt.SaveJpeg(_filepath, _width, _height);
        return this;
    }

    // metodo per aprirlo direttamente una volta generato
    public PlotCreator ShowPlot()
    {
        using (var process = new System.Diagnostics.Process())
        {
            process.StartInfo.FileName = _filepath;
            process.StartInfo.UseShellExecute = true;
            process.Start();
        }
        return this;
    }
}