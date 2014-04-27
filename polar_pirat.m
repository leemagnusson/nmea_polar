load data.mat

figure(1); clf;
cmap = jet(size(A,2));
for i = 1:size(A,2)
    h = polar(A(:,i),Vboat(:,i));
    hold on;
    set(h,'Color',cmap(i,:));
end
