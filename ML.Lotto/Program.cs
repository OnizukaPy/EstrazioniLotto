// carichiamo le librerie necessarie per la Dependency Injection
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using ML.Lotto.Creators;
using ML.Lotto.Models;

// creiamo un host per la Dependency Injection
var host = Host.CreateDefaultBuilder(args)
    .ConfigureServices((context, services) =>
    {
        // aggiungiamo il servizio DatasetCreator come singleton come Transient
        services.AddSingleton<DatasetCreator>();
        services.AddTransient<PlotCreator>();
        // registriamo i servizi necessari per l'applicazione
        services.AddSingleton<Application>();
    })
    .Build();

// creiamo una istanza dell'applicazione
var app = host.Services.GetRequiredService<Application>();

// avviamo l'init dell'applicazione
app.Init("BA.csv");

// eseguiamo il run dell'applicazione
//app.Run(25);