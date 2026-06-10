clear all;

fileName = 'cosine_irradiance_downward.txt';
runNo = 1;

data = readIrradiance(fileName);


spectrum    = data(runNo).irradiance(1,:);
wavelengths = data(runNo).wavelength;
depths      = data(runNo).depth;

test1 = textread('test1.txt','','headerlines',14);
mod = interp1(test1(:,1),test1(:,2), wavelengths);

absDiff = spectrum-mod;
relDiff = (spectrum./mod-1)*100;
areaDiff = (trapz(wavelengths,spectrum)/trapz(wavelengths,mod)-1)*100;

xl = [wavelengths(1)-2 wavelengths(end)+2];
subplot(2,2,1)
h = plot(wavelengths, spectrum, test1(:,1), test1(:,2),'linewidth',1);
legend(h,'AccuRT','disort',2)
grid on
xlabel('Wavelength [nm]')
ylabel('Irradiance [W m^{-2} nm^{-1}]')
set(gca,'xlim',xl,'xminortick','on','yminortick','on')
grid on

subplot(2,2,2)
plot(wavelengths, absDiff,'linewidth',1);
xlabel('Wavelength [nm]')
ylabel('Absolute difference [W m^{-2} nm^{-1}]')
set(gca,'xlim',xl,'xminortick','on','yminortick','on')
grid on

subplot(2,2,3)
plot(wavelengths, relDiff,'linewidth',1);
xlabel('Wavelength [nm]')
ylabel('Relative difference [%]')
set(gca,'xlim',xl,'xminortick','on','yminortick','on')
grid on

subplot(2,2,4)
uistr(1) = {'Downward surface irradiance'};
uistr(2) = {'Clear atmosphere'};
uistr(3) = {'Surfacace albedo: 0.0'};
uistr(4) = {'Solar zenith angle: 7.58 degrees'};
uistr(5) = {'Ozone column amount: 253 DU'};
uistr(6) = {'Solar spectrum scaling factor: 0.965'};
uistr(7) = {'Atmosphere bottom: 0.0 m'};
plot(0,0)
text(-1.0,0,uistr)
axis off

print -dpdf test1.pdf

disp('Test 1:')
disp(['Mean relative difference = ', num2str(mean(relDiff)), ' %'])
disp(['RMS relative difference = ', num2str(sqrt(mean(relDiff.^2))), ' %'])
disp(['Area difference = ', num2str(areaDiff), ' %'])

if (abs(mean(relDiff)) > 2)
  disp('Test 1 failed!')
end
