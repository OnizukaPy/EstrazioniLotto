
namespace LottoSharp;

class Constants
{
    public const string ARCHIVIO_FILE = "estrazioni";
    public static readonly List<string> RUOTE = new List<string> { "BA", "CA", "FI", "GE", "MI", "NA", "PA", "RM", "TO", "VE", "RN" };
    public const int ESTRAZIONI_PER_CICLO = 18; // 90/5 = 18 cicli per coprire tutte le combinazioni di 5 numeri su 90
}