// installiamo le dipendenze per la dependency injection
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using LottoSharp;

// creiamo un host per gestire le dipendenze e il ciclo di vita dell'applicazione
var host = Host.CreateDefaultBuilder(args)
    .ConfigureServices((_, services) =>
        services.AddSingleton<Application>())
    .Build();

// risolviamo l'istanza dell'applicazione e avviamo il programma
var app = host.Services.GetRequiredService<Application>();

// inizializziamo l'applicazione
app.Init();

// eseguiamo l'applicazione
app.Run();