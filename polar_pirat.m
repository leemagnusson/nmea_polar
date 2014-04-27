load data.mat

%figure(1); clf;
%cmap = jet(size(A,2));
for i = 1:size(A,2)
    h = polar(A(:,i),Vboat(:,i));
    hold on;
    imap = find(V(i)>ws_bins,1,'last');
    set(h,'Color',cmap(imap,:),'Linewidth',2);
end
