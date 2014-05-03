%%

war = [];
wsr = [];
sow = [];
lat = [];
lon = [];

files = ls('tmp2/*.csv');

for i = 1:size(files,1)
    [UTC,Latitude,Longitude,SpeedKnots,MagneticHeading,...
        WindAngleRelative,WindSpeedRelative,SOWKnots] = importfile2(['tmp2/' files(i,:)]);

    war = [war;WindAngleRelative*pi/180];
    wsr = [wsr;WindSpeedRelative];
    sow = [sow;SOWKnots];
    lat = [lat;Latitude];
    lon = [lon;Longitude];
end

%%
no_zone = 15;
bad_inds = isnan(wsr) | (war < no_zone*pi/180) | (war > (360-no_zone)*pi/180) | isnan(sow);
wsr(bad_inds) = [];
war(bad_inds) = [];
sow(bad_inds) = [];

y = wsr.*sin(war);
x = wsr.*cos(war) - sow;

ws = sqrt(x.^2 + y.^2);
wa = atan2(y,x);

bad_inds2 = ws < 5;
ws(bad_inds2) = [];
wa(bad_inds2) = [];
sow(bad_inds2) = [];

figure(1)
polar(wa,sow,'*')

wa_i = linspace(-pi,pi,100)';
%wind_speed = linspace(0,max(ws),50)';
sow_i = linspace(0,max(sow),50);

[wa_gr,sow_gr] = meshgrid(wa_i,sow_i);

ws_gr = griddata(wa,sow,ws,wa_gr,sow_gr);

figure(2); clf; hold on;
plot(wa,sow,'.')
contour(wa_gr,sow_gr,ws_gr)


figure(22);
 h = 1/16*ones(4);
ws_gr_sm = filter2(h,ws_gr);
 surf(wa_gr,sow_gr,ws_gr_sm)

[X,Y] = pol2cart(wa_gr,sow_gr);

figure(3); clf;
h = polar([0 2*pi], [0 max(sow)]);
delete(h)
hold on
[X2,Y2] = pol2cart(wa,sow);
plot(X2,Y2,'.')
contour(X,Y,ws_gr_sm)
colorbar

figure(4);
h = polar([0 2*pi], [0 max(sow)]);
delete(h)
hold on
surf(X,Y,ws_gr_sm)
colorbar

%%
figure(5); clf;
num_points = 50;
cmap = jet(num_points);
h = polar([0 2*pi], [0 max(sow)]);
ph=findall(gca,'type','patch');
set(ph,'facecolor',[0,0,0],'edgecolor',[1,1,1]);
polar_lines = [findall(gca,'Type','line');findall(gca,'Type','text')];
polar_text = findall(gca,'Type','text');

hold on;
ws_bins = linspace(min(ws),max(ws),num_points+1);
%for i = num_points:-1:1
for i = 1:num_points   
    inds = ws > ws_bins(i) & ws < ws_bins(i+1);
    h = polar(wa(inds),sow(inds),'*');%,'MarkerFaceColor',cmap(i,:))
     
    set(h,'MarkerEdgeColor',cmap(i,:),'MarkerSize',2)
end
set(gca,'Color',[0 0 0])
caxis([min(ws) max(ws)])
colorbar
set(gcf,'Color',[0 0 0])
set(gca,'Color',[0 0 0])

set(polar_text,'HorizontalAlignment','center','VerticalAlignment','middle','FontSize',14);
for i = 1:length(polar_text)
    set(polar_text(i),'String',strrep(get(polar_text(i),'String'),' ',''));
end
text2 = copyobj(polar_text,gca);
set(text2,'FontSize',18);
set(polar_lines,'Color',.8*[1 1 1])
uistack(polar_lines,'top')

polar_pirat

delete(h)


figure(6);
plot(lon,lat,'.')
axis equal

