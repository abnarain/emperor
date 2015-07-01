function [signal1 fs1] = plot_fft (filename,varargin)
% returns the signal values and the sampling frequency
% Input : file name containing time, signal in csv format
% Optional input: flag=1 generates double sided FFT image
%                 filename= prints out a pdf file with the FFT in it
r1= csvread(filename);
signal1=r1(:,2);
time1=r1(:,1);
fs1=1/(time1(2)-time1(1))
%fs1=fs1/2;
N=length(time1)
bin_vals = [0 : N-1];
N_2 = ceil(N/2);
length(varargin)
if length(varargin)==1
    flag =varargin{1}
elseif length(varargin)==2
    flag = varargin{1}
    printfilename = varargin{2}
else
    flag=1  
end
if flag==1
X_mags = abs(fft(signal1));
fax_Hz = bin_vals*fs1/N;
%plot(fax_Hz(1:N_2), 10*log10(X_mags(1:N_2)))
%plot(fax_Hz(2000:3000), 10*log10(X_mags(2000:3000)))
plot(fax_Hz(500:2000), 10*log10(X_mags(500:2000)))
title('Single-sided Magnitude spectrum (Hertz)');
else
X_mags = abs(fftshift(fft(signal1)));
fax_Hz = (bin_vals-N_2)*fs1/N;
plot(fax_Hz, 10*log10(X_mags))
title('Double-sided Magnitude spectrum (Hertz)');
end
xlabel('Frequency (Hz)')
ylabel('Magnitude |Y(f)| dB');
axis tight

if length(varargin)==2
set(gcf, 'Units', 'inches'); % set units
PaperWidth = 6; % paper width
PaperHeight = PaperWidth*(sqrt(5)-1)/2; % paper height
set(gcf, 'PaperSize', [PaperWidth PaperHeight]); % set paper size
afFigurePosition = [1 1 PaperWidth PaperHeight]; % set figure on screen [pos_x pos_y width_x width_y]
set(gcf, 'Position', afFigurePosition); % set figure position on paper [left bottom width height]
set(gcf, 'PaperPositionMode', 'auto'); %
set(gca, 'Units','normalized','Position',[0.1 0.15 0.85 0.8]); % fit axes within figure
f = sprintf('/tmp/%s',printfilename);
saveas(gcf, f, 'pdf')
end
