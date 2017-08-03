%plot outputs from gurobi
%taisa kushner 
%aug 1 2017

clear Data
close all
beep off

allGurobifiles=dir('*.csv');
MAX=numel(allGurobifiles);

Data(MAX).times=[];
Data(MAX).lowbnd=[];
Data(MAX).upbnd=[];
Data(MAX).lbl=[];
for i=1:MAX
    Data(i).lbl=allGurobifiles(i).name;
    [Data(i).times, Data(i).lowbnd, Data(i).upbnd]=importGurobiData(allGurobifiles(i).name);
end

for i=1:MAX
    figure(i)
    hold on;
    for n = 1 : numel(Data(i).upbnd)
        plot([Data(i).times(n),Data(i).times(n)], [Data(i).upbnd(n) Data(i).lowbnd(n)],'Color',[.612,.769,.635],'linewidth',10);
    end
    title(strcat({'Reachability analysis for: '},strrep(strrep(Data(3).lbl, '.csv',''),'_',{' '})),'FontSize',16)
    xlabel('depth (time)','FontSize',14)
    ylabel('glucose concentration (mg/dL)','FontSize',14)
    hold off;
end
