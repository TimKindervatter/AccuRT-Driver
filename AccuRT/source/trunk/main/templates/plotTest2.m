clear all;
warning off
% Begin user input
plotLogY = false;
% End user input

dataA = readRadiance('test2.txt');
dataB = readRadiance('radiance.txt');

wl  = dataA.wavelengths;
z   = dataA.depths;
phi = dataA.azimuthAngles;
for i=1:length(phi)
  for j=1:length(z)
    for k=1:length(wl)
      yA{i,j}(:,k)= squeeze(dataA.radiance(j,k,:,i));
      yB{i,j}(:,k)= squeeze(dataB.radiance(j,k,:,i));
    end
  end
end

delete(figure(1))
figure(1)
x = dataA.polarAngles;
n = 1;
for i=1:2
  for j=1:2
    subplot(2,2,n)
    hold on
    if plotLogY
      semilogy(x,yA{i,j},'--','linewidth',1)
      h=semilogy(x,yB{i,j},'-','linewidth',1)
    else
      plot(x,yA{i,j},'--','linewidth',1)
      h=plot(x,yB{i,j},'-','linewidth',1);
    end
    hold off
    set(gca,'xminortick','on','yminortick','on')
    set(gca,'xlim',[0 180])
    xlabel('Polar angles [degrees]')
    ylabel('Radiance [W m^{-2} nm^{-1} sr^{-1}]')
    title(['\phi = ',num2str(phi(i)),' deg, z = ',num2str(z(j)),' m'])
    set(gca,'xtick',[0 45 90 135 180])
    grid on
    if n==4
      hl=legend(h,num2str(wl'),4);
      set(get(hl,'title'),'string','Wavelength [nm]');
    end
    n=n+1;
  end
end
print -dpdf test2_1.pdf

delete(figure(2))
figure(2)
n = 1;
for i=1:2
  for j=1:2
    subplot(2,2,n)
    err = 2*(yB{i,j}-yA{i,j})./(yA{i,j}+yB{i,j})*100;
    plot(x,err,'-','linewidth',1)
    set(gca,'xminortick','on','yminortick','on')
    set(gca,'xlim',[0 180])
    set(gca,'xtick',[0 45 90 135 180])
    xlabel('Polar angles [degrees]')
    ylabel('Error [%]')
    title(['\phi = ',num2str(phi(i)),' deg, z = ',num2str(z(j)),' m'])
    grid on
    n=n+1;
  end
end

print -dpdf test2_2.pdf
