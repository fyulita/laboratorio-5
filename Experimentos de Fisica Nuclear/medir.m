%Para adquirir datos con NIDAQ si no funcionan daqhwinfo y analoginput
%Para saber cómo se llama la placa (Dev#):
devices = daq.getDevices;
%%
%Para saber más información de cada dispositivo:
%devices(#)

%Inicializa la comunicación y el canal
sesion = daq.createSession('ni');
%Inicializa la conexion (usar Dev# sacada de las lineas anteriores y el canal correspondiente)
addAnalogInputChannel(sesion,'Dev4', 'ai3', 'Voltage');

sesion.Rate = 100000; %Frecuencia de sampleo en Hz
sesion.DurationInSeconds = 120; %Duración de la medición en segundos
%No hacer una medición muy larga porque se cuelga
%Por ejemplo, empezar con 1 minuto e ir aumentando
sesion.Channels(1).InputType = 'SingleEnded';

[data, time] = sesion.startForeground;
%Acá se guardan todos los datos

disp('Ya termine de medir.');

%Definir umbral en volts (el valor por debajo del cual no se consideran picos)
umbral=1;

%Buscar los picos
[pks,locs] = findpeaks(data,'MINPEAKHEIGHT',umbral);

npks=length(pks); %cantidad de picos
cps=length(pks)/sesion.DurationInSeconds; %cuentas por segundo        

disp('Voy a hacer el primer grafico.')

figure(1);clf;
subplot(3,1,1);
hold on
plot(time,data) %los datos completos

if ~isempty(pks) %si hay picos, los grafica
    plot(time(locs),pks,'g.','markerfacecolor',[1 0 0]); 
    %en cada tiempo y a altura de cada pico plotea
    %en simbolito para marcar que hay un pico
end
%xlim([0 .005]) %limite elegido para ver que se detecta o no, y la forma de los picos
%ylim([-2 5])
%line(xlim,[umbral umbral],'color','r')
%el limite en y lo elijo a partir de un grafico sin fijar los limites
xlabel('Time [s]')
ylabel('Voltage [V]')
grid on

disp('Termine de hacer el primer grafico.');
disp('Voy a hacer el segundo grafico.')

%Para el histograma: conviene usar un multiplo de la minima
%resolucion de voltaje para el ancho de bines, para evitar
%cosas raras con aliasing, dobles lineas, etc.
resolucion_daq=min(diff(unique(data)));
X=0:100*resolucion_daq:10;             
h=hist(pks,X);%calculo el histograma        

subplot(3,1,2)
plot(X,h,'.') %un histograma acumulado de picos en escala lineal
%xlim([umbral 9])
xlim([1 10])
ylabel('Counts')
xlabel('Voltage [V]')  
grid on

disp('Termine de hacer el segundo grafico.');
disp('Voy a hacer el tercer grafico.')

subplot(3,1,3)
semilogy(X,h,'.') %lo mismo en escala logaritmica        
xlim(X([1 end]))
ylabel('Counts')
xlabel('Voltage [V]')  
grid on

disp('Termine de hacer el tercer grafico.');