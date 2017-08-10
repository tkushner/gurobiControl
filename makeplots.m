%plot outputs from gurobi
%taisa kushner 
%aug 1 2017

clear Data
close all
beep off
allGurobifiles=dir('./outputs/PSO3-*');
MAX=numel(allGurobifiles);

Data(MAX).times=[];
Data(MAX).lowbnd=[];
Data(MAX).upbnd=[];
Data(MAX).lbl=[];

for i=1:MAX
    Data(i).lbl=allGurobifiles(i).name;
    [Data(i).times, Data(i).lowbnd, Data(i).upbnd]=importGurobiData(strcat('./outputs/',allGurobifiles(i).name));
end

for i=1:MAX
    figure(i)
    hold on;
    for n = 1 : numel(Data(i).upbnd)
        plot([Data(i).times(n),Data(i).times(n)], [Data(i).upbnd(n) Data(i).lowbnd(n)],'Color',[.612,.769,.635],'linewidth',10);
        maxt=max(Data(i).times)+10;
        b1=plot(1:maxt, repmat(70,1,maxt),'--r');
        plot(1:maxt,repmat(180,1,maxt),'--r');
        b2=plot(1:maxt,repmat(80,1,maxt),'--k');
        plot(1:maxt,repmat(120,1,maxt),'--k')
    end
    title(strcat({'Reachability analysis for: '},strrep(strrep(Data(i).lbl, '.csv',''),'_',{' '})),'FontSize',16)
    xlabel('depth (time)','FontSize',14)
    ylabel('glucose concentration (mg/dL)','FontSize',14)
    legend([b1,b2],'Safe Bounds for hyper and hypoglycemia','Goal Euglycemic Range')
    hold off;
end
