%%

war = [];
wsr = [];
sow = [];

files = ls('tmp/*.csv');

for i = 1:size(files,1)
    [Latitude,Longitude,SpeedKnots,MagneticHeading, ...
        WindAngleRelative,WindSpeedRelative,SOWKnots] = importfile(['tmp/' files(i,:)]);

    war = [war;WindAngleRelative*pi/180];
    wsr = [wsr;WindSpeedRelative];
    sow = [sow;SOWKnots];
end
bad_inds = isnan(wsr) | (war < 30*pi/180) | (war > 330*pi/180) | isnan(sow);
wsr(bad_inds) = [];
war(bad_inds) = [];
sow(bad_inds) = [];

y = wsr.*sin(war);
x = wsr.*cos(war) - sow;

ws = sqrt(x.^2 + y.^2);
wa = atan2(y,x);

figure(1)
polar(wa,sow,'*')

wa_i = linspace(0,2*pi,100)';
%wind_speed = linspace(0,max(ws),50)';
sow_i = linspace(0,max(sow),50);

[wa_gr,sow_gr] = meshgrid(wa_i,sow_i);

ws_gr = griddata(wa,sow,ws,wa_gr,sow_gr);

figure(2); clf; hold on;
contour(wa_gr,sow_gr,ws_gr)
plot(wa,sow,'*')

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
plot(X2,Y2,'*')
contour(X,Y,ws_gr_sm)
colorbar

