%plot outputs from gurobi
clear Data
cd ../GurobiControl

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
        plot([Data(i).times(n),Data(i).times(n)], [Data(i).upbnd(n) Data(i).lowbnd(n)],'linewidth',10);
    end
    title(strcat({'Reachability analysis for: '},strrep(Data(i).lbl,'.csv','')))
    xlabel('depth (time)')
    ylabel('glucose concentration (mg/dL)')
    hold off;
end
