%a = xmlread('Wind_Polar.xml');
load data.mat

anglei = [10;30;35;40;45;A(2:end-1,1)*180/pi;160;170]*pi/180;
value = zeros(length(anglei),length(V));
for i = 1:length(V)
    value(:,i) = interp1([10*pi/180;A(:,i);180*pi/180],...
        [1;Vboat(:,i);-Vboat(end,i)*cos(A(end,i))],anglei,'spline','extrap');
end
figure(1); clf;
cmap = jet(length(V));
for i = 1:length(V)
    h1 = polar(anglei,value(:,i));
    hold on;
    h2 = polar(A(:,i),Vboat(:,i));
    set(h1,'Color',cmap(i,:),'Marker','.');
    set(h2,'Color',cmap(i,:),'LineStyle','none','Marker','o');
    
end
%angle = A(2:end-1,:)*180/pi;
%value = Vboat(2:end-1,:);
curve = V;
angle = anglei*180/pi;
docNode = com.mathworks.xml.XMLUtils.createDocument('Polar');
for i = 1:size(value,2)
    curve_node = docNode.createElement('PolarCurve');
    docNode.getDocumentElement.appendChild(curve_node);
    curve_index_node = docNode.createElement('PolarCurveIndex');
    curve_index_node.setAttribute('value',num2str(curve(i)));
    curve_node.appendChild(curve_index_node);
    for j = 1:size(value,1)
        item_node = docNode.createElement('PolarItem');
        curve_node.appendChild(item_node);
        angle_node = docNode.createElement('Angle');
        angle_node.setAttribute('value',num2str(angle(j)))
        item_node.appendChild(angle_node);
        value_node = docNode.createElement('Value');
        value_node.setAttribute('value',num2str(value(j,i)))
        item_node.appendChild(value_node);
    end
end
xmlwrite(docNode)
xmlwrite('pirat_polar.xml',docNode)
